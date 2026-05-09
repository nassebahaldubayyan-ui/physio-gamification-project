using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class MatchingReceiver : MonoBehaviour
{
    public int port = 5052;

    [Header("Hand Object")]
    public Transform handPoint;

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;

    private TrackerPacket latestPacket;
    private readonly object packetLock = new object();

    void Start()
    {
        // إذا ما فيه HandPoint
        if (handPoint == null)
        {
            GameObject h = GameObject.FindGameObjectWithTag("Hand");

            if (h == null)
            {
                h = new GameObject("HandPoint");
                h.tag = "Hand";
            }

            handPoint = h.transform;
        }

        // تشغيل UDP
        try
        {
            udpClient = new UdpClient(port);

            receiveThread = new Thread(new ThreadStart(ReceiveData));
            receiveThread.IsBackground = true;
            receiveThread.Start();

            Debug.Log("[MatchingReceiver] UDP Started");
        }
        catch (System.Exception e)
        {
            Debug.LogError("UDP Start Error: " + e.Message);
        }
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

                TrackerPacket packet =
                    JsonUtility.FromJson<TrackerPacket>(json);

                lock (packetLock)
                {
                    latestPacket = packet;
                }
            }
            catch (System.Exception e)
            {
                if (isRunning)
                    Debug.LogError("UDP Error: " + e.Message);
            }
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
        // تحريك اليد
        if (handPoint != null && Camera.main != null)
        {
            Vector3 worldPos =
                Camera.main.ViewportToWorldPoint(
                    new Vector3(p.palm_x, p.palm_y, 10f)
                );

            worldPos.z = 0f;

            handPoint.position = worldPos;
        }

        // إرسال حالة القبضة للسيارات
        DraggableCar[] allCars =
            FindObjectsOfType<DraggableCar>();

        foreach (DraggableCar car in allCars)
        {
            car.SetHandClosed(p.hand_closed);
        }
    }

    void OnDestroy()
    {
        isRunning = false;

        if (receiveThread != null && receiveThread.IsAlive)
            receiveThread.Join(200);

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