let menu=document.querySelector('#menu-bars');
let navbar=document.querySelector('.navbar');

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}



function search() {
    let query = document.getElementById("searchInput").value;
    console.log("Searching for:", query);
    // You can replace the console.log with actual search logic
}

document.getElementById("searchInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        search();
    }
});




function login() {
    let email = document.getElementById("loginEmail").value;
    let password = document.getElementById("loginPassword").value;
    
    if (email.trim() === "" || password.trim() === "") {
        alert("Please enter both email/username and password.");
        return;
    }
    
    alert("Login successful! (Backend functionality to be implemented)");
}

function register() {
    let orgName = document.getElementById("orgName").value;
    let orgType = document.getElementById("orgType").value;
    let orgAddress = document.getElementById("orgAddress").value;
    let orgContact = document.getElementById("orgContact").value;
    let orgEmail = document.getElementById("orgEmail").value;
    let username = document.getElementById("regUsername").value;
    let password = document.getElementById("regPassword").value;

    if (!orgName || !orgType || !orgAddress || !orgContact || !orgEmail || !username || !password) {
        alert("Please fill in all fields.");
        return;
    }

    alert("Registration successful! (Backend functionality to be implemented)");
}

// Show login form by default when page loads
showLogin();document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault();  // ✅ Prevent normal form submission

    fetch("http://127.0.0.1:5000/register", {  // ✅ Ensure Flask URL is correct
        method: "POST",
        body: new FormData(this)
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
});

fetch('http://127.0.0.1:5000/home', {
    method: 'GET',
    mode: 'cors',  // ✅ Enables CORS
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

