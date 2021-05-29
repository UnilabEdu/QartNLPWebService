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

const loginEvent = () =>{
  loginContent.classList.add('active-login');
}
loginBtn.addEventListener('click', loginEvent);

window.onclick = (event) => {
    if (event.target == loginContent)
        loginContent.classList.remove("active-login");
};

loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', e => {
  e.preventDefault();
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
})

const loginLogo = document.querySelector('.user-logo');

const dropDown = () =>{
  const userName = JSON.parse(localStorage.getItem('loginInfo')).email.split('@')[0];
  const dropdown = document.querySelector('#dropdown');
  const userInfo = document.querySelector('#user-name');
  userInfo.innerText = userName;
  dropdown.classList.toggle('active-dropdown');
  loginLogo.classList.toggle('invertedLogo');
  loginBtn.classList.toggle('dropdownMargin');
}

const userLogged = () => {
  loginLogo.src = '../assets/dif-head-logo.svg';
  loginBtn.removeEventListener('click', loginEvent);
  loginLogo.addEventListener('click', dropDown);
}

if (localStorage.loginInfo) {
  userLogged();
}

const logout = document.querySelector('#log-out');

logout.addEventListener('click', ()=>{
  localStorage.removeItem('loginInfo');
  location.reload();
})

const addButton = document.querySelector('#add-file');
if (addButton) {
  addButton.addEventListener('click', () => {
    window.location.href = 'add-file.html';
  });
}

const copyInp = document.querySelector('.copy-inp');
const arrowInc = document.querySelector('.arrow-increase')
const up = document.querySelector('.cont-up');
const uploadFile = document.querySelector('.upload-file');

if(arrowInc){
  arrowInc.addEventListener('click', ()=>{
    if(!copyInp.classList.contains('active-textarea')){
      copyInp.style.height = '352px';
      arrowInc.style.transform = 'rotate(270deg)';
      up.remove();
      uploadFile.innerHTML = ``;
      copyInp.classList.add('active-textarea');
    }else{
      copyInp.classList.remove('active-textarea');
      copyInp.style.height = '70px';
      arrowInc.style.transform = 'rotate(0deg)';
      uploadFile.innerHTML = `<div class="cont-up">
      <h2>ატვირთეთ ფაილი</h2>
      <button class="btn-upload">
      upload
      </button>
      </div>`
    }
  })

  copyInp.addEventListener('click', ()=>{
    copyInp.style.height = '352px';
    arrowInc.style.transform = 'rotate(270deg)';
    up.remove();
    uploadFile.innerHTML = ``;
    copyInp.classList.add('active-textarea');
  })
}