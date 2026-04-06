using UnityEngine;

public class StarGrab : MonoBehaviour
{
    public Transform handPoint;   // اربطيه بـ Palm Transform
    public bool handClosed;       // true = اليد قبضت النجمة

    private bool isHeld = false;

    void Update()
    {
        if (handPoint == null) return;

        // النجمة تمسك إذا اليد مقبوضة وقريبة
        if (handClosed && IsHandNear())
            isHeld = true;

        if (!handClosed)
            isHeld = false;

        // النجمة تتحرك مع اليد
        if (isHeld)
            transform.position = handPoint.position;
    }

    bool IsHandNear()
    {
        float dist = Vector2.Distance(transform.position, handPoint.position);
        return dist < 1.5f;  // المسافة المقبولة لمس اليد للنجمة
    }
}