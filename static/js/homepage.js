document.addEventListener('DOMContentLoaded', () => {
    const printCardBtn = document.getElementById('hmpPrintRequirementsBtn');

    if (printCardBtn) {
        printCardBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Set global isolating layout flag to cleanly split the context viewport visually for hardware printers
            document.body.classList.add('hmp-print-isolated-mode');
            
            // Trigger operational system hardware dialogue pipeline safely
            window.print();
            
            // Cleanup interface state transitions smoothly upon system frame focus restoration
            setTimeout(() => {
                document.body.classList.remove('hmp-print-isolated-mode');
            }, 500);
        });
    }
});