document.addEventListener("DOMContentLoaded", function(){
    const icon = document.querySelector(".icon");
    const dropDown = document.querySelector(".mobile-drop-down");
    isClicked = false;
    icon.onclick = ()=>{
        icon.classList.toggle("fa-xmark");
        if(!isClicked){
            dropDown.style.display = "flex";
            isClicked = true;
        } else{
            dropDown.style.display = "none";
            isClicked = false;

        }
    }
});

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.querySelector(
          "body").style.visibility = "hidden";
        document.querySelector(
          ".spinner").style.visibility = "visible";
    } else {
        document.querySelector(
          ".spinner").style.display = "none";
        document.querySelector(
          "body").style.visibility = "visible";
    }
};
