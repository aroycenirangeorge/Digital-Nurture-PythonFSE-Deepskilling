import { courses } from './data.js';


const gridContainer = document.querySelector('.course-grid');
const searchInput = document.getElementById('course-search');
const sortBtn = document.getElementById('sort-credits');
const totalDisplay = document.getElementById('total-credits-display');

const renderCourses = (data) => {
    gridContainer.innerHTML = '';
    data.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Code: ${course.code}</p>
            <span>Credits: ${course.credits}</span>
        `;
        article.dataset.name = course.name;
        article.dataset.grade = course.grade;
        gridContainer.appendChild(article);
    });
    const total = data.reduce((sum, c) => sum + c.credits, 0);
    totalDisplay.textContent = `Total Credits: ${total}`;
};

searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = courses.filter(c => c.name.toLowerCase().includes(term));
    renderCourses(filtered);
});

sortBtn.addEventListener('click', () => {
    const sorted = [...courses].sort((a, b) => b.credits - a.credits);
    renderCourses(sorted);
});

gridContainer.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (card) {
        alert(`Course: ${card.dataset.name}\nGrade: ${card.dataset.grade}`);
    }
});


axios.interceptors.request.use(config => {
    console.log(`API call started: ${config.url}`);
    return config;
});


async function apiFetch(url, params = {}) {
    try {
        const response = await axios.get(url, { params: params, timeout: 5000 });
        return response.data;
    } catch (err) {
        throw new Error(err.response ? `HTTP Error: ${err.response.status}` : err.message);
    }
}

async function loadNotifications() {
    const container = document.getElementById('notif-container');
    const feedback = document.getElementById('notif-feedback');
    feedback.innerHTML = '<p class="spinner">Loading notifications...</p>';
    
    try {
        const posts = await apiFetch('https://jsonplaceholder.typicode.com/posts', { _limit: 3 });
        feedback.innerHTML = '';
        posts.forEach(post => {
            container.innerHTML += `<div class="notif-card"><h4>${post.title}</h4></div>`;
        });
    } catch (err) {
        feedback.innerHTML = `<p>Error: ${err.message}.</p><button id="retry-btn">Retry</button>`;
        document.getElementById('retry-btn').onclick = loadNotifications;
    }
}

const initPortal = async () => {
    gridContainer.innerHTML = '<p>Loading courses...</p>';
    await new Promise(resolve => setTimeout(resolve, 1000));
    renderCourses(courses);
};


initPortal();
loadNotifications();