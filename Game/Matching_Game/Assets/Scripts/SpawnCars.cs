using UnityEngine;
using System.Collections;

public class SpawnCars : MonoBehaviour
{
    [Header("Car Prefabs")]
    public GameObject redCarPrefab;
    public GameObject greenCarPrefab;
    public GameObject blueCarPrefab;

    [Header("Basket References")]
    public Transform redBasket;
    public Transform greenBasket;
    public Transform blueBasket;

    [Header("Spawn Settings")]
    public float spawnInterval = 4f;
    public float carLifeTime   = 20f;
    public float spawnX        = 10f;  // يمين الشاشة

    [Header("Movement")]
    public float carSpeed     = 1.0f;
    public float dropDistance = 2.5f;

    // ─────────────────────────────────────────────────────────
    void Start()
    {
        StartCoroutine(SpawnLoop());
    }

    IEnumerator SpawnLoop()
    {
        yield return new WaitForSeconds(0.5f);
        while (true)
        {
            SpawnRandomCar();
            yield return new WaitForSeconds(spawnInterval);
        }
    }

    // ─────────────────────────────────────────────────────────
    public void SpawnRandomCar()
    {
        int colorIndex     = Random.Range(0, 3);
        GameObject prefab  = null;
        ColorType  color   = ColorType.Red;
        Transform  basket  = null;

        switch (colorIndex)
        {
            case 0: prefab = redCarPrefab;   color = ColorType.Red;   basket = redBasket;   break;
            case 1: prefab = greenCarPrefab; color = ColorType.Green; basket = greenBasket; break;
            case 2: prefab = blueCarPrefab;  color = ColorType.Blue;  basket = blueBasket;  break;
        }

        if (prefab == null || basket == null) return;

        // ✅ السيارة تطلع في نفس Y السلة تماماً
        Vector3 spawnPos = new Vector3(spawnX, basket.position.y, 0f);

        // تحقق إذا في سيارة بنفس اللون موجودة بالفعل في نفس الصف
        if (IsColorAlreadyActive(color)) return;

        GameObject car = Instantiate(prefab, spawnPos, Quaternion.identity);
        car.tag = "Car";

        // ضع اللون
        DraggableCar dc = car.GetComponent<DraggableCar>();
        if (dc != null)
        {
            dc.color        = color;
            dc.dropDistance = dropDistance;
        }

        // Car.cs لو موجود
        Car c = car.GetComponent<Car>();
        if (c != null) c.color = color;

        // السرعة
        CarMover mover = car.GetComponent<CarMover>();
        if (mover == null) mover = car.AddComponent<CarMover>();
        mover.speed = carSpeed;

        Destroy(car, carLifeTime);
    }

    // ─────────────────────────────────────────────────────────
    // منع تكدس نفس اللون في نفس الصف
    bool IsColorAlreadyActive(ColorType color)
    {
        foreach (GameObject car in GameObject.FindGameObjectsWithTag("Car"))
        {
            DraggableCar dc = car.GetComponent<DraggableCar>();
            if (dc != null && dc.color == color) return true;
        }
        return false;
    }
}