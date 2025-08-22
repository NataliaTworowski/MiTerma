// Ocultar/mostrar barra de navegación al hacer scroll
let lastScrollTop = 0;
const header = document.querySelector('header');
window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop > lastScrollTop && scrollTop > 50) {
        header.style.transform = 'translateY(-100%)';
        header.style.transition = 'transform 0.3s';
    } else {
        header.style.transform = 'translateY(0)';
        header.style.transition = 'transform 0.3s';
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
}, false);

// Script para menú móvil y modal
document.addEventListener('DOMContentLoaded', function() {
    // Menú móvil
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.onclick = function() {
            mobileMenu.classList.toggle('hidden');
        };
    }

    // Modal de Login
    const loginBtn = document.getElementById('login-btn');
    const loginBtnMobile = document.getElementById('login-btn-mobile');
    const loginModal = document.getElementById('login-modal');
    const closeModal = document.getElementById('close-modal');

    function openModal() {
        if (loginModal) {
            loginModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModalFunc() {
        if (loginModal) {
            loginModal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }

    if (loginBtn) {
        loginBtn.onclick = function(e) {
            e.preventDefault();
            openModal();
        };
    }

    if (loginBtnMobile) {
        loginBtnMobile.onclick = function(e) {
            e.preventDefault();
            if (mobileMenu) mobileMenu.classList.add('hidden');
            openModal();
        };
    }

    if (closeModal) {
        closeModal.onclick = closeModalFunc;
    }

    if (loginModal) {
        loginModal.onclick = function(e) {
            if (e.target === loginModal) closeModalFunc();
        };
    }

    document.onkeydown = function(e) {
        if (e.key === 'Escape' && loginModal && !loginModal.classList.contains('hidden')) {
            closeModalFunc();
        }
    };
});