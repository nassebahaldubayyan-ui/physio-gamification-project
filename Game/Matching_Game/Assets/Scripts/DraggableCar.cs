using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    [Header("Color")]
    public ColorType color;

    [Header("Drop Distance (world units)")]
    public float dropDistance = 2.5f;

    [Header("Spawn Protection")]
    public float spawnGracePer = 0.2f;

    private bool isHolding = false;
    private bool handClosed = false;
    private bool prevHandClosed = false;
    private float spawnTime;
    private Transform handPoint;
    private Collider2D carCollider;
    private Rigidbody2D rb;

    void Start()
    {
        spawnTime = Time.time;

        if (!gameObject.CompareTag("Car"))
            gameObject.tag = "Car";

        // ✅ إيقاف الجاذبية
        rb = GetComponent<Rigidbody2D>();
        if (rb != null)
        {
            rb.gravityScale = 0;
            rb.bodyType = RigidbodyType2D.Kinematic;
        }

        // الـ Collider
        carCollider = GetComponent<Collider2D>();
        if (carCollider == null)
        {
            BoxCollider2D box = gameObject.AddComponent<BoxCollider2D>();
            box.size = new Vector2(7f, 5f);
            carCollider = box;
        }
        // ✅ لا نغير isTrigger أبداً — نخليه ثابت
        carCollider.isTrigger = false;

        GameObject hand = GameObject.FindGameObjectWithTag("Hand");
        if (hand != null) handPoint = hand.transform;
    }

    void Update()
    {
        if (handPoint == null)
        {
            GameObject hand = GameObject.FindGameObjectWithTag("Hand");
            if (hand == null) { prevHandClosed = handClosed; return; }
            handPoint = hand.transform;
        }

        bool graceOver = (Time.time - spawnTime) > spawnGracePer;
        bool handOverCar = carCollider != null && carCollider.OverlapPoint(handPoint.position);
        bool justClosed = handClosed && !prevHandClosed;

        // ── الإمساك ──────────────────────────────────────────
        if (justClosed && graceOver && handOverCar && !isHolding)
        {
            isHolding = true;
            Debug.Log($"[DraggableCar] Grabbed {color}");
        }

        // ── الإفلات ──────────────────────────────────────────
        if (!handClosed && isHolding)
        {
            isHolding = false;
            CheckDrop();
        }

        // ── ملاحقة اليد ──────────────────────────────────────
        if (isHolding)
        {
            transform.position = new Vector3(
                handPoint.position.x,
                handPoint.position.y,
                0f);
        }

        prevHandClosed = handClosed;
    }

    void CheckDrop()
    {
        Basket[] baskets = FindObjectsOfType<Basket>();
        foreach (Basket basket in baskets)
        {
            if (basket == null) continue;

            // ✅ هل السيارة داخل حدود السلة؟
            if (basket.ContainsPoint(transform.position) && basket.color == color)
            {
                if (GameManager.Instance != null)
                    GameManager.Instance.AddScore(1);
                Debug.Log($"[DraggableCar] Matched {color} → +1");
                Destroy(gameObject);
                return;
            }
        }
    }

    public void SetHandClosed(bool closed) => handClosed = closed;
    public bool IsHolding() => isHolding;
}