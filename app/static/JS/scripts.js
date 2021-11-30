const btn = document.getElementById('analyze-button')
const grammarSection = document.getElementById('analyze-section')
const clearText = document.getElementById('analyze-text')
const grammarText = document.getElementById('prtext')
if (btn) {
  btn.addEventListener('click', () => {
    if (clearText.innerText == 'გაანალიზე') {
      if (prtext.value.trim().length == 0) {
        alert('გთხოვთ, შეიყვანეთ ტექსტი.')
      } else {
        grammarSection.classList.toggle('display-flex')
        clearText.innerText = 'გაასუფთავე'
        btn.style.background = '#707070'
      }
    } else {
      grammarSection.classList.toggle('display-flex')
      clearText.innerText = 'გაანალიზე'
      btn.style.background = '#496AC1'
      btn.classList.remove('clear-bt')
      grammarText.value = ''
    }
  })
}

const loginBtn = document.querySelector('.login')
const loginContent = document.querySelector('.login-bg')

const loginEvent = () => {
  loginContent.classList.add('active-login')
  recovPas.classList.remove('active-login')
}
loginBtn.addEventListener('click', loginEvent)

loginForm = document.querySelector('.login-btn')
loginForm.addEventListener('click', (e) => {
  e.preventDefault()
  const divEmail = document.querySelector('#email')
  const divPassword = document.querySelector('#password')
  let inputEmail = document.forms['login']['email'].value
  let inputPassword = document.forms['login']['password'].value
  
  if(divEmail.value == ''){
    document.querySelector('#email').style.border = '1px solid red'
  } else{
    document.querySelector('#email').style.border = 'none'
  }

  if(divPassword.value == ''){
    document.querySelector('#password').style.border = '1px solid red'
  } else{
    document.querySelector('#password').style.border = 'none'
  }

  if(divPassword.value !== '' && divEmail.value !== ''){
    localStorage.setItem(
      'loginInfo',
      JSON.stringify({ email: inputEmail, password: inputPassword })
    )
    location.reload()
  }
 
})

const loginLogo = document.querySelector('.user-logo')

const dropDown = () => {
  const userName = JSON.parse(localStorage.getItem('loginInfo')).email.split(
    '@'
  )[0]
  const dropdown = document.querySelector('#dropdown')
  const userInfo = document.querySelector('#user-name')
  userInfo.innerText = userName
  dropdown.classList.toggle('active-dropdown')
  loginLogo.classList.toggle('invertedLogo')
  loginBtn.classList.toggle('dropdownMargin')
}

const userLogged = () => {
  loginLogo.src = '../assets/dif-head-logo.svg'
  loginBtn.removeEventListener('click', loginEvent)
  loginLogo.addEventListener('click', dropDown)
  loginLogo.src = '../assets/profile.svg'
  loginBtn.removeEventListener('click', loginEvent)
  loginLogo.addEventListener('click', dropDown)
}

if (localStorage.loginInfo) {
  userLogged()
}

const logout = document.querySelector('#log-out')

logout.addEventListener('click', () => {
  localStorage.removeItem('loginInfo')
  location.reload()
})

const addButton = document.querySelector('#add-file')
if (addButton) {
  addButton.addEventListener('click', () => {
    window.location.href = 'add-file.html'
  })
}

const copyInp = document.querySelector('.copy-inp')
const arrowInc = document.querySelector('.arrow-increase')
const up = document.querySelector('.cont-up')
const uploadFile = document.querySelector('.upload-file')
const flName = document.querySelector('.file-name')

if (arrowInc) {
  arrowInc.addEventListener('click', () => {
    if (!copyInp.classList.contains('active-textarea')) {
      if (flName.textContent == '') {
        copyInp.style.height = '352px'
        arrowInc.style.transform = 'rotate(270deg)'
        up.style.display = 'none'
        uploadFile.style.display = 'none'
        copyInp.classList.add('active-textarea')
      }
    } else {
      copyInp.classList.remove('active-textarea')
      copyInp.style.height = '70px'
      arrowInc.style.transform = 'rotate(0deg)'
      up.style.display = 'block'
      uploadFile.style.display = 'block'
    }
  })

  copyInp.addEventListener('click', () => {
    if (flName.textContent == '') {
      copyInp.style.height = '352px'
      arrowInc.style.transform = 'rotate(270deg)'
      up.style.display = 'none'
      uploadFile.style.display = 'none'
      copyInp.classList.add('active-textarea')
    }
  })
}

