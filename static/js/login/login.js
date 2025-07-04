const registerSpan = document.getElementById(`registerspan`);
const firstname = document.getElementById(`firstname`);
const lastname = document.getElementById(`lastname`);
const password = document.getElementById(`password`);
const email = document.getElementById(`email`);
const terms = document.getElementById('terms');
const termDiv = document.getElementById('allterms');
// Alerts
const existEmail = document.getElementById('existEmail');
const passwordAlert = document.getElementById('passwordAlert')

function register(){
    if(firstname.classList.contains("hidden")){
        registerToggle();
        return
    } 
    if (!terms.checked) {
        alert("You must agree to the terms and conditions.");
        return
    }
    if(!/^[a-zA-Z]{3,}$/.test(firstname.value)){
        alert("First name must be at least 3 letters long.")
        return
    } if(!/^[a-zA-Z]{3,}$/.test(lastname.value)){
        alert("Last name must be at least 3 letters long.")
        return
    } if(!checkPassword()){
        return
    }

    // JSON request 
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", "./register");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.withCredentials = true; // Allow cookies like a form

    xhr.onload = function() {
        if (xhr.status === 200 || xhr.status === 201) {
            try {
                const resp = JSON.parse(xhr.responseText);
                if (resp.redirect) {
                    window.location.href = resp.redirect;
                    return;
                }
            } catch (e) {
                alert("An error happend, if this persistes please contact support");
            }
        } else if (xhr.status === 409) {
            existEmail.innerHTML = "An acount exists with this Email!";
            existEmail.classList.remove("hidden");
 1       } else {
            alert("Account creation failed: " + xhr.responseText);
        }
    };
    const data = {
        firstname: firstname.value,
        lastname: lastname.value,
        email: email.value,
        password: password.value
    };
    xhr.send(JSON.stringify(data));
}
function registerToggle(){
    password.addEventListener('focusout', checkPassword);
    email.addEventListener('focusout', checkEmail);
    firstname.classList.remove("hidden");
    lastname.classList.remove("hidden");
    allterms.classList.remove("hidden");
}
function login(){
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", "./login");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.withCredentials = true; // Allow cookies like a form

    xhr.onload = function() {
        if (xhr.status === 200 || xhr.status === 201) {
            try {
                const resp = JSON.parse(xhr.responseText);
                if (resp.redirect) {
                    window.location.href = resp.redirect;
                    return;
                }
            } catch (e) {
                alert("An error happend, if this persistes please contact support");
            }
        } else {
            alert("Account login failed: " + JSON.parse(xhr.responseText).error);
        }
    };
    const data = {
        email: email.value,
        password: password.value
    };
    xhr.send(JSON.stringify(data));
}
function checkPassword(){
    const pwd = password.value;
    const fname = firstname.value.toLowerCase();
    const lname = lastname.value.toLowerCase();
    const pwdLower = pwd.toLowerCase();

    if (pwd.length < 8) {
        passwordAlert.innerHTML = "Must be at least 8 characters long";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    if (pwd.length > 40) {
        passwordAlert.innerHTML = "Must not be longer than 40 characters";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd)) {
        passwordAlert.innerHTML = "Must contain at least one letter";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    if (!/\d/.test(pwd)) {
        passwordAlert.innerHTML = "Must contain at least one number";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    if (!/[^a-zA-Z0-9]/.test(pwd) && pwd.length < 14) {
        passwordAlert.innerHTML = "Must contain at least one special character";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    if (fname && pwdLower.includes(fname)) {
        passwordAlert.innerHTML = "Must not contain your first name";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    if (lname && pwdLower.includes(lname)) {
        passwordAlert.innerHTML = "Must not contain your last name";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    const uniqueChars = new Set(pwd).size;
    if (uniqueChars < 6) {
        passwordAlert.innerHTML = "Must contain at least 6 unique characters";
        passwordAlert.classList.remove("hidden");
        return false;
    }
    passwordAlert.classList.add("hidden")
    return true;
}
function checkEmail() {
    const emailValue = email.value;
    // Simple email regex for demonstration
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailValue)) {
        existEmail.innerHTML = "Please enter a valid email address";
        existEmail.classList.remove("hidden");
        return false;
    }
    console.log(emailUnique(emailValue))
    existEmail.classList.add("hidden");
    return true;
}
function emailUnique(email){
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "./register");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.withCredentials = true; // Allow cookies like a form

    xhr.onload = function() {
        if (xhr.status === 200 || xhr.status === 201) {
            try {
                const resp = JSON.parse(xhr.responseText);
                console.log(resp["unique"] == true)
                if(resp["unique"] == true){
                    return true
                }
                else{
                    existEmail.innerHTML = "An acount exists with this Email!";
                    existEmail.classList.remove("hidden");
                }
            } catch (e) {
                alert("An error happend, if this persistes please contact support");
            }
        } else{
            return false
        }
    };
    const data = {
        email: email
    };
    xhr.send(JSON.stringify(data));
}