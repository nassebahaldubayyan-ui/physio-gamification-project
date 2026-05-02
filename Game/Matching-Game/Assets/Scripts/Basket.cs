using UnityEngine;

public class Basket : MonoBehaviour
{
    public ColorType color;

    private void OnTriggerEnter2D(Collider2D other)
    {
        Debug.Log(" in ");

        Car car = other.GetComponent<Car>();

        if (car != null)
        {
            if (car.color == color)
            {
                Debug.Log("T");
                GameManager.instance.AddScore(1);
                Destroy(car.gameObject);
            }
            else
            {
                Debug.Log("FS!");
            }
        }
    }
}