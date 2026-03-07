using UnityEngine;

public class EggSpawner : MonoBehaviour
{
    public GameObject eggPrefab;
    public Transform[] spawnPoints;
    public float spawnTime = 2f;

    void Start()
    {
        InvokeRepeating(nameof(SpawnEgg), 1f, spawnTime);
    }

    void SpawnEgg()
    {
        if (Time.timeScale == 0f) return;

        int index = Random.Range(0, spawnPoints.Length);
        Instantiate(eggPrefab, spawnPoints[index].position, Quaternion.identity);
    }
}