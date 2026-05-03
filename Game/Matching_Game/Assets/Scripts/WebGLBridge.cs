using UnityEngine;
using System.Runtime.InteropServices;

public class WebGLBridge : MonoBehaviour
{
    // ============================================
    // تعريف الدوال الخارجية من JavaScript
    // ============================================

    [DllImport("__Internal")]
    private static extern void EndGameFromJS(int score, int matches);

    [DllImport("__Internal")]
    private static extern void UpdateScoreFromJS(int score);

    [DllImport("__Internal")]
    private static extern void UpdateMatchesFromJS(int matches);

    // ============================================
    // الدوال اللي تستدعيها GameManager
    // ============================================

    // هذه هي الدالة المطلوبة (SendEndGame)
    public static void SendEndGame(int score, int matches)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        EndGameFromJS(score, matches);
        Debug.Log($"WebGLBridge: SendEndGame - Score: {score}, Matches: {matches}");
#else
        Debug.Log($"Editor Mode - SendEndGame: Score: {score}, Matches: {matches}");
#endif
    }

    public static void SendResults(int score, int matches)
    {
        SendEndGame(score, matches);
    }

    public static void SendScore(int score)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        UpdateScoreFromJS(score);
        Debug.Log($"WebGLBridge: SendScore - {score}");
#endif
    }

    public static void SendMatches(int matches)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
        UpdateMatchesFromJS(matches);
        Debug.Log($"WebGLBridge: SendMatches - {matches}");
#endif
    }
}