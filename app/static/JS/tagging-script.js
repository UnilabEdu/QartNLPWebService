// VARS
const resetButton = document.getElementById('reset_btn');
const saveButton = document.getElementById('submit');
const words = document.querySelectorAll('span');
const words_list = document.getElementById('words_list');
const initJson = document.getElementById('init-json');
console.log('init_json id selected', initJson)
let taggedWordArray = [] // array of word objects
let taggedWords = [] // array of words (right block)


// FN-s
function updateWordsList(wordObject) {

    // let wordObject = {
    //     id: this.id.split("w")[1],
    //     content: this.textContent
    // }

    let is_taggedWordArray_empty = taggedWordArray.length === 0;

    if (is_taggedWordArray_empty) {
        // just add clicked word if it's the first one;
        taggedWordArray.push(wordObject)

    } else {

        let lastWordID = taggedWordArray[taggedWordArray.length - 1].id
        let firstWordID = taggedWordArray[0].id

        let is_right_neighbor = Math.abs(parseInt(lastWordID) - parseInt(wordObject.id)) === 1
        let is_left_neighbor = Math.abs(parseInt(firstWordID) - parseInt(wordObject.id)) === 1

        let is_in_array

        for (let i of taggedWordArray) {
            if (i.id === wordObject.id) {
                is_in_array = true
            }
        }

        if (!is_in_array && (is_right_neighbor || is_left_neighbor)) {
            taggedWordArray.push(wordObject);
            taggedWordArray.sort((a, b) => a.id - b.id);
        } else {
            Toastify({
              text: "შემდეგი სიტყვა უნდა იყოს ან მარჯვენა ან მარხენა მეზობელი",
              duration: 10000,
              // destination: "https://github.com/apvarun/toastify-js",  // link to plugin github page
              // newWindow: true,
              close: true,
              gravity: "top", // `top` or `bottom`
              position: "left", // `left`, `center` or `right`
              backgroundColor: "linear-gradient(to right, darkred, red)",
              stopOnFocus: true, // Prevents dismissing of toast on hover
              onClick: function(){} // Callback after click
            }).showToast();

        }
    }
    updateWordListView(); // right block

}

function updateWordListView() {
    taggedWords = []
    for (const obj of taggedWordArray) {
        taggedWords.push(obj.content)
    }
    words_list.textContent = taggedWords.join(" ")
}

function resetButtonOnClick() {
    words_list.textContent = "empty";
    taggedWordArray = []
    taggedWords = []
}

function saveButtonOnClick() {
    // send json containing taggedWordArray to api
    let nerTag = document.getElementById('ner_tag').value;
    let finalJSON = {
        file_id: 1,
        page_id: 1,
        ner_tag: nerTag,
        words: taggedWordArray,
    }
    console.log(finalJSON)
    fetch('http://127.0.0.1:5000/api/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(finalJSON)
    }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function wrap_id(ids, tag){
    if (Array.isArray(ids) && ids.length > 1){
        let word = document.querySelector('#w'+ids[0])
        let wrapper = document.createElement('span')
        wrapper.classList.add('ner-tag', 'ner-'+tag.toLowerCase())
        word.parentNode.insertBefore(wrapper,word)


        for (let i = ids[0]; i<=ids[1]; i++ ) {
            wrapper.appendChild(document.querySelector('#w'+i))
        }
    }
}

function initTags(initJsonSelector) {
    let tags = JSON.parse(initJsonSelector.innerHTML)
    tags.forEach((words) => {
        if (words.keys.length > 1) {
            wrap_id(words.keys, words.value)
        } else {
            wrap_id([words.keys[0],words.keys[0]], words.value)
        }
    })
}


// EVENT LISTENERS
resetButton.addEventListener('click', resetButtonOnClick);
saveButton.addEventListener('click', saveButtonOnClick);

for (let i = 0; i < words.length; i++) {
    words[i].addEventListener('click', function () {
        updateWordsList({
            id: this.id.split("w")[1],
            content: this.textContent
        })
    });
}

initTags(initJson)