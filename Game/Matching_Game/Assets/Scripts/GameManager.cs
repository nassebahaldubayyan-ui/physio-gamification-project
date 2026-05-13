using UnityEngine;
using TMPro;
[System.Serializable]
public class LevelConfig
{
    public int levelNumber;
    public float gameDuration;
    public int gripSensitivity;
    public string levelName;

    public float carSpeed;
    public float spawnInterval;
    public float grabDistance;
    public float dropDistance;
}
public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    public TMP_Text scoreText;
    public TMP_Text timerText;
    public GameObject endPanel;

    public float timeLeft = 60f;
    private int score = 0;
    private int userID = 1;
    private bool gameStarted = false;

    public SpawnCars spawnManager;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    void Start()
    {
        Time.timeScale = 0f;
        UpdateUI();
        if (endPanel != null)
            endPanel.SetActive(false);
    }
    // ✅ 1 — تستقبل الإعدادات من HTML قبل البدء
    public void ApplyLevelConfig(string json)
    {
        LevelConfig config = JsonUtility.FromJson<LevelConfig>(json);
        if (config == null) return;

        timeLeft = config.gameDuration;

        if (spawnManager != null)
        {
            spawnManager.ApplyLevelSettings(config);
        }

        Debug.Log($"Config applied: Level {config.levelNumber}");

        UpdateUI();
    }

    // ✅ 2 — تشغّل اللعبة من HTML
    public void StartGameFromHTML()
    {
        gameStarted = true;
        Time.timeScale = 1f;
        Debug.Log("Game started from HTML!");
    }



    public void SetUserID(int id)
    {
        userID = id;
        Debug.Log("User ID set: " + userID);
    }

    void Update()
    {
        if (!gameStarted || Time.timeScale == 0f) return;

        timeLeft -= Time.deltaTime;

        if (timerText != null)
            timerText.text = "Time: " + Mathf.Ceil(timeLeft);

        // ✅ أبلغ HTML بالتايمر
#if UNITY_WEBGL && !UNITY_EDITOR
    SendTimerToHTML(timeLeft);
#endif

        if (timeLeft <= 0f)
        {
            timeLeft = 0f;
            gameStarted = false;
            Time.timeScale = 0f;

#if UNITY_WEBGL && !UNITY_EDITOR
        SendEndGameToHTML(score);
#endif

            if (endPanel != null) endPanel.SetActive(true);
        }
    }



    public void AddScore(int value)
    {
        score += value;
        UpdateUI();
        // ✅ أبلغ HTML بالسكور الجديد
#if UNITY_WEBGL && !UNITY_EDITOR
        SendScoreToHTML(score);
#endif
    }

    void UpdateUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;
    }
    // ✅ دوال التواصل مع JavaScript
    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void SendScoreToHTML(int score);

    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void SendEndGameToHTML(int score);

    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void SendTimerToHTML(float timer);
}