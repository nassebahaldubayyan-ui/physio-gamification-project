using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    private bool isDragging = false;
    private HandController handController;
    private SpriteRenderer spriteRenderer;
    public ColorType color;

    void Start()
    {
        handController = HandController.Instance;
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    void Update()
    {
        if (handController == null) return;
        if (!handController.IsGameRunning()) return;

        Vector3 handPos = handController.GetHandWorldPosition();
        bool isPinching = handController.IsPinching();

        // طباعة المسافة فقط عندما تحاول الإمساك (لتجنب زحمة الـ Console)
        if (isPinching)
        {
            float dist = Vector3.Distance(handPos, transform.position);
            Debug.Log($"Hand at: {handPos} | Car at: {transform.position} | Distance: {dist}");
        }

        if (isPinching && !isDragging)
        {
            float distance = Vector3.Distance(handPos, transform.position);

            if (distance < 3.5f && handController.IsPinching())
            {
                isDragging = true;
                if (spriteRenderer != null)
                    spriteRenderer.color = Color.yellow;
            }
        }
        else if (isDragging && isPinching)
        {
            // جعل السيارة تتبع اليد مباشرة
            transform.position = new Vector3(handPos.x, handPos.y, 0f);
        }
        else if (isDragging && !isPinching)
        {
            isDragging = false;
            if (spriteRenderer != null)
                spriteRenderer.color = Color.white;
        }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (isDragging) return;

        Basket basket = other.GetComponent<Basket>();
        if (basket != null && basket.color == color)
        {
            GameManager.instance.AddScore(10);
            Destroy(gameObject);
        }
    }
}