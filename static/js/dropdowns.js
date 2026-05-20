document.addEventListener('DOMContentLoaded', () => {
    const avatarBtn = document.getElementById('navbarUserMenuBtn');
    const dropdownMenu = document.getElementById('navbarUserDropdown');

    if (avatarBtn && dropdownMenu) {
        avatarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('cmp-dropdown--open');
        });

        document.addEventListener('click', (e) => {
            if (!dropdownMenu.contains(e.target) && !avatarBtn.contains(e.target)) {
                dropdownMenu.classList.remove('cmp-dropdown--open');
            }
        });
    }
});