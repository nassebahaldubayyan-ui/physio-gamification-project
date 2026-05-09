using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager instance;

    public int score = 0;
    
    public TMP_Text scoreText;
    

    public float gameTime = 60f;
    public TMP_Text timerText;

    public GameObject startPanel;
    public GameObject endPanel;

    public TMP_Text finalScoreText;
 
    private int userID = 1;

    void Awake()
    {
        if (instance == null)
            instance = this;
        else
            Destroy(gameObject);
    }

    void Start()
    {
        UpdateScoreUI();
        if (endPanel != null)
            endPanel.SetActive(false);

        // ������� userID �� Django (��� WebGL)
#if UNITY_WEBGL && !UNITY_EDITOR
        // ���� �������� �� JavaScript
#endif
    }
    public void SetUserID(int id)
    {
        userID = id;
        Debug.Log("User ID set: " + userID);
    }
     void UpdateScoreUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;
    }

    void Update()
    {
        if (Time.timeScale == 0f) return;

        gameTime -= Time.deltaTime;

        if (timerText != null)
            timerText.text = "Time: " + Mathf.Ceil(gameTime);

        if (gameTime <= 0f)
        {
            Time.timeScale = 0f;
            if (endPanel != null)
                endPanel.SetActive(true);

            // ÅÑÓÇá ÇáäÊíÌÉ ÇáäåÇÆíÉ Åáì Django
            StartCoroutine(SendFinalScoreToDjango());
        }
    }



    public void AddScore(int value)
    {
        score += value;
        
        UpdateScoreUI();
        StartCoroutine(SendScoreToDjango(score));

    }

    


    IEnumerator SendScoreToDjango(int currentScore)
    {
        string url = "http://127.0.0.1:8000/api/update-score/";
        WWWForm form = new WWWForm();
        form.AddField("score", currentScore);
        form.AddField("user_id", userID);

        using (UnityEngine.Networking.UnityWebRequest www = UnityEngine.Networking.UnityWebRequest.Post(url, form))
        {
            yield return www.SendWebRequest();
            if (www.result != UnityEngine.Networking.UnityWebRequest.Result.Success)
                Debug.LogError("Error sending score: " + www.error);
        }
    }

    IEnumerator SendFinalScoreToDjango()
    {
        string url = "http://127.0.0.1:8000/api/final-score/";
        WWWForm form = new WWWForm();
        form.AddField("final_score", score);
        form.AddField("user_id", userID);
        form.AddField("time", Mathf.Ceil(gameTime).ToString());

        using (UnityEngine.Networking.UnityWebRequest www = UnityEngine.Networking.UnityWebRequest.Post(url, form))
        {
            yield return www.SendWebRequest();
            if (www.result != UnityEngine.Networking.UnityWebRequest.Result.Success)
                Debug.LogError("Error sending final score: " + www.error);
        }
    }
}