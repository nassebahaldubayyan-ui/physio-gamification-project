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
    public float carLifeTime = 20f;

    [Header("Spawn Position")]
    public float spawnX = 0f;

    [Header("Movement Speed")]
    public float carSpeed = 1.0f;

    void Start()
    {
        StartCoroutine(SpawnLoop());
    }

    // ← Coroutine تقرأ spawnInterval الحالية كل مرة (تدعم التعديل الديناميكي)
    IEnumerator SpawnLoop()
    {
        yield return new WaitForSeconds(0.5f);
        while (true)
        {
            SpawnRandomCar();
            yield return new WaitForSeconds(spawnInterval);
        }
    }

    public void SpawnRandomCar()
    {
        int colorIndex = Random.Range(0, 3);
        GameObject carPrefab = null;
        ColorType chosenColor = ColorType.Red;
        Transform matchingBasket = null;

        switch (colorIndex)
        {
            case 0: carPrefab = redCarPrefab;   chosenColor = ColorType.Red;   matchingBasket = redBasket;   break;
            case 1: carPrefab = greenCarPrefab; chosenColor = ColorType.Green; matchingBasket = greenBasket; break;
            case 2: carPrefab = blueCarPrefab;  chosenColor = ColorType.Blue;  matchingBasket = blueBasket;  break;
        }

        if (carPrefab == null) return;

        // إزاحة عشوائية بسيطة على Y لتجنب تكدس السيارات
        float y = (matchingBasket != null)
            ? matchingBasket.position.y + Random.Range(-0.3f, 0.3f)
            : Random.Range(-0.3f, 0.3f);

        Vector3 spawnPos = new Vector3(spawnX, y, 0);
        GameObject car = Instantiate(carPrefab, spawnPos, Quaternion.identity);
        car.tag = "Car";

        DraggableCar dc = car.GetComponent<DraggableCar>();
        if (dc != null) dc.color = chosenColor;

        Car c = car.GetComponent<Car>();
        if (c != null) c.color = chosenColor;

        CarMover mover = car.GetComponent<CarMover>();
        if (mover == null) mover = car.AddComponent<CarMover>();
        mover.speed = carSpeed;

        Destroy(car, carLifeTime);
    }
}