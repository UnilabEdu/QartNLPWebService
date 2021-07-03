console.log("looks like it's working")
var resetButton = document.getElementById('reset_btn');
var words = document.querySelectorAll('span');

var words_list = document.getElementById('words_list');

function updateWordsList(){
    text_data = " " + this.textContent

    console.log("word has been pressed")
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

resetButton.addEventListener('click', resetButtonOnClick);

for(var i = 0; i < words.length; i++){
    words[i].addEventListener('click', updateWordsList );
}
