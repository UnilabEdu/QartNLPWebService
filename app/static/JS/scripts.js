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
            btn.style.padding = "8px 42px";
            btn.classList.remove('clear-bt');
            grammarText.value= "";
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

// const submitBtn = document.querySelector('.login-btn');
// submitBtn.addEventListener('submit', event => {
//   event.preventDefault();
// });

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
    emailContext();
    if(divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    return false;
  }else{
    localStorage.setItem('loginInfo', JSON.stringify({email:inputEmail,password:inputPassword }));
    location.reload();
  }
}

const userLogged = () => {
  const userEmail = JSON.parse(localStorage.getItem('loginInfo')).email;
  const userPass = JSON.parse(localStorage.getItem('loginInfo')).password;
  const loginLogo = document.querySelector('.user-logo');
  loginLogo.src = '../assets/dif-head-logo.svg';
}

if (localStorage.loginInfo) {
  userLogged();
  loginBtn.addEventListener('click', () => {
    alert('ok');
  });
}

// const variable = JSON.parse(localStorage.getItem('loginInfo'))
// variable.email & variable.password
// ასე დაასელექთებ მეილს ან პაროლს
