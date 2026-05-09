using UnityEngine;

public class CarMover : MonoBehaviour
{
    [Header("Movement")]
    public float speed = 1.5f;        // سرعة بسيطة عشان سهل سحبها
    public float despawnX = -12f;     // لو خرجت من الشاشة من اليسار → احذفها

    private DraggableCar draggable;

    void Awake()
    {
        draggable = GetComponent<DraggableCar>();
    }

    void Update()
    {
        // ⛔ لو السيارة ممسوكة باليد، توقف عن الحركة
        if (draggable != null && draggable.IsHolding())
            return;

        // ➡️ تحريك من اليمين لليسار: نقص قيمة x كل فريم
        transform.position += Vector3.left * speed * Time.deltaTime;

        // إذا طلعت من حدود الشاشة من اليسار، احذفها
        if (transform.position.x < despawnX)
        {
            Destroy(gameObject);
        }
    }
}
