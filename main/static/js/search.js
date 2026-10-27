document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('product-search-input');
    const box = document.getElementById('autocomplete-box');
    if (!searchInput || !box) return;

    searchInput.addEventListener('input', function() {
        const q = this.value.trim();
        if (q.length < 2) {
            box.style.display = 'none';
            box.innerHTML = '';
            return;
        }
        fetch(`/products/autocomplete/?q=${encodeURIComponent(q)}`)
            .then(res => res.json())
            .then(data => {
                box.innerHTML = '';
                let results = data.results || [];
                if (results.length > 0) {
                    results.forEach(item => {
                        const option = document.createElement('div');
                        option.className = 'autocomplete-suggestion';
                        option.textContent = item.title;
                        option.onclick = function(e) {
                            e.preventDefault();
                            window.location.href = item.url;
                        };
                        box.appendChild(option);
                    });
                    box.style.display = 'block';
                } else {
                    const empty = document.createElement('div');
                    empty.className = 'autocomplete-suggestion';
                    empty.textContent = 'Ничего не найдено';
                    box.appendChild(empty);
                    box.style.display = 'block';
                }
            });
    });
    document.addEventListener('mousedown', function(e) {
        if (!box.contains(e.target) && e.target !== searchInput) {
            box.style.display = 'none';
        }
    });
});
