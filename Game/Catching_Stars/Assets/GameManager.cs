using UnityEngine;
using TMPro;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    public TMP_Text scoreText;
    public TMP_Text timerText;
    public GameObject endPanel;
    public SpawnStars starSpawner;

    public float timeLeft = 60f;
    private int score = 0;
    private int userID = 1; // ”Ì „ «” ·«„Â „‰ Django

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    void Start()
    {
        UpdateScoreUI();
        if (endPanel != null)
            endPanel.SetActive(false);

        // «” ﬁ»«· userID „‰ Django (⁄»— WebGL)
#if UNITY_WEBGL && !UNITY_EDITOR
        // ”Ì „ «” œ⁄«ƒÂ „‰ JavaScript
#endif
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

            // ≈—”«· «·‰ ÌÃ… «·‰Â«∆Ì… ≈·Ï Django
            StartCoroutine(SendFinalScoreToDjango());
        }
    }

    public void AddScore(int value)
    {
        score += value;
        UpdateScoreUI();

        // ≈—”«· ﬂ· ‰ﬁÿ… ≈·Ï Django
        StartCoroutine(SendScoreToDjango(score));
    }

    void UpdateScoreUI()
    {
        if (scoreText != null)
            scoreText.text = "Score: " + score;
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
        form.AddField("time", Mathf.Ceil(timeLeft).ToString());

        using (UnityEngine.Networking.UnityWebRequest www = UnityEngine.Networking.UnityWebRequest.Post(url, form))
        {
            yield return www.SendWebRequest();
            if (www.result != UnityEngine.Networking.UnityWebRequest.Result.Success)
                Debug.LogError("Error sending final score: " + www.error);
        }
    }
}