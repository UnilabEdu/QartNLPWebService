console.log('noun')
console.log(grammarSearchForm['არსებითი სახელი'])

console.log('verb')
console.log(grammarSearchForm['ზმნა'])

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