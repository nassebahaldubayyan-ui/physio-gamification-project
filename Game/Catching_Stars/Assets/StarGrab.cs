using UnityEngine;

public class StarGrab : MonoBehaviour
{
    private bool isHolding = false;
    private bool handClosed = false;
    private Transform handPoint;
    private CircleCollider2D starCollider;
    private Transform bagTransform;

    void Start()
    {
        starCollider = GetComponent<CircleCollider2D>();
        if (starCollider == null)
            starCollider = gameObject.AddComponent<CircleCollider2D>();

        // البحث عن اليد والشنطة
        GameObject hand = GameObject.FindGameObjectWithTag("Hand");
        if (hand != null) handPoint = hand.transform;

        GameObject bag = GameObject.FindGameObjectWithTag("Bag");
        if (bag != null) bagTransform = bag.transform;
    }

    void Update()
    {
        if (handPoint == null) return;

        float distanceToHand = Vector2.Distance(transform.position, handPoint.position);

        // حالة 1: اليد قبضت والنجمة قريبة → أمسك
        if (handClosed && distanceToHand < 1.5f && !isHolding)
        {
            isHolding = true;
            if (starCollider != null) starCollider.enabled = false;
        }

        // حالة 2: اليد فتحت والنجمة ممسوكة → حاول الإيداع
        if (!handClosed && isHolding)
        {
            isHolding = false;
            if (starCollider != null) starCollider.enabled = true;

            // تحقق إذا كانت فوق الشنطة
            if (IsOverBag())
            {
                GameManager.Instance.AddScore(10);
                Destroy(gameObject);
            }
        }

        // تحريك النجمة مع اليد
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

    bool IsOverBag()
    {
        if (bagTransform == null) return false;
        return Vector2.Distance(transform.position, bagTransform.position) < 2.0f;
    }
}