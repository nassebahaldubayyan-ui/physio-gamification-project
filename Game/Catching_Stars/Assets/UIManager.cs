using UnityEngine;

public class UIManager : MonoBehaviour
{
    public GameObject startPanel;
    public GameObject endPanel;

    void Start()
    {
        Time.timeScale = 0f;      
        if (endPanel != null)
            endPanel.SetActive(false);
    }

    public void StartGame()
    {
        Debug.Log("StartGame called"); 
        if (startPanel != null)
            startPanel.SetActive(false);

        Time.timeScale = 1f;      
    }
}