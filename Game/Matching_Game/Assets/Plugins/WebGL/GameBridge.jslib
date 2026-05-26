mergeInto(LibraryManager.library, {
    SendScoreToHTML: function(score) {
        if (typeof window.UpdateScoreFromUnity === 'function')
            window.UpdateScoreFromUnity(score);
    },
    SendTimerToHTML: function(timer) {
        if (typeof window.UpdateTimerFromUnity === 'function')
            window.UpdateTimerFromUnity(timer);
    },
    SendEndGameToHTML: function(score) {
        if (typeof window.EndGameFromUnity === 'function')
            window.EndGameFromUnity(score);
    }
});