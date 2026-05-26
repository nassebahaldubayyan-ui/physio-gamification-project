// ============================================================
// GameManager.cs
// الإصلاحات:
//   1) ApplyLevelConfig → حذف grabDistance (لم يعد يُستخدم)
//   2) ApplyLevelConfig → dropDistance يُطبَّق على السيارات الحالية والجديدة
//   3) حذف SetUserID (ما تستخدمه HTML)
// ============================================================
using UnityEngine;
using TMPro;

[System.Serializable]
public class LevelConfig
{
    public int    levelNumber;
    public float  gameDuration;
    public int    gripSensitivity;
    public string levelName;
    public float  carSpeed;
    public float  spawnInterval;
    public float  grabDistance;   // مُرسَل من HTML لكن ما يُستخدم بعد الآن
    public float  dropDistance;
}

public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    [Header("UI References")]
    public TMP_Text    scoreText;
    public TMP_Text    timerText;
    public GameObject  endPanel;

    [Header("Game State")]
    public float timeLeft    = 60f;

    private int  score       = 0;
    private bool gameStarted = false;

    // ─────────────────────────────────────────────────────────
    void Awake()
    {
        if (Instance == null) Instance = this;
        else Destroy(gameObject);
    }

    void Start()
    {
        Time.timeScale = 0f;
        UpdateUI();
        if (endPanel != null) endPanel.SetActive(false);
    }

    // ─────────────────────────────────────────────────────────
    // يستقبل الإعدادات من HTML عبر sendMessage
    // ─────────────────────────────────────────────────────────
    public void ApplyLevelConfig(string json)
    {
        LevelConfig config = JsonUtility.FromJson<LevelConfig>(json);
        if (config == null) return;

        // ── وقت اللعبة ─────────────────────────────────────
        timeLeft = config.gameDuration;

        // ── إعدادات الـ Spawner ─────────────────────────────
        SpawnCars spawner = FindObjectOfType<SpawnCars>();
        if (spawner != null)
        {
            if (config.carSpeed     > 0) spawner.carSpeed     = config.carSpeed;
            if (config.spawnInterval > 0) spawner.spawnInterval = config.spawnInterval;
            if (config.dropDistance > 0) spawner.dropDistance = config.dropDistance;
            // السيارات الجديدة ستأخذ dropDistance تلقائياً من SpawnCars.SpawnRandomCar()
        }

        // ── طبّق dropDistance على السيارات الموجودة حالياً ─
        if (config.dropDistance > 0)
        {
            foreach (DraggableCar car in FindObjectsOfType<DraggableCar>())
                car.dropDistance = config.dropDistance;
        }

        Debug.Log($"[GameManager] Config applied: Level {config.levelNumber} | " +
                  $"Speed {config.carSpeed} | Interval {config.spawnInterval} | Drop {config.dropDistance}");
        UpdateUI();
    }

    // ─────────────────────────────────────────────────────────
    // تُنادى من HTML لبدء اللعبة
    // ─────────────────────────────────────────────────────────
    public void StartGameFromHTML()
    {
        gameStarted    = true;
        Time.timeScale = 1f;
        score          = 0;
        UpdateUI();
        Debug.Log("[GameManager] Game started!");
    }

    // ─────────────────────────────────────────────────────────
    void Update()
    {
        if (!gameStarted || Time.timeScale == 0f) return;

        timeLeft -= Time.deltaTime;

        if (timerText != null)
            timerText.text = "Time: " + Mathf.CeilToInt(timeLeft);

#if UNITY_WEBGL && !UNITY_EDITOR
        SendTimerToHTML(timeLeft);
#endif

        if (timeLeft <= 0f)
        {
            timeLeft      = 0f;
            gameStarted   = false;
            Time.timeScale = 0f;

#if UNITY_WEBGL && !UNITY_EDITOR
            SendEndGameToHTML(score);
#endif
            if (endPanel != null) endPanel.SetActive(true);
        }
    }

    // ─────────────────────────────────────────────────────────
    public void AddScore(int value)
    {
        score += value;
        UpdateUI();

#if UNITY_WEBGL && !UNITY_EDITOR
        SendScoreToHTML(score);
#endif
        Debug.Log($"[GameManager] Score: {score}");
    }

    void UpdateUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;
    }

    // ─────────────────────────────────────────────────────────
    // دوال التواصل مع HTML (WebGL فقط)
    // ─────────────────────────────────────────────────────────
    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void SendScoreToHTML(int score);

    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void SendEndGameToHTML(int score);

    [System.Runtime.InteropServices.DllImport("__Internal")]
    private static extern void SendTimerToHTML(float timer);
}