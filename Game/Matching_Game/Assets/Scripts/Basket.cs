using UnityEngine;

public class Basket : MonoBehaviour
{
    public ColorType color;
    
    // ✅ أضف هذا
    private Collider2D basketCollider;

    void Start()
    {
        basketCollider = GetComponent<Collider2D>();
        if (basketCollider == null)
        {
            BoxCollider2D box = gameObject.AddComponent<BoxCollider2D>();
            basketCollider = box;
        }
        basketCollider.isTrigger = false;
    }

    // ✅ هل النقطة داخل السلة؟
    public bool ContainsPoint(Vector2 point)
    {
        if (basketCollider == null) return false;
        return basketCollider.OverlapPoint(point);
    }
}