using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;

    public int score = 0;
    public TMP_Text scoreText;

    public float gameTime = 30f;
    public TMP_Text timerText;

    public GameObject startPanel;
    public GameObject endPanel;

    public TMP_Text finalScoreText;

    private bool isGameRunning = false;

    void Awake()
    {
        instance = this;
    }

    void Update()
    {
        if (!isGameRunning) return;

        gameTime -= Time.deltaTime;
        timerText.text = "Time: " + Mathf.Ceil(gameTime);

        if (gameTime <= 0)
        {
            EndGame();
        }
    }

    public void StartGame()
    {
        score = 0;
        gameTime = 30f;

        startPanel.SetActive(false);
        endPanel.SetActive(false);

        isGameRunning = true;
    }

    public void EndGame()
    {
        isGameRunning = false;
        endPanel.SetActive(true);

        finalScoreText.text = "Final Score: " + score;
    }

    public void AddScore(int value)
    {
        score += value;
        scoreText.text = "Score: " + score;
    }
}