using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    public ColorType color;

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

        GameObject hand = GameObject.FindGameObjectWithTag("Hand");
        if (hand != null) handPoint = hand.transform;
    }

    void Update()
    {
        if (handPoint == null)
        {
            GameObject hand = GameObject.FindGameObjectWithTag("Hand");
            if (hand != null) handPoint = hand.transform;
            return;
        }

        float distanceToHand = Vector2.Distance(transform.position, handPoint.position);

        // حالة 1: اليد مقفلة + السيارة قريبة → امسك
        if (handClosed && distanceToHand < 1.5f && !isHolding)
        {
            isHolding = true;
            if (carCollider != null) carCollider.enabled = false;
            Debug.Log($"Grabbed {color} car");
        }

        // حالة 2: اليد فتحت + السيارة ممسوكة → حاول الإيداع
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

        // تحريك السيارة مع اليد
        if (isHolding)
        {
            transform.position = handPoint.position;
        }
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
            if (Vector2.Distance(transform.position, basket.transform.position) < 1.5f && basket.color == color)
                return true;
        }
        return false;
    }
}