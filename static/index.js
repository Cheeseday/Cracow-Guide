// const myModal = document.getElementById('myModal')
// const myInput = document.getElementById('myInput')

// myModal.addEventListener('shown.bs.modal', () => {
//   myInput.focus()
// })

const stars = document.querySelectorAll('.favourite');

for (let i = 0; i < stars.length; i++) {
  stars[i].addEventListener("click", (event) => {
    event.target.classList.toggle("favourited")
  });
}
