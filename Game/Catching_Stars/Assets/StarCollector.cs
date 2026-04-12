using UnityEngine;

public class StarCollector : MonoBehaviour
{
    private void OnTriggerEnter2D(Collider2D other)
    {
        //  Õﬁﬁ ≈–« «··Ì œŒ· ÂÊ ‰Ã„…
        if (other.CompareTag("Star"))
        {
            StarGrab star = other.GetComponent<StarGrab>();

            // ≈–« «·‰Ã„… „„”Êﬂ…
            if (star != null && star.IsHolding())
            {
                GameManager.Instance.AddScore(10);
                Destroy(other.gameObject);

                // ŸÂ— ‰Ã„… ÃœÌœ…
                SpawnStars spawner = FindObjectOfType<SpawnStars>();
                if (spawner != null)
                    spawner.SpawnRandomStar();
            }
        }
    }
}