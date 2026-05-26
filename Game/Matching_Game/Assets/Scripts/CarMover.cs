using UnityEngine;

public class CarMover : MonoBehaviour
{
    [Header("Movement")]
    public float speed = 1.5f;        
    public float despawnX = -12f;     

    private DraggableCar draggable;

    void Awake()
    {
        draggable = GetComponent<DraggableCar>();
    }

    void Update()
    {
        if (draggable != null && draggable.IsHolding())
            return;

        transform.position += Vector3.left * speed * Time.deltaTime;

        if (transform.position.x < despawnX)
        {
            Destroy(gameObject);
        }
    }
}
