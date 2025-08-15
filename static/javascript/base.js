let lastScroll = 0;
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    if (currentScroll > lastScroll && currentScroll > 50) {
        // Bajando: ocultar navbar
        navbar.style.transform = 'translateY(-100%)';
        navbar.style.transition = 'transform 0.3s';
    } else {
        // Subiendo: mostrar navbar
        navbar.style.transform = 'translateY(0)';
        navbar.style.transition = 'transform 0.3s';
    }
    lastScroll = currentScroll;
});