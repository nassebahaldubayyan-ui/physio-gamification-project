using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    public ColorType color;

    [Header("Grab Settings")]
    public float grabDistance = 2.5f;   
    public float dropDistance = 2.5f;     // مسافة الإيداع في السلة

    private bool isHolding = false;
    private bool handClosed = false;
    private Transform handPoint;
    private BoxCollider2D carCollider;

    void Start()
    {
        carCollider = GetComponent<BoxCollider2D>();
        if (carCollider == null)
            carCollider = gameObject.AddComponent<BoxCollider2D>();


        if (!gameObject.CompareTag("Car"))
            gameObject.tag = "Car";

        FindHand();
    }

    void FindHand()
    {
        GameObject hand = GameObject.FindGameObjectWithTag("Hand");
        if (hand != null) handPoint = hand.transform;
    }

    void Update()
    {
        if (handPoint == null)
        {
            FindHand();
            if (handPoint == null) return;
        }

        float distanceToHand = Vector2.Distance(transform.position, handPoint.position);

        // حالة 1: اليد مقفلة + قريبة → امسك
        if (handClosed && distanceToHand < grabDistance && !isHolding)
        {
            isHolding = true;
            if (carCollider != null) carCollider.enabled = false;
            Debug.Log($"[DraggableCar] Grabbed {color} car. dist={distanceToHand:F2}");
        }

        // حالة 2: اليد فُتحت + ممسوكة → جرّب الإيداع
        if (!handClosed && isHolding)
        {
            isHolding = false;
            if (carCollider != null) carCollider.enabled = true;

            if (IsOverMatchingBasket())
            {
                if (GameManager.instance != null)
                    GameManager.instance.AddScore(10);
                Destroy(gameObject);
            }
        }

        // تحريك السيارة مع اليد
        if (isHolding)
        {
            transform.position = handPoint.position;
        }
    }

    public void SetHandClosed(bool closed) { handClosed = closed; }
    public bool IsHolding() { return isHolding; }

    bool IsOverMatchingBasket()
    {
        Basket[] allBaskets = FindObjectsOfType<Basket>();
        foreach (Basket basket in allBaskets)
        {
            float dist = Vector2.Distance(transform.position, basket.transform.position);
            if (dist < dropDistance && basket.color == color)
                return true;
        }
        return false;
    }
}
