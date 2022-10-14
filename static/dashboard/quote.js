document.addEventListener("DOMContentLoaded", function(){
    const form = document.querySelector("form");
    const symbol = document.querySelector('#symbol')
    const errorSymbol = document.querySelector('.error-symbol');
    symbol.onkeyup = function(){
        errorSymbol.classList.remove('show')
    }
    form.addEventListener('submit', (e)=>{
        if(symbol.value == ''){
            e.preventDefault();
            errorSymbol.classList.add('show')
        }else{
            document.querySelectorAll('.error').forEach(error =>{
                error.classList.remove('show');
            })
        }
    })
})

function storeName(){
    const buyButton = document.querySelector('.quoted a button');
    const logo = document.querySelector('.row img');
    let stockLogoUrl = logo.getAttribute('src');
    let stockName = buyButton.getAttribute('data-stock');
        if(sessionStorage.getItem('stock') === null){
            sessionStorage.setItem('stock',stockName);
            sessionStorage.setItem('logo',stockLogoUrl);
        }
}

