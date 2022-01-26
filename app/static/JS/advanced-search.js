'use strict'

console.log(grammarSearchForm);

const addNewSearchFormButton = document.getElementById('add-new-search');
const newSearchFormDiv = document.getElementById('new-search-form');
const addNewFormText = document.getElementById('add-new-form-text');
const createdFormsDiv = document.getElementById('block-created-forms');
const submitSearchButton = document.getElementById('submit-search-button');
const searchInput = document.getElementById('search-input');
submitSearchButton.addEventListener('click', submitSearch);
searchInput.addEventListener('input', toggleFirstFormRadius);

const saveButton = createElem('button', {
    className : 'btn-save',
    innerText : t.save,
    eventListener : ['click', saveForm]
})

let createdForms = [];


// adding a new search form, choosing parts of speech and tags
addNewSearchFormButton.addEventListener('click', () => toggleNewSearchForm());
let searchFormActive = false;
let currentPOS = null;
let currentGrammarTags = [];

function toggleNewSearchForm(editButton = false) {
    if (!searchFormActive) {
        return displayNewSearchForm(editButton);
    } else {
        return hideNewSearchForm();
    }
}

function displayNewSearchForm(editButton = false) {
    searchFormActive = true;
    let formDiv = createElem('div', {
        id : 'temporary-search-form',
        className : 'filter-form active-block',
    });
    let partOfSpeechDiv = createElem('div', {
        innerHTML : `<h2>${t.choosePartOfSpeech}</h2>`
    });

    for (const [key, value] of Object.entries(grammarSearchForm)) {
        let listElem = createElem('li', {
            id : value.short_name,
            innerText : key
        });
        listElem.addEventListener('click', () => displayGrammarTags(key, listElem, formDiv));
        partOfSpeechDiv.appendChild(listElem);
    }
    formDiv.appendChild(partOfSpeechDiv);
    if (editButton) {
        formDiv.appendChild(editButton);
        let formId = editButton.id.split('-')[2];
        let formElement = document.getElementById(`saved-form-${formId}`);
        formElement.insertAdjacentElement('afterend', formDiv);
    } else {
        formDiv.appendChild(saveButton);
        newSearchFormDiv.appendChild(formDiv);
    }
    addNewFormText.innerText = t.disableSearchForm;
    return formDiv;
}

function hideNewSearchForm() {
    let temporarySearchForm = document.getElementById('temporary-search-form');
    temporarySearchForm.remove();
    currentPOS = null;
    currentGrammarTags = [];
    searchFormActive = false;
    addNewFormText.innerText = t.addSearchForm;
}

function displayGrammarTags(partOfSpeech, partOfSpeechElement, formDivElement, tagsToPreselect = null) {
    currentGrammarTags = [];
    if (tagsToPreselect) currentGrammarTags = tagsToPreselect.slice();
    if (tagsToPreselect) tagsToPreselect = getTagsFromArray(tagsToPreselect);

    if ((currentPOS && currentPOS.name === partOfSpeech) && !tagsToPreselect) {
        hideGrammarTags();
    } else {
        if (currentPOS) hideGrammarTags();

        currentPOS = {'name': partOfSpeech, 'short_name': grammarSearchForm[partOfSpeech].short_name};
        partOfSpeechElement.classList.add('active-li');
        let grammarTagsDiv = createElem('div', {
            id : 'current-grammar-tags'
        });
        if (grammarSearchForm[partOfSpeech].tags.length) grammarTagsDiv.innerHTML = `<h2>${t.chooseTags}</h2>`;

        for (let item of grammarSearchForm[partOfSpeech].tags) {
            let listElem = createElem('li', {
                className : item.short_name,
                innerText : current_lang === 'ka' ? item.full_name_ge : item.full_name_en
            });
            if (tagsToPreselect && tagsToPreselect.includes(item.short_name)) {
                listElem.classList.add('active-li');
            }
            listElem.addEventListener('click', () => toggleGrammarTag(item));
            grammarTagsDiv.appendChild(listElem);
        }
        formDivElement.appendChild(grammarTagsDiv);
    }
}

function hideGrammarTags() {
    let activePOS = document.getElementById(currentPOS.short_name);
    let currentGrammarTagsDiv = document.getElementById('current-grammar-tags');
    activePOS.classList.remove('active-li');
    currentPOS = null;
    currentGrammarTagsDiv.remove();
}

