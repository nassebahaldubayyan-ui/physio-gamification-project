using UnityEngine;

public class AppleMovement : MonoBehaviour
{
    private bool isFalling = false;
    public float fallSpeed = 2.5f;
    private Vector2 startPos;
    private bool isReturning = false;
    private bool isActive = true;

    void Start()
    {
        startPos = transform.position;
    }

    void Update()
    {
        if (!isActive) return;

        if (isFalling && !isReturning)
        {
            transform.Translate(Vector2.down * fallSpeed * Time.deltaTime);

            if (transform.position.y < -5f)
            {
                ReturnToTop();
            }
        }
    }

    public void StartFalling()
    {
        if (!isActive) return;
        if (!isFalling)
        {
            isFalling = true;
            isReturning = false;
        }
    }

    public void ReturnToTop()
    {
        if (!isActive) return;
        isFalling = false;
        isReturning = true;
        float randomX = Random.Range(-6f, 6f);
        transform.position = new Vector2(randomX, startPos.y);
        isReturning = false;
    }

    public void ResetFalling()
    {
        isFalling = false;
        isReturning = false;
        transform.position = startPos;
    }

    public void Deactivate()
    {
        isActive = false;
        isFalling = false;
        StopAllCoroutines();
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (!isActive) return;

        if (other.CompareTag("Basket"))
        {
            if (GameManager.instance != null && GameManager.instance.IsGameRunning())
            {
                GameManager.instance.AddScore();
            }
            ReturnToTop();
        }
    }
}