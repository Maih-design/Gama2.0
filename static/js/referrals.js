/**
 * Premium Healthcare Operations - Referrals Component Pipeline Interactions Engine
 */
document.addEventListener('DOMContentLoaded', () => {
    // Pipeline Trigger: Handle On-The-Fly Center Adjustments Inside The Active Queue Matrix
    const changeCenterButtons = document.querySelectorAll('[data-action="change-center-trigger"]');
    
    changeCenterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const referralId = this.dataset.referralId;
            const currentCenter = this.dataset.currentCenter;
            
            // Dynamic Verification Dialog Frame
            const targetSelectWrapper = document.getElementById(`inline-center-selector-${referralId}`);
            if (targetSelectWrapper) {
                targetSelectWrapper.style.display = targetSelectWrapper.style.display === 'none' ? 'flex' : 'none';
            }
        });
    });

    // Pipeline Trigger: Standardized Printing Dialog Interceptor Framework
    const hardwarePrintButtons = document.querySelectorAll('[data-action="hardware-print-trigger"]');
    hardwarePrintButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    });
});