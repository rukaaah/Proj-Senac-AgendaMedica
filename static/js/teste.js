
function crtz(){{
    data = document.getElementById("desmarcarid").value
    datae = document.getElementById("desmarcarid")

    if (data != ''){
    text = datae.options[datae.selectedIndex].text
    teste = window.confirm("Voce tem certeza que quer desmarcar "+text+"?")
    if (teste == true){
        document.getElementById('form').submit()
    }}
}}

function addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days + 1);
    year = result.getFullYear()
    month = (result.getMonth() + 1).toString().padStart(2, "0")
    day = result.getDate().toString().padStart(2, "0");
    data = (year + '-' + month + '-' + day);
    return data;
  }

function teste(){
    localStorage.clear
    datateste = document.getElementById('datahoje').value
    localStorage.setItem('data', datateste)
    data = localStorage.getItem('data')
    this.form.submit()
}
function maisdata(){
    data = localStorage.getItem('data')
    data = addDays(data, 1)
    document.getElementById('datahoje').value = data
    document.getElementById('form').submit()
    teste()
}
function menosdata(){
    data = localStorage.getItem('data')
    data = addDays(data, -1)
    document.getElementById('datahoje').value = data
    document.getElementById('form').submit()
    teste()
}

function uai(){
    data = new Date();
    year = data.getFullYear();
    month = (data.getMonth() + 1).toString().padStart(2, "0");
    day = data.getDate().toString().padStart(2, "0");
    data = (year + '-' + month + '-' + day);
    if(sessionStorage.getItem('datainicial') == '' || sessionStorage.getItem('datainicial') == null){
        document.getElementById('datahoje').value = data
        sessionStorage.setItem('datainicial', '1')
        teste()
}
}

function clickcel(id){
    idst = document.getElementById('teste'+id)
    tamanho = document.getElementById('tamanho').innerHTML
    i= 0
    while (i < tamanho){
        if (i != id){
        st = document.getElementById("teste"+i)
        st.classList.remove("hide")
        i++
        }else{
            i++
        }
    }
    if (idst.getAttribute('class') != 'obsdiv hide'){
        idst.classList.add("hide")
    }else{
        idst.classList.remove("hide")
}

}