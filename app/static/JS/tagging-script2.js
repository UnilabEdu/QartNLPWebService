// VARS
const words = document.querySelectorAll('span');
const words_list = document.getElementById('words_list');
console.log('words_list!')
console.log(words_list)

let selectedWordIDs = []
let selectedWordObjects = []
let alreadyTaggedIDs = []

for (let i = 0; i < words.length; i++) {
    words[i].addEventListener('click', () => selectWord(words[i]));
}

let wrapper = document.createElement('span')
wrapper.id = 'ner-tag-selected'
const dropdown = document.createElement('div')
dropdown.id = 'ner-dropdown'
const dropdownHelpText = document.createElement('p')
dropdownHelpText.innerText = 'Choose a Ner Type for the selection:'
dropdown.append(dropdownHelpText)
for (let nerTitle of allTypes) {
    let nerSelector = document.createElement('button')
    nerSelector.innerText = nerTitle
    nerSelector.addEventListener('click', () => applyNerTag(nerSelector))
    dropdown.append(nerSelector)
}

let deleteButton = document.createElement('button')
deleteButton.innerText = 'X'
deleteButton.classList.add('ner-tag-delete')
let timeout;

function selectWord(word) {
    let selectedWordId = parseInt(word.id.split('w')[1])
    let nextSibling = word.nextSibling

    if (alreadyTaggedIDs.includes(selectedWordId)) {
        displayDeleteButton(word)
        return;
    } else if (selectedWordIDs.includes(selectedWordId)) {
        displayDeleteButton(word, true)
        return;
    }

    if (!selectedWordIDs.length) {
        word.parentNode.insertBefore(wrapper, word)
    }

    if ( (!selectedWordIDs.length) || (Math.max(...selectedWordIDs) + 1 === selectedWordId) ) {
        wrapper.append(word, nextSibling)
    } else if (Math.min(...selectedWordIDs) - 1 === selectedWordId) {
        wrapper.prepend(word, nextSibling)
    } else {
        console.log('incorrect word selected')
        Toastify({
                text: "შემდეგი სიტყვა უნდა იყოს ან მარჯვენა ან მარხენა მეზობელი",
                duration: 5000,
                close: true,
                gravity: "left",
                position: "left",
                backgroundColor: "#525e79",
                onClick: function () {
                } // Callback after click
            }).showToast();
        return;
    }

    selectedWordIDs.push(selectedWordId)
    let wordObject = { id: selectedWordId, content: word.value }
    selectedWordObjects.push(wordObject)

    wrapper.append(dropdown)
    console.log(selectedWordIDs)
}

console.log(allTypes)


function applyNerTag(element) {
    let nerTagName = element.innerText || element.textContent
    postNerTag(nerTagName)
}

function postNerTag(nerTagName) {
    const requestBody = {
        file_id: fileID,
        page_id: pageID,
        ner_tag: nerTagName,
        words: selectedWordObjects
    }

    fetch('/api/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            let resultObject = {keys: data.words, value: data.tag_type}
            backendTags.push(resultObject)
            refreshTags()
        })
        .catch((error) => {
            console.error('Error:', error);
        })
}


function refreshTags() {
    resetEverything()

    alreadyTaggedIDs = []
    let wrapperID = 1
    for (let tagObject of backendTags) {
        alreadyTaggedIDs.push(...tagObject.keys)
        console.log('alreadyTaggedIDs')
        console.log(alreadyTaggedIDs)
        let targetWords = getWordsById(tagObject.keys)
        let targetClass = 'ner-' + tagObject.value.toLowerCase().replace(' ', '_')
        let doneWrapper = document.createElement('span')
        doneWrapper.id = 'wrapper-' + wrapperID.toString()
        wrapperID++

        doneWrapper.classList.add('ner-tag', targetClass)
        targetWords[0].parentNode.insertBefore(doneWrapper, targetWords[0])

        doneWrapper.append(...targetWords)
    }
}

refreshTags()



function resetEverything(onlyDeselect = false) {
    let allWrappers;
    if (onlyDeselect) {
        allWrappers = [document.getElementById('ner-tag-selected')]
    } else {
        allWrappers = document.querySelectorAll('.ner-tag, #ner-tag-selected')
    }
    for (let elem of allWrappers) {
        elem.replaceWith(...elem.childNodes)
    }
    deleteButton.style.display = 'none'
    selectedWordIDs = []
    selectedWordObjects = []
}


// Helpers

function getWordsById(ids) {
    const wordElements = []

    ids.sort()

    for (let id of ids) {
        let elem = document.getElementById('w' + id)
        wordElements.push(elem)
        wordElements.push(elem.nextSibling)
    }
    return wordElements
}


function displayDeleteButton(wordElement, isDeselectButton = false) {
    let handlerFuncDelete = () => deleteNerTag(wordIDs)
    let handlerFuncDeselect = () => resetEverything(true)
    deleteButton.removeEventListener('click', handlerFuncDelete)
    deleteButton.removeEventListener('click', handlerFuncDeselect)

    clearTimeout(timeout)
    deleteButton.style.display = 'inline'
    let wrapperElement = wordElement.parentNode
    let parentID = wrapperElement.id.split('-')[1]
    deleteButton.id = 'delete-btn-' + parentID
    wrapperElement.append(deleteButton)
    let wordsToDelete = wrapperElement.childNodes
    console.log('wordsToDelete')
    console.log(wordsToDelete)
    let wordIDs = []

    for (let word of wordsToDelete) {
        console.log(word.tagName)
        if (word.tagName === 'SPAN') {
            console.log('word')
            let wordID = parseInt(word.id.split('w')[1])
            wordIDs.push(wordID)
        }
    }

    timeout = setTimeout(() => deleteButton.style.display = 'none', 2000)
    if (isDeselectButton) {
        deleteButton.addEventListener('click', handlerFuncDeselect, { once: true })
    } else {
        deleteButton.addEventListener('click', handlerFuncDelete, { once: true })
    }
}

function deleteNerTag(words) {
    const requestBody = {
        file_id: fileID,
        page_id: pageID,
        word_ids: words,
        words: selectedWordObjects
    }


    console.log('delete attempted')
    console.log(words)
    fetch('/api/', {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            console.log(backendTags)
            let removedTagIndex = backendTags.findIndex( (item) => {
                console.log(item.keys.sort())
                console.log(data.words.sort())
                console.log(item.keys)
                console.log(data.words)
                console.log(item.keys.sort() === data.words.sort())
                return JSON.stringify(item.keys.sort()) === JSON.stringify(data.words.sort())
            } )
            backendTags.splice(removedTagIndex, 1)
            console.log(removedTagIndex)
            console.log(data.words)
            refreshTags()
        })
        .catch((error) => {
            console.error('Error:', error);
        })
}