function toggleGrammarTag(tag) {
    let tagElem = document.getElementsByClassName(tag.short_name)[0];
    let selectedTags = getTagsFromArray(currentGrammarTags);

    if (selectedTags.includes(tag.short_name)) {
        tagElem.classList.remove('active-li');
        currentGrammarTags.splice(selectedTags.indexOf(tag.short_name), 1);
    } else {
        tagElem.classList.add('active-li');
        currentGrammarTags.push({
                                 tag: tag.short_name,
                                 name: current_lang === 'ka' ? tag.full_name_ge : tag.full_name_en
        });
    }
}


// saving a form with chosen data and displaying it
function saveForm() {
    if (!currentPOS) {
        alert(t.choosePartOfSpeechToAddForm)
    } else {
        let tags = currentGrammarTags.slice()
        let partOfSpeech = { tag: currentPOS.short_name, name: currentPOS.name }
        new Form(createdForms.length + 1, tags, partOfSpeech, createdForms.length)
        hideNewSearchForm()
    }
}

function displayForm(form, update = false) {
    let id = form.id;
    let tagNames = getNamesFromArray(form.tags);
    let tagsString = `<b>${form.partOfSpeech.name}</b> ${tagNames.slice().join(', ')}`;
    let parentDiv =      createElem('div',    { id : `saved-form-${id}`, className : 'block-content' });
    let textContentDiv = createElem('div',    { className : 'block-txt-content' });
    let text =           createElem('p',      { innerHTML : tagsString });
    let editFormDiv =    createElem('div',    { id : `form-edit-${id}`,  className: 'f-btn'});
    let editFormText =   createElem('span',   { innerText: t.editForm});
    let editFormImage =  createElem('img',    { className: 'filter', src: filterSvgUrl});
    let numsDiv =        createElem('div',    { id : `nums-div-${id}`,   className : 'nums' });
    let numMinusButton = createElem('button', { id : `btn-minus-${id}`,  className : 'minus-btn' });
    let numNumberDiv =   createElem('div',    { id : `radius-${id}`,     className : 'num', innerText : form.radius } );
    let numPlusButton =  createElem('button', { id : `btn-plus-${id}`,   className : 'pls-btn'} );

    numsDiv.appendChild(numMinusButton);
    numsDiv.appendChild(numNumberDiv);
    numsDiv.appendChild(numPlusButton);
    parentDiv.appendChild(numsDiv);

    numMinusButton.addEventListener('click', () => form.changeRadius(-1));
    numPlusButton.addEventListener('click', () => form.changeRadius(1));

    if (form.radius === '') {
        numsDiv.classList.add('invisible');
        textContentDiv.classList.add('align-to-right');
    }

    editFormDiv.appendChild(editFormText);
    editFormDiv.appendChild(editFormImage);
    textContentDiv.appendChild(text);
    textContentDiv.appendChild(editFormDiv);

    parentDiv.appendChild(textContentDiv);

    editFormDiv.addEventListener('click', () => form.displayEditForm());

    if (update) {
        return parentDiv;
    } else {
        createdFormsDiv.appendChild(parentDiv);
    }
}


class Form {
    constructor(id, tags, partOfSpeech, radius) {
        createdForms.push(this);
        if (!radius && searchInput.value) radius = 1;
        this.id = id;
        this.tags = tags;
        this.partOfSpeech = partOfSpeech;
        this.radius = radius || '';
        this.editButton = createEditButton(id - 1);
        displayForm(this);
    }
    changeRadius(amount) {
        this.radius = this.radius + amount;
        if (this.radius < 1) this.radius = 1;
        let radiusDiv = document.getElementById(`radius-${this.id}`);
        radiusDiv.innerText = this.radius;
    }
    displayEditForm() {
        let editForm = toggleNewSearchForm(this.editButton);
        if (editForm) {
            let partOfSpeechElement = document.getElementById(this.partOfSpeech.tag);
            let selectedTags = this.tags;

            currentGrammarTags = this.tags.slice();
            displayGrammarTags(this.partOfSpeech.name, partOfSpeechElement, editForm, selectedTags);
        }
    }
    update(partOfSpeech, tags) {
        if (!partOfSpeech) {
            this.delete();
        } else {
            this.tags = tags;
            this.partOfSpeech = {tag: partOfSpeech.short_name, name: partOfSpeech.name};
            let previousFormDiv = document.getElementById(`saved-form-${this.id}`);
            let newFormDiv = displayForm(this, true);
            createdFormsDiv.replaceChild(newFormDiv, previousFormDiv);
        }
        hideNewSearchForm();
    }
    delete() {
        let savedFormDiv = document.getElementById(`saved-form-${this.id}`);
        savedFormDiv.remove();
        createdForms = createdForms.filter( form => form !== this );
        alert(t.emptyFormHasBeenRemoved);
        if (createdForms && !searchInput.value) {
            let firstFormNumDiv = document.getElementsByClassName('nums')[0];
            let firstFormRadius = document.getElementsByClassName('num')[0];
            firstFormNumDiv.classList.add('invisible');
            firstFormNumDiv.nextElementSibling.classList.add('align-to-right');
            createdForms[0].radius = '';
            firstFormRadius.innerText = '';
        }
    }
    getQuery() {
        let tags = getTagsFromArray(this.tags);
        let tagsString = tags.join(',');

        let radius;
        if (this.radius) { radius = this.radius.toString() + ',' }
        else radius = '';

        let comma;
        if (tagsString) { comma = ',' }
        else comma = '';

        return `${radius}${this.partOfSpeech.tag}${comma}${tagsString}`
    }
}


