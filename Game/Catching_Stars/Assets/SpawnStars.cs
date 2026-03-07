using UnityEngine;

public class SpawnStars : MonoBehaviour
{
    public GameObject redStarPrefab;
    public GameObject blueStarPrefab;
    public GameObject yellowStarPrefab;

    public float spawnInterval = 3f; // ßá 3 ËæÇäí äÌãÉ ÌÏíÏÉ
    public float starLifeTime = 10f; // ÊÎÊİí ÈÚÏ 10 ËæÇäí

    public Vector2 minPos = new Vector2(-7f, 2f);
    public Vector2 maxPos = new Vector2(7f, 5f);

    void Start()
    {
        InvokeRepeating("SpawnRandomStar", 1f, spawnInterval);
    }

    void SpawnRandomStar()
    {
        // ÇÎÊÑ áæä ÚÔæÇÆí ãÊæÇİŞ ãÚ ÇáÔäØ
        int color = Random.Range(0, 3);
        GameObject starPrefab = redStarPrefab;
        if (color == 1) starPrefab = blueStarPrefab;
        else if (color == 2) starPrefab = yellowStarPrefab;

        // ÇÎÊÑ ãßÇä ÚÔæÇÆí ÈÇáÓãÇÁ
        float x = Random.Range(minPos.x, maxPos.x);
        float y = Random.Range(minPos.y, maxPos.y);

        GameObject star = Instantiate(starPrefab, new Vector3(x, y, 0), Quaternion.identity);
        Destroy(star, starLifeTime); // ÊÎÊİí ÈÚÏ starLifeTime ËæÇäí
    }
}
