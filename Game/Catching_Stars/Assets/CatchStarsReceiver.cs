using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class CatchStarsReceiver : MonoBehaviour
{
    public int port = 5052;
    public Transform handPoint;          

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;
    private TrackerPacket latestPacket;
    private object packetLock = new object();

    void Start()
    {
        udpClient = new UdpClient(port);
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
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
        if (handPoint != null)
        {
            //  ÕÊÌ· „‰ Viewport (0-1) ≈·Ï World Space
            Vector3 worldPos = Camera.main.ViewportToWorldPoint(new Vector3(p.palm_x, p.palm_y, 10f));
            handPoint.position = worldPos;
        }

        StarGrab[] allStars = FindObjectsOfType<StarGrab>();
        foreach (StarGrab star in allStars)
        {
            star.SetHandClosed(p.hand_closed);
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