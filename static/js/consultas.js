var formSignin = document.querySelector('#agendar')
var formSignup = document.querySelector('#desmarcar')
var btnColor = document.querySelector('.btnColor')

//deixar o botão previamente selecionado ao carregar pagina...
document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById("btnAgendar").click();
});

document.querySelector('#btnAgendar')
.addEventListener('click', () => {
    formSignin.style.left = "25px"      //valores que determinam posição do formulario ao ser selecionado pela função
    formSignup.style.left = "450px"
    btnColor.style.left = "0px"
})

document.querySelector('#btnDesmarcar')
.addEventListener('click', () => {
    formSignin.style.left = "-450px"
    formSignup.style.left = "25px"
    btnColor.style.left = "110px"
})