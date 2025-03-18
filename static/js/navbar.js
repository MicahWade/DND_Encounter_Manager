const navLinks = document.querySelector('.nav-links')
function onToggleMenu(e) {
    e.name = e.name == 'menu-sharp' ? 'close-sharp' : 'menu-sharp'
    navLinks.classList.toggle('top-[9%]')
}