// executing search
function submitSearch() {
    if (!createdForms) {
        alert(t.useSearchFormsToInitiateSearch);
    } else {
        let query = '';
        if (searchInput.value) {
            query = `"` + searchInput.value + `"_`
        }

        for (const form of createdForms) {
            query += form.getQuery() + '_';
        }
        query = query.slice(0, -1);

        query = encodeURIComponent(query);

        window.location.href = searchFormUrl + `?query=${query}`;
    }
}

// recover forms from sent query
function recoverForms(query) {
    let allFormQueries = query.split('_');
    if (allFormQueries[0].charAt(0) === `"` && allFormQueries[0].charAt(allFormQueries[0].length-1) === `"`) {
        searchInput.value = allFormQueries[0].slice(1, -1);
        allFormQueries = allFormQueries.slice(1);
    }

    for (const formQuery of allFormQueries) {
        let allTags = formQuery.split(',');
        let radius;
        if (isNaN(parseInt(allTags[0]))) {
            radius = '';
        } else {
            radius = allTags[0];
            allTags = allTags.slice(1);
        }

        let partOfSpeechTag = allTags[0];
        allTags = allTags.slice(1);

        let foundPartOfSpeech = Object.entries(grammarSearchForm).filter( (obj) => obj[1].short_name === partOfSpeechTag )[0];
        let partOfSpeech = { tag: foundPartOfSpeech[1].short_name, name: foundPartOfSpeech[0] };

        let tags = foundPartOfSpeech[1].tags.filter( item => allTags.includes(item.short_name) );
        tags = tags.map( item => ({
            tag: item.short_name,
            name: current_lang === 'ka' ? item.full_name_ge : item.full_name_en
        }) );

        new Form(createdForms.length + 1, tags, partOfSpeech, parseInt(radius));
    }
}

// the first form radius should be unavailable unless there's a text query
function toggleFirstFormRadius() {
    if (createdForms) {
        let firstFormNumDiv = document.getElementsByClassName('nums')[0];
        let firstFormRadius = document.getElementsByClassName('num')[0];


        if (searchInput.value) {
            firstFormNumDiv.classList.remove('invisible');
            firstFormNumDiv.nextElementSibling.classList.remove('align-to-right');
            createdForms[0].radius = 1;
            firstFormRadius.innerText = 1;
        } else {
            firstFormNumDiv.classList.add('invisible');
            firstFormNumDiv.nextElementSibling.classList.add('align-to-right');
            createdForms[0].radius = '';
            firstFormRadius.innerText = '';
        }
    }
}


// helpers
function createEditButton(index) {
    let button = createElem('button', {
        className : 'btn-save',
        innerText : t.update
    })
    let targetForm = createdForms[index];
    button.addEventListener('click', () => targetForm.update(currentPOS, currentGrammarTags));
    button.id = `edit-btn-${index + 1}`;
    return button;
}

function createElem(tag, args = null) {
    let elem = document.createElement(tag);

    if (args) {
        if (args.className) {
            elem.className = args.className;
        }
        if (args.id) {
            elem.id = args.id;
        }
        if (args.innerHTML) {
            elem.innerHTML = args.innerHTML;
        }
        if (args.innerText) {
            elem.innerText = args.innerText;
        }
        if (args.src) {
            elem.src = args.src;
        }
        if (args.eventListener) {
            elem.addEventListener(
                args.eventListener[0],
                args.eventListener[1]
            )
        }
    }
    return elem;
}

let getTagsFromArray = arr => arr.map(item => item.tag);

let getNamesFromArray = arr => arr.map(item => item.name);

if (sentQuery) {
    recoverForms(sentQuery);
}
