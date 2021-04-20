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
            btn.classList.add('clear-bt');
        }else{
            clearText.innerText = 'გაანალიზე';
            btn.style.background = '#172224';
            btn.classList.remove('clear-bt');
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

const validation = () => {
  let inputEmail = document.forms["login"]["email"].value;
  let inputPassword = document.forms["login"]["password"].value;
  if (inputEmail == "") {
    alert("Please enter your email");
    return false;
  }else if(inputPassword ==""){
    alert("Please enter your password");
    return false;
  }
}
