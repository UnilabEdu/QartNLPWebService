// lemmatization demo
const btn = document.getElementById('analyze-button')
const grammarSection = document.getElementById('analyze-section')
const clearText = document.getElementById('analyze-text')
const grammarText = document.getElementById('prtext')
if (btn) {
  btn.addEventListener('click', () => {
    if (clearText.innerText === 'გაანალიზე') {
      if (grammarText.value.trim().length === 0) {
        alert('გთხოვთ, შეიყვანეთ ტექსტი.')
      } else {

        displayLemmatizedData(grammarText.value.trim())


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
      let allResultDivs = document.querySelectorAll('.grammar-block')
      let allResultTexts = document.querySelectorAll('.gram-textarea')

      for (let elem in allResultDivs) {
          elem.remove()
      }
      for (let elem in allResultTexts) {
          elem.remove()
      }

    }
  })
}


async function requestLemmatization(text) {
    let options = {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "text": (text)
      })}
    return await fetch('api/lemma', options)
        .then(r => {return r.json() })
}

async function displayLemmatizedData(text) {
    let lemmatizedData = await requestLemmatization(text)

    const parentDiv = document.querySelectorAll('.grammar-blocks')[0]

    let counter = 0
    for (const [key, value] of Object.entries(lemmatizedData)) {
        console.log(key)
        console.log(value)
        counter++
        let block_to_insert = document.createElement('div')
        block_to_insert.classList.add('grammar-block')
        block_to_insert.classList.add(`block-${counter-1}`)
        parentDiv.appendChild(block_to_insert)

        let child_block_to_insert = document.createElement('div')
        child_block_to_insert.classList.add('gram-textarea')
        block_to_insert.appendChild(child_block_to_insert)
        child_block_to_insert.innerHTML = `<h2> ${key} </h2> <br> ლემმა: ${value.lemma} <br> თეგები: ${value.pos_tags}`

    }
    console.log(lemmatizedData)
}

// file search filter


const filterBtn = document.querySelector('#filter-form');

if(filterBtn){
  console.log('ძიების შედეგები')
  console.log(searchResults)



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
        if(memberInfo.id === member.id){
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
        if(e.id === x.id){
          x.classList.add('active-photo')
        }
      })
    })
  })
}