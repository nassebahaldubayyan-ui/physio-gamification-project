using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;
    public int score = 0;
    public float timeLeft = 60f;
    public BasketController Basket;
    public AppleSpawner appleSpawner;
    private bool gameRunning = false;
    private bool gameEnded = false;

    void Awake() { instance = this; Time.timeScale = 1f; }

    void Update()
    {
        if (!gameRunning || gameEnded) return;

        timeLeft -= Time.deltaTime;

        // ≈—”«· «· «Ì„— ≈·Ï HTML ﬂ· frame (√Ê ﬂ· À«‰Ì… √›÷·)
        if (Mathf.FloorToInt(timeLeft) != Mathf.FloorToInt(timeLeft + Time.deltaTime))
        {
#if !UNITY_EDITOR && UNITY_WEBGL
            try {
                Application.ExternalCall("UpdateTimerFromUnity", Mathf.Ceil(timeLeft));
            } catch { }
#endif
        }

        if (timeLeft <= 0)
        {
            EndGame();
        }
    }

    public bool IsGameRunning()
    {
        return gameRunning && !gameEnded;
    }

    public void AddScore()
    {
        if (!gameRunning || gameEnded) return;
        score++;
#if !UNITY_EDITOR && UNITY_WEBGL
        try {
            Application.ExternalCall("UpdateScoreFromUnity", score);
        } catch { }
#endif
    }

    public void StartGameFromHTML()
    {
        Debug.Log("StartGameFromHTML called");
        if (gameRunning || gameEnded) return;

        gameRunning = true;
        gameEnded = false;
        score = 0;
        timeLeft = 60f;

#if !UNITY_EDITOR && UNITY_WEBGL
        try {
            Application.ExternalCall("UpdateScoreFromUnity", 0);
            Application.ExternalCall("UpdateTimerFromUnity", 60);
        } catch { }
#endif

        if (Basket != null) Basket.StartMove();
        if (appleSpawner != null) appleSpawner.StartSpawning();
    }

    public void ForceEndGame()
    {
        EndGame();
    }

    void EndGame()
    {
        if (gameEnded) return;

        gameEnded = true;
        gameRunning = false;

        if (Basket != null) Basket.StopMove();
        if (appleSpawner != null) appleSpawner.StopSpawning();

#if !UNITY_EDITOR && UNITY_WEBGL
        try {
            Application.ExternalCall("EndGameFromUnity", score);
        } catch { }
#endif
    }
}
