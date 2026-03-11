using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class BoxStack : MonoBehaviour
{
    public float stackOffsetY = 0.5f; // المسافة بين الكور
    private int count = 0;

    public Vector3 GetNextPosition()
    {
        Vector3 pos = transform.position;
        pos.y += count * stackOffsetY;
        count++;
        return pos;
    }
}