const uploadBtn = document.querySelector('#btn-upload')
if (uploadBtn) {
  const inputFile = document.querySelector('#file-input')
  const copyHead = document.querySelector('#copy-text-head')
  const copyCont = document.querySelector('.copy-container')
  uploadBtn.addEventListener('click', () => {
    inputFile.classList.toggle('display-block')
  })
  inputFile.onchange = () => {
    copyHead.style.display = 'none'
    copyCont.style.display = 'none'
  }
}
const regButton = document.querySelector('.registration-button')
const login = document.querySelector('.login-content')
const registration = document.querySelector('.registration-content')
const logBtn = document.querySelector('.avtorization-button')

regButton.addEventListener('click', () => {
  login.classList.add('invisible')
  registration.classList.remove('invisible')
  registration.classList.add('visible')
})

logBtn.addEventListener('click', () => {
  registration.classList.remove('visible')
  registration.classList.add('invisible')
  login.classList.remove('invisible')
  login.classList.add('visible')
})

const recovPas = document.querySelector('.pas-rec-bg')
const forgotBtn = document.querySelector('.forgot-password')

forgotBtn.addEventListener('click', (e) => {
  e.preventDefault()
  recovPas.classList.remove('invisible')
  recovPas.classList.add('vis')
  document.querySelector('.login-cont').classList.add('invisible')
})

if(document.querySelector('.autoriz')){
document.querySelector('.autoriz').addEventListener('click', (e)=>{
  e.preventDefault()
  recovPas.classList.add('invisible')
  recovPas.classList.remove('vis')
  document.querySelector('.login-cont').classList.remove('invisible')
})
}

window.onclick = (event) => {
  if (event.target == loginContent) {
    loginContent.classList.remove('active-login')
    recovPas.classList.add('invisible')
    recovPas.classList.remove('vis')
    login.classList.remove('invisible')
    document.querySelector('.login-cont').classList.remove('invisible')
    registration.classList.add('invisible')
    registration.classList.remove('visible')
  }
}

const regForm = document.getElementById('registration-form')

regForm.addEventListener('submit', (e) => {
  e.preventDefault()
  const divEmail = document.querySelector('.reg-email-input')
  const divPassword = document.querySelector('.reg-password-input')
  let inputEmail = document.forms['registration']['email'].value
  let inputPassword = document.forms['registration']['password'].value
  const emailContext = () => {
    if (divEmail.childNodes[3] === undefined) {
      const validEdiv = document.createElement('span')
      validEdiv.classList.add('emailwarning')
      validEdiv.textContent = 'გთხოვთ შეიყვანეთ მეილი'
      divEmail.append(validEdiv)
    }
  }
  const passwordContext = () => {
    if (divPassword.childNodes[3] === undefined) {
      const validPdiv = document.createElement('span')
      validPdiv.classList.add('passwordvalidation')
      validPdiv.textContent = 'გთხოვთ შეიყვანეთ პაროლი'
      divPassword.append(validPdiv)
    }
  }

  if(inputEmail == ''){
    document.querySelector('#reg-email').style.border = '1px solid red';
  }else{
    document.querySelector('#reg-email').style.border = 'none';
  }
  if(inputPassword == ''){
    document.querySelector('#reg-password').style.border = '1px solid red';
  }else{
    document.querySelector('#reg-password').style.border = 'none';
  }

  if(inputEmail !== '' && inputPassword !== ''){
    console.log('registration')
  }

})

const upload = document.querySelector('.btn-upload')
let fileName

if (upload) {
  upload.addEventListener('change', (item) => {
    fileName = upload.value.split('\\').slice(-1)[0]
    flName.innerHTML = fileName
    if (flName.textContent !== '') {
      copyInp.disabled = true
    }
  })
}

const hamburger = document.querySelector('.hamburger')
const navRight = document.querySelector('.nav-right')
if(hamburger){
  hamburger.addEventListener('click', () => {
    navRight.classList.toggle('show')
  })
}

//slider
const contentSlider = document.querySelector('.slider-ul');
const sliderItem = document.querySelectorAll('.slider-item');
const paginationContent = document.querySelector('.slider-pagination');

(function pagination() {
  if (sliderItem.length > 0) {
    for (var i = 0; i < sliderItem.length; i++) {
      var eFpagination = document.createElement('span')
      eFpagination.classList.add('pag-button')
      eFpagination.setAttribute('id', i)
      paginationContent.append(eFpagination)
    }
    if (eFpagination) {
      const getButtons = document.querySelectorAll('.pag-button')
      getButtons.forEach((eachBtn) => {
        if (eachBtn.id == 0) {
          eachBtn.style.background = '#496AC1'
        }
        eachBtn.addEventListener('click', () => {
          getButtons.forEach((eachBtn) => {
            eachBtn.style.background = '#fff'
          })
          eachBtn.style.background = '#496AC1'
          const x = 100 * eachBtn.id
          contentSlider.style.top = `-${x}%`
        })
      })
    }
  }
})()


