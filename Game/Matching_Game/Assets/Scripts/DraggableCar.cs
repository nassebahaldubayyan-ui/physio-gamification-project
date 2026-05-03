using UnityEngine;

public class DraggableCar : MonoBehaviour
{
    private bool isDragging = false;
    private Vector3 offset;
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

        // بدء السحب
        if (isPinching && !isDragging)
        {
            if (Vector3.Distance(handPos, transform.position) < 1.5f)
            {
                isDragging = true;
                offset = transform.position - handPos;
                if (spriteRenderer != null)
                    spriteRenderer.color = Color.yellow;
            }
        }
        // متابعة السحب
        else if (isDragging && isPinching)
        {
            transform.position = handPos + offset;
        }
        // إنهاء السحب
        else if (isDragging && !isPinching)
        {
            isDragging = false;
            if (spriteRenderer != null)
                spriteRenderer.color = Color.white;

            // التحقق من المطابقة (Basket هو اللي يتعامل معها)
        }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        Basket basket = other.GetComponent<Basket>();
        if (basket != null && isDragging == false)
        {
            if (basket.color == color)
            {
                GameManager.instance.AddScore(10);
                Destroy(gameObject);
            }
        }
    }
}