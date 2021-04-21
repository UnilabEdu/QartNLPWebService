const btn = document.getElementById('analyze-button');
const grammarSection = document.getElementById('analyze-section');
const clearIcon = document.getElementById('clear-icon');
const clearText = document.getElementById('analyze-text');
if (btn){
    btn.addEventListener('click', ()=>{
        grammarSection.classList.toggle("display-flex");
        clearIcon.classList.toggle("display-flex");
        if(clearText.innerText == 'გაანალიზე'){
            clearText.innerText = 'გაასუფთავე';
            btn.style.background = '#707070';
            btn.style.padding = "8px";
        }else{
            clearText.innerText = 'გაანალიზე';
            btn.style.background = '#172224';
            btn.style.padding = "8px 46px";
        }
    });
}

const loginBtn = document.querySelector('.login');
const loginContent = document.querySelector('.login-bg');

loginBtn.addEventListener('click',()=>{
    loginContent.classList.add('active-login');
})

window.onclick = (event) => {
    if (event.target == loginContent) 
        loginContent.classList.remove("active-login");
};