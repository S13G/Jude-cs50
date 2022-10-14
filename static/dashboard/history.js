const form = document.querySelector("form");
const div = document.querySelector("main .after");
const choice = document.querySelector(".after .choice");

function showChoice(){
    div.style.visibility = 'visible';
    choice.style.transform = 'scale(1)';
    console.log(true)
}
function removeChoice(){
    div.style.visibility = 'hidden';
    choice.style.transform = 'scale(0.1)';
}
form.addEventListener('submit', (e)=>{
    showChoice();
    e.preventDefault();
    const choiceButtons = document.querySelectorAll('.choice button')
    choiceButtons.forEach((button)=>{
        button.onclick =()=>{
            if(button.value == "no"){
                removeChoice();
                e.preventDefault();
            }else{
                const input = document.querySelector('form #choice');
                input.value = 'yes';
                console.log(input.value)
                form.submit();
            }
        }
    })
})
