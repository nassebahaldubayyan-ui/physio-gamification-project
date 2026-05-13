using UnityEngine;


[RequireComponent(typeof(Basket))]
public class BasketCollector : MonoBehaviour
{
    private Basket myBasket;

    void Start()
    {
        myBasket = GetComponent<Basket>();

        Collider2D col = GetComponent<Collider2D>();
        if (col == null)
            col = gameObject.AddComponent<BoxCollider2D>();
        col.isTrigger = true;
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        // نفحص لو سيارة دخلت السلة
        if (!other.CompareTag("Car")) return;

        DraggableCar car = other.GetComponent<DraggableCar>();
        if (car == null) return;

        // نقاط فقط لو السيارة ممسوكة + لون مطابق 
        if (car.IsHolding() && car.color == myBasket.color)
        {
            if (GameManager.Instance != null)
                GameManager.Instance.AddScore(1);

            Destroy(other.gameObject);
        }
    }
}
