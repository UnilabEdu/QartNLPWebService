// Popup buttons
const settingsButton = document.querySelector('.profile-info')

// Popup blocks
const settingsBlock = document.querySelector('.profile-setting-popup')
const settingsSmallBlock = document.querySelector('.setting-block')

// Popup listeners
settingsButton.addEventListener('click', () => showSettingsPopup())


// Popup functions
function showSettingsPopup() {
    settingsBlock.classList.add('setting-on')
}


window.onclick = (event) => {
    console.log('here')
    console.log(settingsSmallBlock)
    console.log('event target:')
    console.log(event.target)
    console.log(settingsSmallBlock.contains(event.target))
    if (
        (settingsBlock.classList.contains('setting-on')) &&
        (event.target !== settingsButton) &&
        (!settingsSmallBlock.contains(event.target))
    ) {
        settingsBlock.classList.remove('setting-on')
    }
}
