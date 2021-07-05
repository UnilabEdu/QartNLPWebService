// SETTINGS
const debug = 1;

// VARS
const resetButton = document.getElementById('reset_btn');
const words = document.querySelectorAll('span');
const words_list = document.getElementById('words_list');

// FN-s
function clog(){
    if (debug){
        console.log(...arguments)
    }
}

const taggedWordArray = []
let taggedWords = []

function updateWordsList() {
    let wordId = this.id.split("w")[1]
    let wordContent = this.textContent


    let wordObject = {
        id: wordId,
        content: wordContent
    }

    if (taggedWordArray.length === 0) {
        taggedWordArray.push(wordObject)
    } else {
        let lastWordID = taggedWordArray[taggedWordArray.length - 1].id

        if (Math.abs(lastWordID - wordId) === 1) {
            taggedWordArray.push(wordObject)
        }

        taggedWordArray.sort(function(a, b) {
            return a.id - b.id ;
        });
    }




    console.log(taggedWordArray)
    // clog(wordObject+" has been pressed")

    getWordsFromTaggedWordArray()
    words_list.textContent = taggedWords
    console.log(taggedWordArray)
}

function getWordsFromTaggedWordArray(){
    taggedWords = []
    for (const obj of taggedWordArray) {
        taggedWords.push(obj.content)
    }
}

function resetButtonOnClick(){
    words_list.textContent = "empty";
}


// EVENT LISTENERS
resetButton.addEventListener('click', resetButtonOnClick);

for(let i = 0; i < words.length; i++){
    words[i].addEventListener('click', updateWordsList );
}
