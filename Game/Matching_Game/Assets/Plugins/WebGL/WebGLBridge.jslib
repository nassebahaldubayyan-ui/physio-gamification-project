mergeInto(LibraryManager.library, {

    EndGameFromJS: function(score, matches) {
        if (typeof window !== "undefined") {
            window.EndGameFromJS(score, matches);
        }
    },

    UpdateScoreFromJS: function(score) {
        if (typeof window !== "undefined") {
            window.UpdateScoreFromJS(score);
        }
    },

    UpdateMatchesFromJS: function(matches) {
        if (typeof window !== "undefined") {
            window.UpdateMatchesFromJS(matches);
        }
    }

});