mergeInto(LibraryManager.library, {
    SendScoreToHTML: function(score) {
        if (typeof window.UpdateScoreFromUnity === 'function')
            window.UpdateScoreFromUnity(score);
    },
    SendEndGameToHTML: function(score) {
        if (typeof window.EndGameFromUnity === 'function')
            window.EndGameFromUnity(score);
    }
});