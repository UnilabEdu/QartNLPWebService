function get_word_details(wordId) {
    let highlighted_words = document.getElementsByClassName('clicked-word')
    for (let elem of highlighted_words) {
        elem.classList.remove('clicked-word')
    }

    let wordToHighlight = document.getElementById(wordId)
    wordToHighlight.classList.add('clicked-word')

    let lemma = document.getElementById('word_lemma');
    let tag = document.getElementById('word_tag');

    let currentLemma = lemmaArray[wordId].lemma;
    let currentWordTags = lemmaArray[wordId].tags;
    if (!currentWordTags && !currentLemma) {
        lemma.innerHTML = 'სიტყვის ლემატიზაცია ვერ შესრულდა';
        tag.innerHTML = '';
    } else {
        currentWordTags = currentWordTags.split(',').join(', ');
        currentWordTags = escapeHtml(currentWordTags);
        lemma.innerHTML = `<b>ლემმა</b>: ${currentLemma}`;
        tag.innerHTML = `<b>თეგები</b>: ${currentWordTags}`;
    }
}

// utils
function escapeHtml(string)
{
    return string
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
