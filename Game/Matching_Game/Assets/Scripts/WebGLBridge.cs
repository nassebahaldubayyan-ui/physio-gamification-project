using UnityEngine;
using System.Runtime.InteropServices;

public class WebGLBridge : MonoBehaviour
{
    [DllImport("__Internal")]
    private static extern void UpdateScoreFromJS(int score);

    [DllImport("__Internal")]
    private static extern void UpdateMatchesFromJS(int matches);

    [DllImport("__Internal")]
    private static extern void EndGameFromJS(int score, int matches);

    // ============================================
    // دوال لإرسال البيانات إلى JavaScript
    // ============================================

    public static void SendScore(int score)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        UpdateScoreFromJS(score);
#endif
    }

    public static void SendMatches(int matches)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        UpdateMatchesFromJS(matches);
#endif
    }

    public static void SendResults(int score, int matches)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        EndGameFromJS(score, matches);
#endif
    }
}