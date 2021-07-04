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

function updateWordsList(){
    let text_data = " " + this.textContent

    clog("word has been pressed")
    if (words_list.textContent === 'empty'){
        words_list.textContent = text_data;
    }
    else{
        words_list.textContent += text_data;
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
