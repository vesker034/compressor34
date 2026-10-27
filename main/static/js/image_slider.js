document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.image-slider').forEach(slider => {
        const thumbs = slider.querySelectorAll('.thumb');
        const current = slider.querySelector('.slider-current');
        const prevBtn = slider.querySelector('.slider-btn.prev');
        const nextBtn = slider.querySelector('.slider-btn.next');

        const images = Array.from(thumbs).map(t => t.getAttribute('src'));
        let currentIndex = 0;

        function showImage(index) {
            if (!images.length) return;
            currentIndex = (index + images.length) % images.length;
            current.src = images[currentIndex];
            thumbs.forEach((t, i) => t.classList.toggle('active', i === currentIndex));
        }

        thumbs.forEach((thumb, idx) => thumb.addEventListener('click', () => showImage(idx)));

        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', e => { e.stopPropagation(); showImage(currentIndex - 1); });
            nextBtn.addEventListener('click', e => { e.stopPropagation(); showImage(currentIndex + 1); });
        }

        // Модалка (fullscreen)
        const modal = document.querySelector('.slider-modal');
        const modalImg = modal.querySelector('.modal-img');
        const modalPrev = modal.querySelector('.modal-btn.prev');
        const modalNext = modal.querySelector('.modal-btn.next');

        function openModal() {
            modalImg.src = images[currentIndex];
            modal.classList.remove('hidden');
        }
        function closeModal() {
            modal.classList.add('hidden');
        }
        function modalShow(i) {
            currentIndex = (i + images.length) % images.length;
            modalImg.src = images[currentIndex];
        }

        if (current) current.addEventListener('click', openModal);
        modal.addEventListener('click', closeModal);
        modalPrev.addEventListener('click', e => { e.stopPropagation(); modalShow(currentIndex - 1); });
        modalNext.addEventListener('click', e => { e.stopPropagation(); modalShow(currentIndex + 1); });

        showImage(0);
    });
});
