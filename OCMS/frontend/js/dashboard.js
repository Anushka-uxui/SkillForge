
function checkAuth() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Login first");
        window.location = "login.html";
    }
}



async function loadCourses() {

    const token = localStorage.getItem("token");

    const res = await fetch(`${BASE_URL}/courses/`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!res.ok) {
        alert("Failed to load courses");
        return;
    }

    const data = await res.json();
    const courses = data.results || data;

    let html = "";

    courses.forEach(c => {
        html += `
        <div style="border:1px solid black; padding:10px; margin:10px;">
            <h3>${c.title}</h3>
            <p>${c.description}</p>
            <p>Price: ₹${c.price}</p>
            <button onclick="enroll(${c.id})">Enroll</button>
        </div>
        `;
    });

    document.getElementById("courses").innerHTML = html;
}



async function enroll(courseId) {

    const token = localStorage.getItem("token");

    const res = await fetch(`${BASE_URL}/enrollments/enroll/${courseId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await res.json();

    alert(data.message || "Enrollment done");
}


function logout() {
    localStorage.removeItem("token");
    window.location = "login.html";
}


// Auto run
window.onload = () => {
    checkAuth();
    loadCourses();
};