//dropdown list 
const lists = document.querySelectorAll('.drop-list-li');
const dropdownMenus = document.querySelectorAll('.dropdown-categories');

lists.forEach((element)=>{
  dropdownMenus.forEach((drop)=>{
     element.addEventListener('click', ()=>{
       if(element.id === drop.id){
         drop.classList.toggle('active-menu')
         element.firstChild.nextSibling.classList.toggle('rotate')
         element.lastChild.previousSibling.classList.toggle('active-link')
       }
    })
  })
})

//copy clipboard 
const answer = document.querySelector("#copyResult");
const copy   = document.querySelectorAll("#copyButton");
const selection = window.getSelection();
const range = document.createRange();
const textToCopy = document.querySelectorAll("#textToCopy")

copy.forEach((e)=>{
  e.addEventListener('click', ()=>{
    e.classList.add('copied');
    setTimeout(()=>{
      e.classList.remove('copied');
    },2000)
    range.selectNodeContents(e.nextElementSibling);
    selection.removeAllRanges();
    selection.addRange(range);
    const successful = document.execCommand('copy');
    if(successful){
      // answer.innerHTML = 'Copied!';
    } else {
      // answer.innerHTML = 'Unable to copy!';  
    }
    window.getSelection().removeAllRanges()
  })
})


//profile-setting
const profileSettingBtn = document.querySelector('.profile-info');


if(profileSettingBtn){
  profileSettingBtn.addEventListener('click', ()=>{
    document.querySelector('.profile-setting-popup').classList.add('setting-on');
    document.body.style.overflow = 'hidden'
  }) 
}

window.onclick = (event) => {
  if (event.target == document.querySelector('.profile-setting-popup')) {
    document.querySelector('.profile-setting-popup').classList.remove('setting-on');
    document.body.style.overflow = 'auto'
  }
}

//filter
const filterBtn = document.querySelector('#filter-form');

if(filterBtn){
  filterBtn.addEventListener('click', ()=>{
    document.querySelector('.filter-form').classList.toggle('active-block');
  })

  const _metkvelebisNacili = document.querySelectorAll('.metkv-nacili');
  _metkvelebisNacili.forEach((e)=>{
    e.addEventListener('click', ()=>{
      _metkvelebisNacili.forEach((z)=>{
        if(e===z){
          z.classList.toggle('active-li')
        }else {
          z.classList.remove('active-li')
        }
      })
    })
  })
  const _tipi = document.querySelectorAll('.type');
  _tipi.forEach((e)=>{
    e.addEventListener('click', ()=>{
      _tipi.forEach((z)=>{
        if(e===z){
          z.classList.toggle('active-li')
        }else {
          z.classList.remove('active-li')
        }
      })
    })
  })
  const _suliereba = document.querySelectorAll('.sul');
  _suliereba.forEach((e)=>{
    e.addEventListener('click', ()=>{
      _suliereba.forEach((z)=>{
        if(e===z){
          z.classList.toggle('active-li')
        }else {
          z.classList.remove('active-li')
        }
      })
    })
  })  
  const _ricxvi = document.querySelectorAll('.nm');
  _ricxvi.forEach((e)=>{
    e.addEventListener('click', ()=>{
      _ricxvi.forEach((z)=>{
        if(e===z){
          z.classList.toggle('active-li')
        }else {
          z.classList.remove('active-li')
        }
      })
    })
  })  
  const _brunva = document.querySelectorAll('.brn');
  _brunva.forEach((e)=>{
    e.addEventListener('click', ()=>{
      _brunva.forEach((z)=>{
        if(e===z){
          z.classList.toggle('active-li')
        }else {
          z.classList.remove('active-li')
        }
      })
    })
  })  
}

//team members
const members = document.querySelectorAll('.team-member');
const membersInfo = document.querySelectorAll('.team-info');
const flp = document.querySelectorAll('.full-photo');

if(members){
  membersInfo.forEach(memberInfo=>{
    members.forEach(member=>{
      member.addEventListener('click', ()=>{
        if(memberInfo.id == member.id){
          memberInfo.classList.add('active-info');
        }else{
          memberInfo.classList.remove('active-info');
        }
        members.forEach(e=>{
          if(member === e){
            e.classList.add('current-member')
          }else{
            e.classList.remove('current-member')
          }
        })
      })
    })
  })

  members.forEach((e)=>{
    flp.forEach((x)=>{
      document.querySelectorAll('.close-photo').forEach(y=>{
        y.addEventListener('click', ()=>{
          x.classList.remove('active-photo')
        })
      })
      e.addEventListener('dblclick', ()=>{
        if(e.id == x.id){
          x.classList.add('active-photo')
        }
      })
    })
  })
}
