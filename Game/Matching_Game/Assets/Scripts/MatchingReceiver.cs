using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class MatchingReceiver : MonoBehaviour
{
    public int port = 5053;  
    public Transform handPoint;

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;
    private TrackerPacket latestPacket;
    private object packetLock = new object();

    void Start()
    {
        if (handPoint == null)
        {
            GameObject hand = GameObject.FindGameObjectWithTag("Hand");
            if (hand == null)
            {
                hand = new GameObject("HandPoint");
                hand.tag = "Hand";
            }
            handPoint = hand.transform;
        }

        udpClient = new UdpClient(port);
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        
        Debug.Log($"MatchingReceiver started on port {port}");
    }

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

    void UpdateGame(TrackerPacket p)
    {
        if (handPoint != null && Camera.main != null)
        {
            Vector3 worldPos = Camera.main.ViewportToWorldPoint(new Vector3(p.palm_x, p.palm_y, 10f));
            worldPos.z = 0f;
            handPoint.position = worldPos;
        }

        // إرسال حالة القبضة لكل السيارات
        DraggableCar[] allCars = FindObjectsOfType<DraggableCar>();
        foreach (DraggableCar car in allCars)
        {
            car.SetHandClosed(p.hand_closed);
        }
    }

    void OnDestroy()
    {
        isRunning = false;
        receiveThread?.Join();
        udpClient?.Close();
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