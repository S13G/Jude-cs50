document.addEventListener("DOMContentLoaded", function(){
    const form = document.querySelector("form");
    const username = document.querySelector('#username')
    const password = document.querySelector('#password')
    const errorName = document.querySelector('.error-name');
    const errorPassword = document.querySelector('.error-password');
    username.onkeyup = function(){
        errorName.classList.remove('show')
    }
    password.onkeyup = function(){
        errorPassword.classList.remove('show');
    }
    form.addEventListener('submit', (e)=>{
        if(username.value == '' && password.value == ''){
            e.preventDefault();
            errorName.classList.add('show')
            errorPassword.innerHTML = "Password cannot be empty";
            errorPassword.classList.add('show');
        }else if(username.value == ""){
            e.preventDefault();
            errorName.classList.add('show')
        }else if(password.value == ''){
            e.preventDefault();
            errorPassword.innerHTML = "Password cannot be empty";
            errorPassword.classList.add('show');
        }else if(password.value.length < 8){
            e.preventDefault();
            errorPassword.innerHTML = `${password.value.length}chars Too weak: Min is 8chars`;
            errorPassword.classList.add('show');
        }else{
            document.querySelectorAll('.error').forEach(error =>{
                error.classList.remove('show');
            })
        }
    })
})
