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

        // بدء السحب
        if (isPinching && !isDragging)
        {
            float distance = Vector3.Distance(handPos, transform.position);
            Debug.Log($"Try grab: distance={distance}");
            
            if (distance < 1.8f)
            {
                isDragging = true;
                if (spriteRenderer != null)
                    spriteRenderer.color = Color.yellow;
                Debug.Log($"✅ Grabbed car: {color}");
            }
        }
        // متابعة السحب
        else if (isDragging && isPinching)
        {
            transform.position = handPos;
        }
        // إنهاء السحب
        else if (isDragging && !isPinching)
        {
            isDragging = false;
            if (spriteRenderer != null)
                spriteRenderer.color = Color.white;
            Debug.Log($"Released car: {color}");
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