using UnityEngine;

public class BagMatch : MonoBehaviour
{
    public GameManager gameManager;

    void OnTriggerEnter2D(Collider2D other)
    {
        if (gameManager == null) return;

        if (gameObject.tag == "BagRed" && other.tag == "StarRed")
        {
            gameManager.AddScore();
            Destroy(other.gameObject);
        }
        else if (gameObject.tag == "BagBlue" && other.tag == "StarBlue")
        {
            gameManager.AddScore();
            Destroy(other.gameObject);
        }
        else if (gameObject.tag == "BagYellow" && other.tag == "StarYellow")
        {
            gameManager.AddScore();
            Destroy(other.gameObject);
        }
    }
}