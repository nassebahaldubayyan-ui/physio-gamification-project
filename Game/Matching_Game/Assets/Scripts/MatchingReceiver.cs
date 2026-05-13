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

#if !UNITY_WEBGL || UNITY_EDITOR
    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;
    private TrackerPacket latestPacket;
    private object packetLock = new object();
#endif

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
        Debug.Log("MatchingReceiver: WebGL build - UDP disabled, using JS bridge instead.");
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

                lock (packetLock)
                {
                    latestPacket = packet;
                }
            }
            catch (System.Exception e) { Debug.LogError("UDP Error: " + e.Message); }
        }
    }

    void Update()
    {
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
    // WebGL: receive packets via JS bridge -> unityInstance.sendMessage("MatchingReceiver", "ReceivePacketFromJS", json)
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
        if (handPoint != null)
        {
            Vector3 worldPos =
                Camera.main.ViewportToWorldPoint(
                    new Vector3(
                        p.palm_x,
                        p.palm_y,
                        10f
                    )
                );

            worldPos.z = 0f;

            handPoint.position = Vector3.Lerp(
                handPoint.position,
                worldPos,
                Time.deltaTime * 30f
            );
        }
        DraggableCar[] allCars = FindObjectsOfType<DraggableCar>();

        DraggableCar closestCar = null;
        float closestDistance = Mathf.Infinity;

        foreach (DraggableCar car in allCars)
        {
            float dist = Vector2.Distance(
                handPoint.position,
                car.transform.position
            );

            if (dist < closestDistance)
            {
                closestDistance = dist;
                closestCar = car;
            }
        }

        foreach (DraggableCar car in allCars)
        {
            car.SetHandClosed(false);
        }

        if (closestCar != null && closestDistance < 2f)
        {
            closestCar.SetHandClosed(p.hand_closed);
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
