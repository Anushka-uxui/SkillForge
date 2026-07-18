const BASE_URL = "http://127.0.0.1:8000"
const token = localStorage.getItem("token")

async function loadCourses() {

    let res = await fetch(`${BASE_URL}/courses/`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })

    let data = await res.json()

    let html = ""

    data.results?.forEach(c => {
        html += `
<div style="border:1px solid black;padding:10px;margin:10px">
<h3>${c.title}</h3>
<p>${c.description}</p>
<p>Category: ${c.category}</p>
<p>Price: ₹${c.price}</p>
</div>
`
    })

    document.getElementById("courseList").innerHTML = html
}

loadCourses()