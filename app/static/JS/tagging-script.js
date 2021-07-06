// VARS
const resetButton = document.getElementById('reset_btn');
const words = document.querySelectorAll('span');
const words_list = document.getElementById('words_list');

let taggedWordArray = [] // array of word objects
let taggedWords = [] // array of words (right block)




// FN-s
function updateWordsList() {

    let wordObject = {
        id: this.id.split("w")[1],
        content: this.textContent
    }

    let is_taggedWordArray_empty = taggedWordArray.length === 0;

    if (is_taggedWordArray_empty) {
        // just add clicked word if it's the first one;
        taggedWordArray.push(wordObject)

    } else {

        let lastWordID = taggedWordArray[taggedWordArray.length - 1].id
        let firstWordID = taggedWordArray[0].id

        let is_right_neighbor = Math.abs(parseInt(lastWordID) - parseInt(wordObject.id)) === 1
        let is_left_neighbor = Math.abs(parseInt(firstWordID) - parseInt(wordObject.id)) === 1

        if (is_right_neighbor || is_left_neighbor) {
            taggedWordArray.push(wordObject);
            taggedWordArray.sort((a, b) => a.id - b.id );
        }
    }
    updateWordListView(); // right block

    console.log(taggedWordArray)
}


function updateWordListView(){
    taggedWords = []
    for (const obj of taggedWordArray) { taggedWords.push(obj.content) }
    words_list.textContent = taggedWords.join(" ")
}

function resetButtonOnClick(){
    words_list.textContent = "empty";
}


// EVENT LISTENERS
resetButton.addEventListener('click', resetButtonOnClick);

for( let i = 0; i < words.length; i++ ){
    words[i].addEventListener('click', updateWordsList );
}
