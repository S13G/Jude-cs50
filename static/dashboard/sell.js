document.addEventListener("DOMContentLoaded", function(){
    const form = document.querySelector("form");
    const symbol = document.querySelector('#symbol')
    const shares = document.querySelector('#shares')
    const errorSymbol = document.querySelector('.error-symbol');
    const errorShares = document.querySelector('.error-shares');
    let symbolValue = symbol.options[symbol.selectedIndex].value;
    symbol.onchange = function(){
        errorSymbol.classList.remove('show')
        // reassign the value of the selected option
        symbolValue = symbol.options[symbol.selectedIndex].value;
    }
    shares.onkeyup = function(){
        errorShares.classList.remove('show')
    }
    form.addEventListener('submit', (e)=>{
        if(symbol.value == '' && shares.value == ''){
            e.preventDefault();
            errorSymbol.classList.add('show');
            errorShares.classList.add('show');
        }else if(symbol.value == ''){
            e.preventDefault();
            errorSymbol.classList.add('show');
        }else if(shares.value == ''){
            e.preventDefault();
            errorShares.innerHTML = 'Invalid Shares number';
            errorShares.classList.add('show');
        }else if(shares.value <= 0){
            e.preventDefault();
            errorShares.innerHTML = 'Invalid Shares number';
            errorShares.classList.add('show');
        }else{
            document.querySelectorAll('.error').forEach(error =>{
                error.classList.remove('show');
            })
        }
    })
})
