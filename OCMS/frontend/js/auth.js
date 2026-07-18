const BASE_URL = "http://127.0.0.1:8000"


async function login(event) {
    event.preventDefault()

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    const res = await fetch(`${BASE_URL}/api/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })

    const data = await res.json()

    if (data.access) {
        localStorage.setItem("token", data.access)
        alert("Login Successful")
        window.location.href = "dashboard.html"
    } else {
        alert("Invalid Login")
    }
}



async function signup(event) {
    event.preventDefault()

    const username = document.getElementById("username").value
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const role = document.getElementById("role").value
    const phone = document.getElementById("phone").value

    const res = await fetch(`${BASE_URL}/accounts/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password, role, phone })
    })

    if (res.ok) {
        alert("User Registered Successfully")
        window.location.href = "login.html"
    } else {
        alert("Registration Failed")
    }
}



function logout() {
    localStorage.removeItem("token")
    window.location.href = "login.html"
}


function checkAuth() {
    const token = localStorage.getItem("token")
    if (!token) {
        alert("Login First")
        window.location.href = "login.html"
    }
}