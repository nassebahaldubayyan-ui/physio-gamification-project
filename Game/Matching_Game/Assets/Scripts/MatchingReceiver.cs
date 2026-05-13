using UnityEngine;
#if !UNITY_WEBGL || UNITY_EDITOR
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
#endif

public class MatchingReceiver : MonoBehaviour
{
    public int port = 5053;
    public Transform handPoint;

    [Header("Hand Smoothing")]
    [Range(5f, 30f)]
    public float handFollowSpeed = 20f;  

    private Vector3 targetHandPos;  

#if !UNITY_WEBGL || UNITY_EDITOR
    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;
    private TrackerPacket latestPacket;
    private object packetLock = new object();
#endif

    private DraggableCar[] cachedCars = new DraggableCar[0];
    private float cacheRefreshInterval = 0.5f;
    private float lastCacheTime = -1f;

    void Start()
    {
        if (handPoint == null)
        {
            GameObject hand = GameObject.Find("Hand");
            if (hand == null) hand = GameObject.FindGameObjectWithTag("Hand");
            if (hand == null)
            {
                hand = new GameObject("Hand");
                hand.tag = "Hand";
            }
            handPoint = hand.transform;
        }

        targetHandPos = handPoint.position;

#if !UNITY_WEBGL || UNITY_EDITOR
        try
        {
            udpClient = new UdpClient(port);
            receiveThread = new Thread(new ThreadStart(ReceiveData));
            receiveThread.IsBackground = true;
            receiveThread.Start();
            Debug.Log($"MatchingReceiver started on port {port}");
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("MatchingReceiver disabled: " + e.Message);
        }
#else
        Debug.Log("MatchingReceiver: WebGL build - UDP disabled.");
#endif
    }

#if !UNITY_WEBGL || UNITY_EDITOR
    void ReceiveData()
    {
        IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, port);
        while (isRunning)
        {
            try
            {
                byte[] data = udpClient.Receive(ref remoteEP);
                string json = Encoding.UTF8.GetString(data);
                var packet = JsonUtility.FromJson<TrackerPacket>(json);
                lock (packetLock) { latestPacket = packet; }
            }
            catch (System.Exception e) { Debug.LogError("UDP Error: " + e.Message); }
        }
    }

    void Update()
    {
        if (Time.time - lastCacheTime > cacheRefreshInterval)
        {
            cachedCars = FindObjectsOfType<DraggableCar>();
            lastCacheTime = Time.time;
        }

        if (handPoint != null)
            handPoint.position = Vector3.Lerp(handPoint.position, targetHandPos, Time.deltaTime * handFollowSpeed);

        lock (packetLock)
        {
            if (latestPacket != null)
            {
                UpdateGame(latestPacket);
                latestPacket = null;
            }
        }
    }
#else
    void Update()
    {
        if (Time.time - lastCacheTime > cacheRefreshInterval)
        {
            cachedCars = FindObjectsOfType<DraggableCar>();
            lastCacheTime = Time.time;
        }
        if (handPoint != null)
            handPoint.position = Vector3.Lerp(handPoint.position, targetHandPos, Time.deltaTime * handFollowSpeed);
    }

    public void ReceivePacketFromJS(string json)
    {
        try
        {
            TrackerPacket packet = JsonUtility.FromJson<TrackerPacket>(json);
            if (packet != null) UpdateGame(packet);
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("ReceivePacketFromJS parse error: " + e.Message);
        }
    }
#endif

    void UpdateGame(TrackerPacket p)
    {
        if (Camera.main != null)
        {
            Vector3 worldPos = Camera.main.ViewportToWorldPoint(new Vector3(p.palm_x, p.palm_y, 10f));
            worldPos.z = 0f;
            targetHandPos = worldPos; 
        }

        foreach (DraggableCar car in cachedCars)
        {
            if (car != null)
                car.SetHandClosed(p.hand_closed);
        }
    }

    void OnDestroy()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        isRunning = false;
        receiveThread?.Join();
        udpClient?.Close();
#endif
    }

    [System.Serializable]
    public class TrackerPacket
    {
        public float palm_x;
        public float palm_y;
        public bool hand_closed;
        public float timestamp;
    }
}