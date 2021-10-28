// VARS
const resetButton = document.getElementById('reset_btn');
const saveButton = document.getElementById('submit');
const words = document.querySelectorAll('span');
const words_list = document.getElementById('words_list');
const initJson = document.getElementById('init-json');
const tag_selector = document.getElementById('ner_tag');
console.log('initJson:')
console.log(initJson)
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
                duration: 5000,
                close: true,
                gravity: "top",
                position: "left",
                backgroundColor: "white",
                boxShadow: "box-shadow: inset 5px 6px 14px 0 rgba(0,0,0,0.34)",
                stopOnFocus: false,
                onClick: function () {
                } // Callback after click
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

    let tempNer = document.getElementsByClassName("ner-temporary")
    tempNer[0].outerHTML = tempNer[0].innerHTML
    console.log(tempNer)
}

function saveButtonOnClick(file_id, page_id) {
    // send json containing taggedWordArray to api
    let nerTag = document.getElementById('ner_tag').value;
    let finalJSON = {
        file_id: file_id,
        page_id: page_id,
        ner_tag: nerTag,
        words: taggedWordArray,
    }
    console.log(taggedWordArray)
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

    words_list.textContent = "empty";
    taggedWordArray = []
    taggedWords = []

    let savedNer = document.getElementsByClassName("ner-temporary")[0]
    savedNer.classList.remove('ner-temporary')
}

function wrap_id(ids, tag) {
    if (Array.isArray(ids) && ids.length > 1) {
        let word = document.querySelector('#w' + ids[0])
        let wrapper = document.createElement('span')
        wrapper.classList.add('ner-tag', 'ner-' + tag.toLowerCase())
        word.parentNode.insertBefore(wrapper, word)


        for (let i = ids[0]; i <= ids[ids.length - 1]; i++) {
            wrapper.appendChild(document.querySelector('#w' + i))
        }
    }
}

function temp_wrap_ids(tagged_ids) {
    let is_tagged = taggedWordArray.length > 1;
    let wrapper = null;

    if (!is_tagged) {
        debugger
        let word = document.querySelector('#w' + tagged_ids[0])
        wrapper = document.createElement('span')
        wrapper.classList.add('ner-tag', 'ner-temporary')
        word.parentNode.insertBefore(wrapper, word)
    } else {
        wrapper = document.querySelector('span.ner-temporary')
    }

    for (let i = Math.min(...tagged_ids); i <= Math.max(...tagged_ids); i++) {
        wrapper.appendChild(document.querySelector('#w' + i))
        wrapper.appendChild(document.createTextNode (" "))
    }
}

function assign_tag() {
    let ner_selected = tag_selector.value;
    let ner_tag = document.querySelector(".ner-temporary")
    ner_tag.className = '';
    ner_tag.classList.add("ner-tag", 'ner-' + ner_selected, 'ner-temporary')
}

function initTags(initJsonSelector) {
    console.log('inittags')
    let tags = JSON.parse(initJsonSelector.innerHTML)
    console.log(tags)
    tags.forEach((words) => {
        console.log(words)
        if (words.keys.length > 1) {
            wrap_id(words.keys, words.value)
        } else {
            wrap_id([words.keys[0], words.keys[0]], words.value)
        }
    })
}

function preSelectWord(element) {
    let ids = taggedWordArray.map(word => word.id);
    Math.min(...ids)
    temp_wrap_ids([Math.min(...ids), Math.max(...ids)], '')
}

// EVENT LISTENERS
resetButton.addEventListener('click', resetButtonOnClick);
//saveButton.addEventListener('click', saveButtonOnClick);
tag_selector.addEventListener('change', assign_tag);

for (let i = 0; i < words.length; i++) {
    words[i].addEventListener('click', function () {
        updateWordsList({
            id: this.id.split("w")[1],
            content: this.textContent
        })

        preSelectWord(this)

    });
}

initTags(initJson)