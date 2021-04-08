function analyzeButton(){
    const btn = document.getElementById('analyze-button');
    const grammarSection = document.getElementById('analyze-section');
    const clearBtn = document.getElementById('clear-icon');
    btn.addEventListener('click', ()=>{
        grammarSection.classList.toggle("display-flex");
        clearBtn.classList.toggle("display-flex");
        if(btn.innerHTML == 'გაანალიზე'){
            btn.innerHTML = 'გაასუფთავე';
            btn.style.background = '#707070';
        }else{
            btn.innerHTML = 'გაანალიზე';
            btn.style.background = '#172224';
        }
    });
}

analyzeButton();