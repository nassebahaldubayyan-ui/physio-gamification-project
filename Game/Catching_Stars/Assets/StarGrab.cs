using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class CatchStarsReceiver : MonoBehaviour
{
    public int port = 5052;
    public Transform handPoint;          // Assign the Palm transform used in StarGrab
    public StarGrab starGrab;            // Assign the StarGrab component

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;

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
                // Execute on main thread
                UnityMainThreadDispatcher.Instance().Enqueue(() => UpdateGame(packet));
            }
            catch (System.Exception e) { Debug.Log(e); }
        }
    }

    void UpdateGame(TrackerPacket p)
    {
        if (handPoint != null)
        {
            // Convert normalised palm coordinates to world position
            Vector3 worldPos = Camera.main.ViewportToWorldPoint(new Vector3(p.palm_x, p.palm_y, 10f));
            handPoint.position = worldPos;
        }
        if (starGrab != null)
        {
            starGrab.handClosed = p.hand_closed;
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