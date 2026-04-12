using UnityEngine;

public class SpawnStars : MonoBehaviour
{
    public GameObject yellowStarPrefab;

    public float spawnInterval = 2f;
    public float starLifeTime = 10f; 

    public Vector2 minPos = new Vector2(-7f, 2f);
    public Vector2 maxPos = new Vector2(7f, 5f);

    void Start()
    {
        InvokeRepeating("SpawnRandomStar", 1f, spawnInterval);
    }

    public void SpawnRandomStar()
    {
        int color = Random.Range(0, 3);
        GameObject starPrefab = yellowStarPrefab;

        
        float x = Random.Range(minPos.x, maxPos.x);
        float y = Random.Range(minPos.y, maxPos.y);

        GameObject star = Instantiate(starPrefab, new Vector3(x, y, 0), Quaternion.identity);
        Destroy(star, starLifeTime); 
    }
}
