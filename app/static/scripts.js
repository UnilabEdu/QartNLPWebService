const btn = document.getElementById('analyze-button');
const grammarSection = document.getElementById('analyze-section');
const clearBtn = document.getElementsByClassName('clear-btn');
btn.addEventListener('click', ()=>{
    grammarSection.classList.toggle("display-flex");
    grammarSection.classList.toggle("display-flex");
    if(btn.innerHTML == 'გაანალიზე'){
        btn.innerHTML = 'გაასუფთავე';
        btn.style.background = 'gray';
    }else{
        btn.innerHTML = 'გაანალიზე';
        btn.style.background = '#172224';
    }
});