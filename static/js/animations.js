document.addEventListener('DOMContentLoaded', () => {
    // Premium entry initialization for cards and responsive elements
    const elements = document.querySelectorAll('.dsh-card-stat, .dsh-panel, .tbl-wrapper');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'anim-fade-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.05 });

    elements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
});