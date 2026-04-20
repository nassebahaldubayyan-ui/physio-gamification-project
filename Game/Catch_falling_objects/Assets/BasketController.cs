using UnityEngine;

public class BasketController : MonoBehaviour
{
    public float speed = 10f;
    public float leftBound = -7f;
    public float rightBound = 7f;

    private float targetX = 0f;
    private bool hasNewData = false;
    private bool isMoving = false;

    public void SetHandPosition(string xValue)
    {
        float normalizedX = float.Parse(xValue, System.Globalization.CultureInfo.InvariantCulture);
        targetX = Mathf.Lerp(leftBound, rightBound, normalizedX);
        hasNewData = true;
    }

    public void StartMove()
    {
        Debug.Log("StartMove called");
        isMoving = true;
    }

    public void StopMove()
    {
        Debug.Log("StopMove called");
        isMoving = false;
    }

    void Update()
    {
        if (!isMoving) return;
        if (hasNewData)
        {
            Vector3 targetPos = new Vector3(targetX, transform.position.y, 0);
            transform.position = Vector3.Lerp(transform.position, targetPos, Time.deltaTime * speed);
            hasNewData = false;
        }
    }
}