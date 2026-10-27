document.addEventListener('DOMContentLoaded', () => {
    // Переключение вкладок
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.querySelector(`#${tab.dataset.tab}`).classList.add('active');
        });
    });

    // Кнопка "Все характеристики"
    const showAllBtn = document.querySelector('#show-all');
    if (showAllBtn) {
        const allFeatures = document.querySelector('#all-features');
        showAllBtn.addEventListener('click', () => {
            allFeatures.classList.toggle('hidden');
            showAllBtn.textContent = allFeatures.classList.contains('hidden')
                ? 'Все характеристики'
                : 'Скрыть';
        });
    }
});
