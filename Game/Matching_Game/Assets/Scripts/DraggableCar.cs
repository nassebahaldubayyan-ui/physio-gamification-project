using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    public ColorType color;

    [Header("Drag thresholds (world units)")]
    public float grabDistance = 1.5f;
    public float dropDistance = 1.5f;

    private bool isHolding = false;
    private bool handClosed = false;
    private Transform handPoint;
    private CircleCollider2D carCollider;

    void Start()
    {
        carCollider = GetComponent<CircleCollider2D>();
        if (carCollider == null)
            carCollider = gameObject.AddComponent<CircleCollider2D>();

        if (!gameObject.CompareTag("Car"))
            gameObject.tag = "Car";

        handPoint = FindHandPoint();
    }

    void Update()
    {
        if (handPoint == null)
        {
            handPoint = FindHandPoint();
            if (handPoint == null) return;
        }

        float distanceToHand = Vector2.Distance(transform.position, handPoint.position);

        // 1: hand closed + car nearby + not already holding -> grab
        if (handClosed && distanceToHand < grabDistance && !isHolding)
        {
            isHolding = true;
            if (carCollider != null) carCollider.enabled = false;
            Debug.Log($"Grabbed {color} car (dist={distanceToHand:F2})");
        }

        // 2: hand opened while holding -> drop (and check for match)
        if (!handClosed && isHolding)
        {
            isHolding = false;
            if (carCollider != null) carCollider.enabled = true;

            if (IsOverMatchingBasket())
            {
                if (GameManager.Instance != null)
                    GameManager.Instance.AddScore(10);
                Destroy(gameObject);
            }
        }

        if (isHolding)
        {
            transform.position = handPoint.position;
        }
    }

   
    private Transform FindHandPoint()
    {
        GameObject hand = GameObject.Find("Hand");
        if (hand == null) hand = GameObject.FindGameObjectWithTag("Hand");
        return hand != null ? hand.transform : null;
    }

    public void SetHandClosed(bool closed)
    {
        handClosed = closed;
    }

    public bool IsHolding()
    {
        return isHolding;
    }

    bool IsOverMatchingBasket()
    {
        Basket[] allBaskets = FindObjectsOfType<Basket>();
        foreach (Basket basket in allBaskets)
        {
            if (Vector2.Distance(transform.position, basket.transform.position) < dropDistance
                && basket.color == color)
                return true;
        }
        return false;
    }
}