using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DragBall : MonoBehaviour
{
    private Vector3 offset;
    private bool isDragging = false;
    private Vector3 startPos;
    private bool isPlaced = false;
    private Rigidbody2D rb;

    void Start()
    {
        startPos = transform.position;
        rb = GetComponent<Rigidbody2D>();
    }

    void OnMouseDown()
    {
        if (isPlaced) return;

        offset = transform.position - GetMouseWorldPos();
        isDragging = true;
    }

    void OnMouseUp()
    {
        isDragging = false;
    }

    void Update()
    {
        if (isDragging)
        {
            transform.position = GetMouseWorldPos() + offset;
        }
    }

    Vector3 GetMouseWorldPos()
    {
        Vector3 mousePoint = Input.mousePosition;
        mousePoint.z = 10f;
        return Camera.main.ScreenToWorldPoint(mousePoint);
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (isPlaced) return;

        if (gameObject.tag == "Red" && other.tag == "RedBox")
        {
            CorrectMatch(other.transform);
        }
        else if (gameObject.tag == "Pink" && other.tag == "PinkBox")
        {
            CorrectMatch(other.transform);
        }
        else if (gameObject.tag == "Yellow" && other.tag == "YellowBox")
        {
            CorrectMatch(other.transform);
        }
        else if (other.CompareTag("RedBox") ||
                 other.CompareTag("PinkBox") ||
                 other.CompareTag("YellowBox"))
        {
            
            transform.position = startPos;
        }


    }
    void CorrectMatch(Transform box)
    {
        isPlaced = true;
        isDragging = false;

        rb.velocity = Vector2.zero;
        rb.bodyType = RigidbodyType2D.Kinematic;

        transform.SetParent(box);

        BoxStack stack = box.GetComponent<BoxStack>();
        if (stack != null)
        {
            transform.position = stack.GetNextPosition();
        }
        else
        {
            transform.position = box.position;
        }

        GameManager.instance.AddScore(1);
    }
}
