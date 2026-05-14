using UnityEngine;
public class SpawnCars : MonoBehaviour
{
    [Header("Car Prefabs ")]
    public GameObject redCarPrefab;
    public GameObject greenCarPrefab;
    public GameObject blueCarPrefab;

    [Header("Basket References ")]
    public Transform redBasket;
    public Transform greenBasket;
    public Transform blueBasket;

    [Header("Spawn Settings")]
    public float spawnInterval = 2f;
    public float carLifeTime = 20f;

    [Header("Spawn Position")]
    public float spawnX = 0f;

    [Header("Movement Speed")]
    public float carSpeed = 1.0f;
    void Start()
    {
        InvokeRepeating("SpawnRandomCar", 0.5f, spawnInterval);
    }

    public void SpawnRandomCar()
    {
        int colorIndex = Random.Range(0, 3);
        GameObject carPrefab = null;
        ColorType chosenColor = ColorType.Red;
        Transform matchingBasket = null;

        switch (colorIndex)
        {
            case 0:
                carPrefab = redCarPrefab;
                chosenColor = ColorType.Red;
                matchingBasket = redBasket;
                break;
            case 1:
                carPrefab = greenCarPrefab;
                chosenColor = ColorType.Green;
                matchingBasket = greenBasket;
                break;
            case 2:
                carPrefab = blueCarPrefab;
                chosenColor = ColorType.Blue;
                matchingBasket = blueBasket;
                break;
        }

        if (carPrefab == null) return;

        float y = (matchingBasket != null) ? matchingBasket.position.y : 0f;
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
