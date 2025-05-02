const myModal = document.getElementById('loginModal')
const myInput = document.getElementById('username')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})

const stars = document.querySelectorAll('.favourite');

for (let i = 0; i < stars.length; i++) {
  stars[i].addEventListener("click", (event) => {
    event.target.classList.remove("favourited")
  });
}
