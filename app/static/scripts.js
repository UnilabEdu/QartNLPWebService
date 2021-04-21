const btn = document.getElementById('analyze-button');
const grammarSection = document.getElementById('analyze-section');
const clearIcon = document.getElementById('clear-icon');
const clearText = document.getElementById('analyze-text');
const grammarText = document.getElementById('prtext');
if (btn){
    btn.addEventListener('click', ()=>{
        if(clearText.innerText == 'გაანალიზე'){
            if (prtext.value.trim().length == 0) {
                alert('გთხოვთ, შეიყვანეთ ტექსტი.');
            }else{
                grammarSection.classList.toggle("display-flex");
                clearText.innerText = 'გაასუფთავე';
                clearIcon.classList.toggle("display-flex");
                btn.style.background = '#707070';
                btn.style.padding = "8px";
            }
        }else{
            clearIcon.classList.toggle("display-flex");
            grammarSection.classList.toggle("display-flex");
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