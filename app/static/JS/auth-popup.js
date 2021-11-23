// Popup blocks
const popupBlock = document.querySelector('.login-bg')
const loginBlock = document.querySelector('.login-content')
const registerBlock = document.querySelector('.registration-content')
const recoverBlock = document.querySelector('.pas-rec-bg')

const individualPopupBlocks = [loginBlock, registerBlock, recoverBlock]

const smallLoginBlock = document.querySelector('.login-cont')

// Auth view switch buttons
const loginButton = document.querySelector('.avtorization-button')
const registerButton = document.querySelector('.registration-button')
const recoverButton = document.querySelector('.forgot-password')
const loginButtonInRecoverForm = document.querySelector('.autoriz')

// Activate Popup buttons
const popupButtonNavbar = document.querySelector('.user-place')
const popupButtonSlider = document.getElementById('slider-auth-btn')

const allAuthNodes = [...individualPopupBlocks, popupButtonSlider, popupButtonNavbar]

// Show popup listeners
popupButtonNavbar.addEventListener('click', showPopup)
popupButtonSlider.addEventListener('click', showPopup)

// Switch auth view listeners
loginButton.addEventListener('click', () => toggleAuthForms(loginBlock))
registerButton.addEventListener('click', () => toggleAuthForms(registerBlock))
recoverButton.addEventListener('click', () => toggleAuthForms(recoverBlock, true))
loginButtonInRecoverForm.addEventListener('click', () => toggleAuthForms(loginBlock))


function showPopup() {
    popupBlock.classList.add('active-login')
}

function hidePopup() {
    popupBlock.classList.remove('active-login')
}


window.onclick = (event) => {
    let clickedAuthNode = false
    allAuthNodes.forEach(node => {
        if (node.contains(event.target)) {
            clickedAuthNode = true
        }
    })

    if (!clickedAuthNode) {
        hidePopup()
    }
}


function toggleAuthForms(formToShow, recoverForm=false) {
    smallLoginBlock.classList.toggle('visible', false)
    smallLoginBlock.classList.toggle('invisible', false)

    individualPopupBlocks.forEach(form => {
        if (recoverForm && form === loginBlock) {
            form = smallLoginBlock
        }

        form.classList.toggle('visible', false)
        form.classList.toggle('invisible', true)
    })
    let visible = recoverForm ? 'vis' : 'visible'
    formToShow.classList.toggle(visible, true)
    formToShow.classList.toggle('invisible', false)
}

// Display form on page load if a form was submitted
if (displayThisPopup) {
    let formToShow;
    let isRecoverForm = false
    switch (displayThisPopup) {
        case 'login':
            formToShow = loginBlock
            break
        case 'signup':
            formToShow = registerBlock
            break
        case 'forgot':
            formToShow = recoverBlock
            isRecoverForm = true
            break
    }
    showPopup()
    toggleAuthForms(formToShow, isRecoverForm)
}
