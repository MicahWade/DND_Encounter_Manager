const registerSpan = document.getElementById(`registerspan`);
const firstname = document.getElementById(`firstname`);
const lastname = document.getElementById(`lastname`);


function register(){
    if(firstname.classList.contains("hidden")){
        registerToggle();
    } else {
        console.log("Not active");
    }
}
function registerToggle(){
    firstname.classList.remove("hidden");
    lastname.classList.remove("hidden");
}
function login(){

}