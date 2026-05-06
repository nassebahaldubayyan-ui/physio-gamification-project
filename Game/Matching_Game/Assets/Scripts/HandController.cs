using UnityEngine;

public class HandController : MonoBehaviour
{
    public static HandController Instance;

    [Header("Cursor Settings")]
    public GameObject handCursor;

    [Header("Screen Mapping")]
    public float minX = -11f;
    public float maxX = 11f;
    public float minY = -6f;
    public float maxY = 6f;

    [Header("Smoothing")]
    public float smoothSpeed = 15f;

    // Internal values
    private float handX = 0.5f;
    private float handY = 0.5f;
    private bool isGripping = false;
    private bool isGameRunning = false;

    private Vector3 currentPosition;
    private Vector3 targetPosition;

    void Awake()
    {
        if (Instance == null) Instance = this;
        else Destroy(gameObject);
    }

    void Start()
    {
        if (handCursor == null)
            CreateCursor();
        
        // Initialize positions
        currentPosition = GetWorldPositionFromNormalized(0.5f, 0.5f);
        targetPosition = currentPosition;
        
        if (handCursor != null)
            handCursor.transform.position = currentPosition;
    }

    void Update()
    {
        MoveCursorSmooth();
        UpdateVisual();
    }

    // ======================================
    // 🔹 استقبال من JavaScript
    // ======================================

    public void SetHandPosition(string data)
    {
        string[] values = data.Split(',');

        if (values.Length == 2)
        {
            if (float.TryParse(values[0], out float x) &&
                float.TryParse(values[1], out float y))
            {
                handX = Mathf.Clamp01(x);
                handY = Mathf.Clamp01(y);

                // تحديث الموقع المستهدف
                targetPosition = GetWorldPositionFromNormalized(handX, handY);
                
                // Debug (اختياري)
                // Debug.Log($"Hand Position: X={handX:F2}, Y={handY:F2} → World: {targetPosition}");
            }
        }
    }

    public void SetGripState(string state)
    {
        isGripping = (state == "true" || state == "1");
        // Debug.Log($"Grip State: {isGripping}");
    }

    public void SetGameRunning(string state)
    {
        isGameRunning = (state == "1" || state == "true");
    }

    // ======================================
    // 🔹 تحويل الإحداثيات
    // ======================================

    private Vector3 GetWorldPositionFromNormalized(float x, float y)
    {
        // تحويل من (0-1) إلى (minX-maxX) و (minY-maxY)
        float worldX = Mathf.Lerp(minX, maxX, x);
        float worldY = Mathf.Lerp(minY, maxY, y);
        
        return new Vector3(worldX, worldY, 0f);
    }

    private void MoveCursorSmooth()
    {
        if (handCursor == null) return;

        // حركة سلسة
        currentPosition = Vector3.Lerp(currentPosition, targetPosition, Time.deltaTime * smoothSpeed);
        handCursor.transform.position = currentPosition;
    }

    // ======================================
    // 🔹 الشكل البصري
    // ======================================

    void UpdateVisual()
    {
        if (handCursor == null) return;

        Renderer r = handCursor.GetComponent<Renderer>();
        if (r != null)
        {
            r.material.color = isGripping ? Color.red : Color.green;
        }

        float scale = isGripping ? 0.8f : 0.5f;
        handCursor.transform.localScale = Vector3.Lerp(
            handCursor.transform.localScale,
            new Vector3(scale, scale, scale),
            Time.deltaTime * 10f
        );
    }

    void CreateCursor()
    {
        handCursor = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        handCursor.name = "HandCursor";
        handCursor.transform.localScale = Vector3.one * 0.5f;

        Renderer r = handCursor.GetComponent<Renderer>();
        if (r != null)
            r.material.color = Color.green;
        
        // إزالة الـ Collider عشان ما يتداخل مع الفيزياء
        Destroy(handCursor.GetComponent<Collider>());
    }

    // ======================================
    // 🔹 دوال عامة للاستخدام
    // ======================================

    public Vector3 GetHandWorldPosition()
    {
        // نرجع الموقع المستهدف (أو الحالي) للسيارات
        return targetPosition;
    }

    public bool IsPinching()
    {
        return isGripping;
    }

    public bool IsGameRunning()
    {
        return isGameRunning;
    }

    public float GetHandX() => handX;
    public float GetHandY() => handY;
}