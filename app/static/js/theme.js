function toggleTheme() {
    const html = document.documentElement;
    const newTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
    html.dataset.theme = newTheme;
    localStorage.setItem('theme', newTheme);

    const mapDiv = document.getElementById('map');
    if (newTheme === 'dark') mapDiv.classList.add('dark-map');
    else mapDiv.classList.remove('dark-map');
}

// Persistir tema ao carregar
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.dataset.theme = savedTheme;