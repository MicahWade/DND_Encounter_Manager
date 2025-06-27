const registerSpan = document.getElementById(`registerspan`);
const firstname = document.getElementById(`firstname`);
const lastname = document.getElementById(`lastname`);
const password = document.getElementById(`password`);
const email = document.getElementById(`email`);
const terms = document.getElementById('terms')

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
    } if(!checkEmail()){
        return
    }

    // JSON request 
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "./register");
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
            } catch (e) {}
            // alert("Account created successfully!");
        } else {
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
    firstname.classList.remove("hidden");
    lastname.classList.remove("hidden");
}
function login(){

}
function checkPassword(){
    const pwd = password.value;
    const fname = firstname.value.toLowerCase();
    const lname = lastname.value.toLowerCase();
    const pwdLower = pwd.toLowerCase();

    if (pwd.length < 8) {
        alert("Password must be at least 8 characters long.");
        return false;
    }
    if (pwd.length > 40) {
        alert("Password must not be longer than 40 characters.");
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd)) {
        alert("Password must contain at least one letter.");
        return false;
    }
    if (!/\d/.test(pwd)) {
        alert("Password must contain at least one number.");
        return false;
    }
    if (!/[^a-zA-Z0-9]/.test(pwd) && pwd.length < 14) {
        alert("Password must contain at least one special character or be more than 14 characters long.");
        return false;
    }
    if (fname && pwdLower.includes(fname)) {
        alert("Password must not contain your first name.");
        return false;
    }
    if (lname && pwdLower.includes(lname)) {
        alert("Password must not contain your last name.");
        return false;
    }
    const uniqueChars = new Set(pwd).size;
    if (uniqueChars < 6) {
        alert("Password must contain at least 6 unique characters.");
        return false;
    }
    return true;
}
function checkEmail() {
    const emailValue = email.value;
    // Simple email regex for demonstration
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailValue)) {
        alert("Please enter a valid email address.");
        return false;
    }
    return true;
}