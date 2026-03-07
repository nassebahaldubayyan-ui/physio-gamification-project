using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    public TMP_Text scoreText;
    public TMP_Text timerText;
    public GameObject endPanel;

    public float timeLeft = 60f;
    int score = 0;

    void Start()
    {
        UpdateScoreUI();
        if (endPanel != null)
            endPanel.SetActive(false);
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

    public void AddScore()
    {
        score++;
        UpdateScoreUI();
    }

    void UpdateScoreUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;
    }
}