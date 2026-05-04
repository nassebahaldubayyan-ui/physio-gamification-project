using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;

    public int score = 0;
    public int matches = 0;           // <--  للمطابقات
    public TMP_Text scoreText;
    public TMP_Text matchesText;       

    public float gameTime = 60f;       
    public TMP_Text timerText;

    public GameObject startPanel;
    public GameObject endPanel;

    public TMP_Text finalScoreText;
    public TMP_Text finalMatchesText;   

    private bool isGameRunning = false;
    private bool gameEnded = false;

    void Awake()
    {
        if (instance == null)
            instance = this;
        else
            Destroy(gameObject);
    }

    void Update()
    {
        if (!isGameRunning) return;

        gameTime -= Time.deltaTime;

#if UNITY_WEBGL && !UNITY_EDITOR
    Application.ExternalCall("UpdateTimerFromUnity", gameTime);
#endif

        if (timerText != null)
            timerText.text = "Time: " + Mathf.Ceil(gameTime);

        if (gameTime <= 0 && !gameEnded)
        {
            EndGame();
        }
    }

    // ============================================
    // دوال تُنادى من JavaScript
    // ============================================

    public void StartGameFromHTML()
    {
        StartGame();
    }

    public void ForceEndGame()
    {
        if (!gameEnded)
            EndGame();
    }

    // ============================================
    // دوال اللعبة الأساسية
    // ============================================

    public void StartGame()
    {
        score = 0;
        matches = 0;
        gameTime = 60f;
        gameEnded = false;
        isGameRunning = true;

        if (startPanel != null)
            startPanel.SetActive(false);
        if (endPanel != null)
            endPanel.SetActive(false);

        UpdateUI();

        // إعلام HandController أن اللعبة بدأت
        if (HandController.Instance != null)
        {
#if !UNITY_EDITOR && UNITY_WEBGL
            HandController.Instance.SetGameRunning("1");
#endif
        }
    }

    public void EndGame()
    {
        if (gameEnded) return;

        isGameRunning = false;
        gameEnded = true;

        if (endPanel != null)
            endPanel.SetActive(true);

        if (finalScoreText != null)
            finalScoreText.text = "Final Score: " + score;
        if (finalMatchesText != null)
            finalMatchesText.text = "Matches: " + matches;

        // إرسال النتيجة إلى JavaScript
#if !UNITY_EDITOR && UNITY_WEBGL
        SendResultsToJS();
#endif

        // إعلام HandController أن اللعبة انتهت
        if (HandController.Instance != null)
        {
            HandController.Instance.SetGameRunning("0");
        }
    }

    public void AddScore(int value)
    {
        if (!isGameRunning) return;

        score += value;
        matches += 1;  // كل مرة نضيف سكور، يعني مطابقة صحيحة
        UpdateUI();
    }

    // للمطابقة الخاطئة
    public void AddMiss()
    {
        if (!isGameRunning) return;
        // 
    }

    private void UpdateUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;

        if (matchesText != null)
            matchesText.text = "Matches: " + matches;

#if !UNITY_EDITOR && UNITY_WEBGL
        try {
            Application.ExternalCall("UpdateScoreFromUnity", 0);
            Application.ExternalCall("UpdateTimerFromUnity", 60);
        } catch { }
#endif
    }

    // ============================================
    // إرسال النتائج إلى JavaScript
    // ============================================

    private void SendResultsToJS()
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        try
        {
            // استدعاء دوال JavaScript
            WebGLBridge.SendResults(score, matches);
        }
        catch (System.Exception e)
        {
            Debug.LogError("Error sending results to JS: " + e.Message);
        }
#endif
    }

    public bool IsGameRunning()
    {
        return isGameRunning;
    }
   
}