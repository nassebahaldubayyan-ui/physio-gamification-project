using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;

    public int score = 0;
    public float timeLeft = 60f;

    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI timerText;

    public GameObject startPanel;
    public GameObject endPanel;
    public TextMeshProUGUI finalScoreText;

    bool gameRunning = false;

    void Awake()
    {
        instance = this;
        Time.timeScale = 0f;
        startPanel.SetActive(true);
        endPanel.SetActive(false);
    }

    void Update()
    {
        if (!gameRunning) return;

        timeLeft -= Time.deltaTime;
        timerText.text = "Time: " + Mathf.Ceil(timeLeft);

        if (timeLeft <= 0)
        {
            EndGame();
        }
    }

    public void AddScore()
    {
        score++;
        scoreText.text = "Score: " + score;
    }

    public void StartGame()
    {
        startPanel.SetActive(false);
        Time.timeScale = 1f;
        gameRunning = true;
    }

    void EndGame()
    {
        gameRunning = false;
        Time.timeScale = 0f;
        endPanel.SetActive(true);
        finalScoreText.text = "Score: " + score;
    }
}