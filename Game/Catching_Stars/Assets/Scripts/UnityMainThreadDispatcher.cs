using UnityEngine;
using System.Collections.Generic;

public class UnityMainThreadDispatcher : MonoBehaviour
{
    private static UnityMainThreadDispatcher instance;
    private readonly Queue<System.Action> actions = new Queue<System.Action>();

    public static UnityMainThreadDispatcher Instance()
    {
        if (instance == null)
        {
            GameObject go = new GameObject("MainThreadDispatcher");
            instance = go.AddComponent<UnityMainThreadDispatcher>();
            DontDestroyOnLoad(go);
        }
        return instance;
    }

    void Update()
    {
        lock (actions)
        {
            while (actions.Count > 0)
            {
                actions.Dequeue().Invoke();
            }
        }
    }

    public void Enqueue(System.Action action)
    {
        lock (actions)
        {
            actions.Enqueue(action);
        }
    }
}