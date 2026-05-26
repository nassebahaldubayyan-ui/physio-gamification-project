// ============================================================
// MatchingReceiver.cs
// يستقبل بيانات اليد من HTML (WebGL) أو UDP (Editor)
// ويحرك نقطة اليد ويُبلّغ كل السيارات بحالة القبضة
// ============================================================
using UnityEngine;

#if !UNITY_WEBGL || UNITY_EDITOR
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
#endif

public class MatchingReceiver : MonoBehaviour
{
    [Header("Settings")]
    public int       port      = 5053;
    public Transform handPoint;

#if !UNITY_WEBGL || UNITY_EDITOR
    private UdpClient  udpClient;
    private Thread     receiveThread;
    private bool       isRunning  = true;
    private TrackerPacket latestPacket;
    private readonly object packetLock = new object();
#endif

    // ─────────────────────────────────────────────────────────
    void Start()
    {
        // أنشئ كائن اليد إذا لم يكن موجوداً
        if (handPoint == null)
        {
            GameObject hand = GameObject.FindGameObjectWithTag("Hand")
                           ?? GameObject.Find("Hand");

            if (hand == null)
            {
                hand     = new GameObject("Hand");
                hand.tag = "Hand";
            }
            handPoint = hand.transform;
        }

#if !UNITY_WEBGL || UNITY_EDITOR
        try
        {
            udpClient     = new UdpClient(port);
            receiveThread = new Thread(ReceiveData) { IsBackground = true };
            receiveThread.Start();
            Debug.Log($"[MatchingReceiver] UDP started on port {port}");
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("[MatchingReceiver] UDP disabled: " + e.Message);
        }
#else
        Debug.Log("[MatchingReceiver] WebGL mode — waiting for JS packets.");
#endif
    }

    // ─────────────────────────────────────────────────────────
#if !UNITY_WEBGL || UNITY_EDITOR

    void ReceiveData()
    {
        IPEndPoint ep = new IPEndPoint(IPAddress.Any, port);
        while (isRunning)
        {
            try
            {
                byte[]  data   = udpClient.Receive(ref ep);
                string  json   = Encoding.UTF8.GetString(data);
                var     packet = JsonUtility.FromJson<TrackerPacket>(json);
                lock (packetLock) { latestPacket = packet; }
            }
            catch (System.Exception e)
            {
                if (isRunning) Debug.LogError("[MatchingReceiver] UDP error: " + e.Message);
            }
        }
    }

    void Update()
    {
        lock (packetLock)
        {
            if (latestPacket == null) return;
            UpdateGame(latestPacket);
            latestPacket = null;
        }
    }

#else
    // WebGL: يُستدعى من JavaScript
    void Update() { }

    public void ReceivePacketFromJS(string json)
    {
        try
        {
            TrackerPacket packet = JsonUtility.FromJson<TrackerPacket>(json);
            if (packet != null) UpdateGame(packet);
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("[MatchingReceiver] Parse error: " + e.Message);
        }
    }
#endif

    // ─────────────────────────────────────────────────────────
    // يُحدّث موقع اليد وحالة القبضة لكل السيارات
    // ─────────────────────────────────────────────────────────
    void UpdateGame(TrackerPacket p)
    {
        // حرّك نقطة اليد في فضاء Unity
        if (Camera.main != null && handPoint != null)
        {
            Vector3 worldPos = Camera.main.ViewportToWorldPoint(
                new Vector3(p.palm_x, p.palm_y, 10f));
            worldPos.z       = 0f;
            handPoint.position = worldPos;
        }

        // أبلّغ كل السيارات بحالة القبضة
        foreach (DraggableCar car in FindObjectsOfType<DraggableCar>())
        {
            if (car != null)
                car.SetHandClosed(p.hand_closed);
        }
    }

    // ─────────────────────────────────────────────────────────
    void OnDestroy()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        isRunning = false;
        receiveThread?.Join(200);
        udpClient?.Close();
#endif
    }

    // ─────────────────────────────────────────────────────────
    [System.Serializable]
    public class TrackerPacket
    {
        public float palm_x;
        public float palm_y;
        public bool  hand_closed;
        public float timestamp;
    }
}