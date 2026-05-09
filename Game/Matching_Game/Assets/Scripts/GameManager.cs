using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    public TMP_Text scoreText;
    public TMP_Text timerText;
    public GameObject endPanel;

    public float timeLeft = 60f;
    private int score = 0;
    private int userID = 1;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    void Start()
    {
        UpdateUI();
        if (endPanel != null)
            endPanel.SetActive(false);
    }

    public void SetUserID(int id)
    {
        userID = id;
        Debug.Log("User ID set: " + userID);
    }

    void Update()
    {
        if (Time.timeScale == 0f) return;

        timeLeft -= Time.deltaTime;

        if (timerText != null)
            timerText.text = "Time: " + Mathf.Ceil(timeLeft);

        if (timeLeft <= 0f)
        {
            Time.timeScale = 0f;
            if (endPanel != null)
                endPanel.SetActive(true);
        }
    }

    public void AddScore(int value)
    {
        score += value;
        UpdateUI();
    }

    void UpdateUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;
    }
}