using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    public ColorType color;

    [Header("Drag thresholds (world units)")]
    public float grabDistance = 1.5f;
    public float dropDistance = 1.5f;

    [Header("Spawn Protection")]
    public float spawnGracePer = 0.3f;

    [Header("Smoothing")]
    [Range(5f, 25f)]
    public float followSpeed = 15f;  

    private bool isHolding = false;
    private bool handClosed = false;
    private float spawnTime;
    private Transform handPoint;
    private CircleCollider2D carCollider;
    private Basket[] cachedBaskets;  

    void Start()
    {
        spawnTime = Time.time;

        carCollider = GetComponent<CircleCollider2D>();
        if (carCollider == null)
            carCollider = gameObject.AddComponent<CircleCollider2D>();

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
            if (hand == null) return;
            handPoint = hand.transform;
        }

        float distanceToHand = Vector2.Distance(transform.position, handPoint.position);
        bool graceOver = (Time.time - spawnTime) > spawnGracePer;

        if (handClosed && graceOver && distanceToHand < grabDistance && !isHolding)
        {
            isHolding = true;
            if (carCollider != null) carCollider.enabled = false;
            Debug.Log($"Grabbed {color} car");
        }

        if (!handClosed && isHolding)
        {
            isHolding = false;
            if (carCollider != null) carCollider.enabled = true;

            if (IsOverMatchingBasket())
            {
                if (GameManager.Instance != null)
                    GameManager.Instance.AddScore(1);
                Destroy(gameObject);
            }
        }

        if (isHolding)
        {
            transform.position = Vector3.Lerp(
                transform.position,
                handPoint.position,
                Time.deltaTime * followSpeed
            );
        }
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