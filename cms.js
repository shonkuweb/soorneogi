document.addEventListener('DOMContentLoaded', () => {
    // Fetch CMS Content
    fetch('http://localhost:8080/api/content')
        .then(res => res.json())
        .then(data => {
            const elements = document.querySelectorAll('[data-cms-key]');
            elements.forEach(el => {
                const key = el.getAttribute('data-cms-key');
                if(data[key]) {
                    el.innerHTML = data[key];
                }
            });
        })
        .catch(err => console.error("CMS Fetch Error:", err));
});
