document.addEventListener('DOMContentLoaded', () => {
    const printButtons = document.querySelectorAll('[data-action="print-document"]');
    
    printButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            window.print();
        });
    });
});