using UnityEngine;

public class HandController : MonoBehaviour
{
    public static HandController Instance;

    [Header("Hand Position Settings")]
    public GameObject handCursor;           // مؤشر بصري لليد (اختياري)
    public float minX = -8f;                // الحد الأيسر للشاشة
    public float maxX = 8f;                 // الحد الأيمن للشاشة
    public float minY = -4f;                // الحد السفلي
    public float maxY = 4f;                 // الحد العلوي

    [Header("Pinch Settings")]
    public float pinchThreshold = 0.05f;    // عتبة كشف حركة Pinch

    // القيم الحالية
    private float handX = 0.5f;             // 0 = يسار, 1 = يمين
    private float handY = 0.5f;             // 0 = أسفل, 1 = أعلى
    private bool isPinching = false;

    // متغيرات إضافية للـ WebGL
    private bool isGameRunning = false;

    void Awake()
    {
        // Singleton pattern
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        // إنشاء المؤشر البصري إذا لم يتم تعيينه
        if (handCursor == null)
        {
            CreateHandCursor();
        }
    }

    void CreateHandCursor()
    {
        GameObject cursor = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        cursor.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);
        cursor.name = "HandCursor";

        // تغيير لون المؤشر
        Renderer renderer = cursor.GetComponent<Renderer>();
        renderer.material.color = Color.yellow;

        handCursor = cursor;
    }

    void Update()
    {
        // تحديث موقع المؤشر البصري
        UpdateCursorVisual();
    }

    // ============================================
    // دوال تُنادى من JavaScript (WebGL)
    // ============================================

    public void SetHandPosition(string xValue)
    {
        if (float.TryParse(xValue, out float x))
        {
            handX = Mathf.Clamp01(x);
            UpdateCursorPosition();
        }
    }

    public void SetHandPositionX(string xValue)
    {
        if (float.TryParse(xValue, out float x))
        {
            handX = Mathf.Clamp01(x);
            UpdateCursorPosition();
        }
    }

    public void SetHandPositionY(string yValue)
    {
        if (float.TryParse(yValue, out float y))
        {
            handY = Mathf.Clamp01(y);
            UpdateCursorPosition();
        }
    }

    public void SetPinch(string pinchValue)
    {
        isPinching = (pinchValue == "1");
    }

    public void SetGameRunning(string running)
    {
        isGameRunning = (running == "1");
    }

    // ============================================
    // تحديث موقع المؤشر
    // ============================================

    private void UpdateCursorPosition()
    {
        if (handCursor != null)
        {
            Vector3 pos = GetHandWorldPosition();
            handCursor.transform.position = pos;
        }
    }

    private void UpdateCursorVisual()
    {
        if (handCursor != null)
        {
            // تغيير لون المؤشر عند Pinch
            Renderer renderer = handCursor.GetComponent<Renderer>();
            if (renderer != null)
            {
                renderer.material.color = isPinching ? Color.red : Color.yellow;
            }

            // تغيير الحجم عند Pinch
            float scale = isPinching ? 0.8f : 0.5f;
            handCursor.transform.localScale = new Vector3(scale, scale, scale);
        }
    }

    // ============================================
    // دوال عامة للاستخدام من سكريبتات أخرى
    // ============================================

    public Vector3 GetHandWorldPosition()
    {
        return new Vector3(
            Mathf.Lerp(minX, maxX, handX),
            Mathf.Lerp(minY, maxY, handY),
            0f
        );
    }

    public Vector2 GetHandNormalizedPosition()
    {
        return new Vector2(handX, handY);
    }

    public bool IsPinching()
    {
        return isPinching;
    }

    public float GetHandX() => handX;
    public float GetHandY() => handY;

    public bool IsGameRunning() => isGameRunning;
}