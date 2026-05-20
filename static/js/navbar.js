document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.cmp-navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
            navbar.style.boxShadow = 'var(--shadow-md)';
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        } else {
            navbar.style.boxShadow = 'none';
            navbar.style.background = 'rgba(255, 255, 255, 0.85)';
        }
    });
});