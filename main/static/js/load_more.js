document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('.load-more');
  const container = document.querySelector('#product-container');
  if (!button || !container) return;

  let isLoading = false;

  button.addEventListener('click', async () => {
    if (isLoading) return;
    const nextPage = button.dataset.next;
    if (!nextPage) return;

    const params = new URLSearchParams(window.location.search);
    params.set('page', nextPage);

    const prevText = button.textContent;
    isLoading = true;
    button.disabled = true;
    button.textContent = 'Загружаю…';

    try {
      const url = `${window.location.pathname}?${params.toString()}`;
      const res = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      const html = await res.text();

      const doc = new DOMParser().parseFromString(html, 'text/html');
      const newItems = doc.querySelectorAll('#product-container .product-card');

      if (newItems.length === 0) {
        button.remove();
        return;
      }

      newItems.forEach(item => container.appendChild(item));

      const newButton = doc.querySelector('.load-more');

      if (!newButton) {
        button.remove();
      } else {
        button.dataset.next = newButton.dataset.next;

        // в адресе фиксируем фактически загруженную страницу
        const currentParams = new URLSearchParams(window.location.search);
        currentParams.set('page', String(Number(newButton.dataset.next) - 1));
        history.replaceState(null, '', `${window.location.pathname}?${currentParams.toString()}`);

        button.disabled = false;
        button.textContent = prevText;
        isLoading = false;
        return;
      }
    } catch (err) {
      console.error('Ошибка загрузки', err);
      button.disabled = false;
      button.textContent = prevText;
      isLoading = false;
      return;
    }

    isLoading = false;
  });
});
