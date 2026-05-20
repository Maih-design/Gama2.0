document.addEventListener('DOMContentLoaded', () => {
    const alertContainer = document.querySelector('.cmp-alert-container');

    if (alertContainer) {
        alertContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('cmp-alert__close') || e.target.closest('.cmp-alert__close')) {
                const alert = e.target.closest('.cmp-alert');
                if (alert) {
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(-20px)';
                    setTimeout(() => {
                        alert.remove();
                    }, 300);
                }
            }
        });

        // Auto dismiss after 6 seconds
        const alerts = alertContainer.querySelectorAll('.cmp-alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(-20px)';
                    setTimeout(() => alert.remove(), 300);
                }
            }, 6000);
        });
    }
});