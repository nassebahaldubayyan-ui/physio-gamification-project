using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class AppleSpawner : MonoBehaviour
{
    public GameObject applePrefab;
    public int numberOfApples = 15;
    public float minDistance = 1.5f;
    public float appleScale = 0.5f;
    public float growTime = 0.6f;
    public float fallDelayMin = 1.2f;
    public float fallDelayMax = 2.5f;

    public List<float> branchHeights = new List<float> { 3.5f, 2.8f, 2.0f };
    public float leftBound = -6f;
    public float rightBound = 6f;

    private List<GameObject> apples = new List<GameObject>();
    private List<bool> isFalling = new List<bool>();
    private List<bool> isGrown = new List<bool>();  
    private List<Vector2> applePositions = new List<Vector2>();
    private bool isSpawning = false;
    private Coroutine fallingCoroutine;
    private bool gameEnded = false;

    void Start() { }

    public void StartSpawning()
    {
        if (isSpawning) return;
        gameEnded = false;
        isSpawning = true;

        foreach (GameObject apple in apples)
            if (apple != null) Destroy(apple);

        apples.Clear();
        isFalling.Clear();
        isGrown.Clear(); 
        applePositions.Clear();

        SpawnApplesOnBranches();
        if (fallingCoroutine != null) StopCoroutine(fallingCoroutine);
        fallingCoroutine = StartCoroutine(ManageFalling());
    }

    public void StopSpawning()
    {
        gameEnded = true;
        isSpawning = false;
        if (fallingCoroutine != null) StopCoroutine(fallingCoroutine);

        foreach (GameObject apple in apples)
        {
            if (apple != null)
            {
                AppleMovement movement = apple.GetComponent<AppleMovement>();
                if (movement != null) movement.Deactivate();
            }
        }
        StopAllCoroutines();
    }

    void SpawnApplesOnBranches()
    {
        int applesPerBranch = Mathf.CeilToInt((float)numberOfApples / branchHeights.Count);

        foreach (float height in branchHeights)
        {
            for (int i = 0; i < applesPerBranch && apples.Count < numberOfApples; i++)
            {
                Vector2 spawnPos = GetValidPosition(height);
                applePositions.Add(spawnPos);

                GameObject newApple = Instantiate(applePrefab, spawnPos, Quaternion.identity);
                newApple.transform.localScale = Vector3.zero;

                if (newApple.GetComponent<AppleMovement>() == null)
                    newApple.AddComponent<AppleMovement>();

                apples.Add(newApple);
                isFalling.Add(false);
                isGrown.Add(false);  
                StartCoroutine(GrowApple(apples.Count - 1));
            }
        }
    }

    IEnumerator GrowApple(int index)
    {
        GameObject apple = apples[index];
        if (apple == null) yield break;

        float elapsed = 0;
        Vector3 targetScale = Vector3.one * appleScale;

        while (elapsed < growTime && apple != null && !gameEnded)
        {
            elapsed += Time.deltaTime;
            float t = elapsed / growTime;
            apple.transform.localScale = Vector3.Lerp(Vector3.zero, targetScale, t);
            yield return null;
        }

        if (apple != null && !gameEnded)
        {
            apple.transform.localScale = targetScale;
            isGrown[index] = true;  
        }
    }

    Vector2 GetValidPosition(float height)
    {
        Vector2 newPos;
        bool valid;
        int attempts = 0;

        do
        {
            valid = true;
            float randomX = Random.Range(leftBound, rightBound);
            newPos = new Vector2(randomX, height);

            foreach (Vector2 pos in applePositions)
            {
                if (Vector2.Distance(newPos, pos) < minDistance)
                {
                    valid = false;
                    break;
                }
            }

            attempts++;
            if (attempts > 200) break;
        }
        while (!valid);

        return newPos;
    }

    IEnumerator ManageFalling()
    {
        while (isSpawning && !gameEnded)
        {
            List<int> availableIndices = new List<int>();
            for (int i = 0; i < apples.Count; i++)
            {
                if (apples[i] != null && !isFalling[i] && isGrown[i])  
                    availableIndices.Add(i);
            }

            if (availableIndices.Count > 0)
            {
                int applesToFall = Random.Range(1, Mathf.Min(3, availableIndices.Count + 1));

                for (int f = 0; f < applesToFall; f++)
                {
                    int randomIndex = availableIndices[Random.Range(0, availableIndices.Count)];
                    if (!isFalling[randomIndex] && isGrown[randomIndex])
                        StartCoroutine(FallApple(randomIndex));

                    availableIndices.Remove(randomIndex);
                    if (availableIndices.Count == 0) break;
                }
            }

            float delay = Random.Range(fallDelayMin, fallDelayMax);
            yield return new WaitForSeconds(delay);
        }
    }

    IEnumerator FallApple(int index)
    {
        if (apples[index] == null || gameEnded) yield break;

        while (!isGrown[index] && !gameEnded)
        {
            yield return new WaitForSeconds(0.1f);
        }

        isFalling[index] = true;
        GameObject apple = apples[index];
        AppleMovement movement = apple.GetComponent<AppleMovement>();

        if (movement != null)
            movement.StartFalling();

        float waitTime = 0;
        float maxWaitTime = 8f;

        while (apple != null && apple.transform.position.y > -5f && waitTime < maxWaitTime && !gameEnded)
        {
            waitTime += Time.deltaTime;
            yield return null;
        }

        if (apple != null && !gameEnded)
        {
            float newHeight = branchHeights[Random.Range(0, branchHeights.Count)];
            Vector2 newPos = GetValidPosition(newHeight);

            applePositions[index] = newPos;
            apple.transform.position = newPos;
            apple.transform.localScale = Vector3.zero;
            isGrown[index] = false;  

            StartCoroutine(GrowApple(index));

            if (movement != null)
                movement.ResetFalling();

            isFalling[index] = false;
        }
    }
}