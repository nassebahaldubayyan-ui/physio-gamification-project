using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    private bool isHolding = false;
    private bool handClosed = false;

    private Transform handPoint;

    [Header("Grab Settings")]
    public float grabDistance = 1.5f;
    public float dropDistance = 1.5f;
    public ColorType color;


    private Rigidbody2D rb;
    private Collider2D carCollider;

    void Start()
    {
        GameObject hand = GameObject.FindGameObjectWithTag("Hand");

        if (hand != null)
            handPoint = hand.transform;

        rb = GetComponent<Rigidbody2D>();

        carCollider = GetComponent<Collider2D>();
    }

    void Update()
    {
        if (handPoint == null) return;

        float distance =
            Vector2.Distance(transform.position, handPoint.position);

        // =========================
        // إمساك السيارة
        // =========================
        if (handClosed &&
            !isHolding &&
            distance < grabDistance)
        {
            StartHolding();
        }

        // =========================
        // إفلات السيارة
        // =========================
        if (!handClosed && isHolding)
        {
            StopHolding();
        }

        // =========================
        // تحريك السيارة مع اليد
        // =========================
        if (isHolding)
        {
            transform.position = Vector3.Lerp(
    transform.position,
    handPoint.position,
    Time.deltaTime * 18f
);

        }
    }

    void StartHolding()
    {
        isHolding = true;

        if (rb != null)
        {
            rb.velocity = Vector2.zero;
            rb.angularVelocity = 0f;
            rb.bodyType = RigidbodyType2D.Kinematic;
        }

        if (carCollider != null)
            carCollider.isTrigger = true;
    }

    void StopHolding()
    {
        isHolding = false;
        if (rb != null) rb.bodyType = RigidbodyType2D.Dynamic;
        if (carCollider != null)
        {
            carCollider.isTrigger = false;
            carCollider.enabled = true;
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
}