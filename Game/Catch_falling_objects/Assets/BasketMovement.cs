using UnityEngine;

public class BasketMovement : MonoBehaviour
{
    public float speed = 1000f;

    void Update()
    {
        float move = Input.GetAxis("Horizontal");

        Vector3 pos = transform.position;
        pos.x += move * speed * Time.deltaTime;

        float screenLimit = Camera.main.orthographicSize * Camera.main.aspect;

        pos.x = Mathf.Clamp(pos.x, -screenLimit, screenLimit);

        transform.position = pos;
    }
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Egg"))
        {
            Destroy(other.gameObject);
            FindObjectOfType<GameManager>().AddScore();
        }
    }
}