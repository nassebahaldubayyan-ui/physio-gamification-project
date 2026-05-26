using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    public ColorType color;

    [Header("Grab / Drop Distance (world units)")]
    public float grabDistance = 5f;
    public float dropDistance = 2.5f;

    [Header("Spawn Protection")]
    public float spawnGracePer = 0.2f;

    private bool isHolding = false;
    private bool handClosed = false;
    private bool prevHandClosed = false;  
    private float spawnTime;
    private Transform handPoint;
    private Basket[] cachedBaskets;

    void Start()
    {
        spawnTime = Time.time;

        if (!gameObject.CompareTag("Car"))
            gameObject.tag = "Car";

        GameObject hand = GameObject.FindGameObjectWithTag("Hand");
        if (hand != null) handPoint = hand.transform;

        cachedBaskets = FindObjectsOfType<Basket>();
    }

    void Update()
    {
        if (handPoint == null)
        {
            GameObject hand = GameObject.FindGameObjectWithTag("Hand");
            if (hand == null) { prevHandClosed = handClosed; return; }
            handPoint = hand.transform;
        }

        float distanceToHand = Vector2.Distance(transform.position, handPoint.position);
        bool graceOver = (Time.time - spawnTime) > spawnGracePer;

        bool justClosed = handClosed && !prevHandClosed;
        if (justClosed && graceOver && distanceToHand < grabDistance && !isHolding)
        {
            isHolding = true;
            Debug.Log($"[DraggableCar] Grabbed {color} at dist {distanceToHand:F2}");
        }

        if (!handClosed && isHolding)
        {
            isHolding = false;

            if (IsOverMatchingBasket())
            {
                if (GameManager.Instance != null)
                    GameManager.Instance.AddScore(1);
                Destroy(gameObject);
            }
        }

        if (isHolding)
            transform.position = new Vector3(handPoint.position.x, handPoint.position.y, 0f);

        prevHandClosed = handClosed;
    }

    public void SetHandClosed(bool closed) => handClosed = closed;
    public bool IsHolding() => isHolding;

    bool IsOverMatchingBasket()
    {
        if (cachedBaskets == null || cachedBaskets.Length == 0)
            cachedBaskets = FindObjectsOfType<Basket>();

        foreach (Basket basket in cachedBaskets)
        {
            if (basket == null) continue;
            if (Vector2.Distance(transform.position, basket.transform.position) < dropDistance
                && basket.color == color)
                return true;
        }
        return false;
    }
}