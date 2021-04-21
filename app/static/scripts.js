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
  const divEmail = document.querySelector('.email-input');
  const divPassword = document.querySelector('.password-input');
  let inputEmail = document.forms["login"]["email"].value;
  let inputPassword = document.forms["login"]["password"].value;
  const emailContext = () => {
    if(divEmail.childNodes[3]===undefined){
      const validEdiv = document.createElement('span');
      validEdiv.classList.add('emailwarning');
      validEdiv.textContent = 'გთხოვთ შეიყვანეთ მეილი';
      divEmail.append(validEdiv);
    }
  }
  const passwordContext = () => {
    if(divPassword.childNodes[3]===undefined){
      const validPdiv = document.createElement('span');
      validPdiv.classList.add('passwordvalidation');
      validPdiv.textContent = 'გთხოვთ შეიყვანეთ პაროლი';
      divPassword.append(validPdiv);
    }
  }
  if (inputEmail == "" && inputPassword == "") {
    emailContext();
    passwordContext();
    return false;
  }else if(inputPassword == "" && inputEmail !== ""){
    if(divEmail.childNodes[3] !== undefined){
      divEmail.childNodes[3].remove();
    }
    passwordContext();
    return false;
  }else if (inputPassword !== "" && inputEmail == ""){
    emailContext()
    if(divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    return false;
  }
}
