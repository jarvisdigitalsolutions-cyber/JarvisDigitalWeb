// detail-mobile.js - Menú móvil, animaciones y mejoras táctiles para PS-Details.html

(function() {
  'use strict';

  // ========== MENÚ HAMBURGUESA ==========
  function initMobileMenu() {
    const navbar = document.querySelector('.navbar');
    let menuToggle = document.getElementById('navToggle');
    
    // Si no existe el botón, lo creamos
    if (!menuToggle && navbar) {
      menuToggle = document.createElement('button');
      menuToggle.id = 'navToggle';
      menuToggle.className = 'menu-toggle';
      menuToggle.setAttribute('aria-label', 'Abrir menú');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
      
      const navActions = document.querySelector('.nav-actions');
      if (navActions) {
        navbar.insertBefore(menuToggle, navActions);
      } else {
        navbar.appendChild(menuToggle);
      }
    }

    if (!menuToggle) return;

    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;

    function toggleMenu() {
      const isOpen = navbar.classList.toggle('mobile-open');
      menuToggle.setAttribute('aria-expanded', isOpen);
      const icon = menuToggle.querySelector('i');
      if (icon) {
        icon.className = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
      }
      // Animación adicional: vibración suave (opcional)
      if (isOpen && navigator.vibrate) navigator.vibrate(50);
    }

    menuToggle.addEventListener('click', toggleMenu);

    // Cerrar menú al hacer clic en un enlace
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        if (navbar.classList.contains('mobile-open')) {
          navbar.classList.remove('mobile-open');
          menuToggle.setAttribute('aria-expanded', 'false');
          const icon = menuToggle.querySelector('i');
          if (icon) icon.className = 'fa-solid fa-bars';
        }
      });
    });

    // Cerrar menú al redimensionar a escritorio
    window.addEventListener('resize', () => {
      if (window.innerWidth > 900 && navbar.classList.contains('mobile-open')) {
        navbar.classList.remove('mobile-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        const icon = menuToggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      }
    });

    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', (e) => {
      if (navbar.classList.contains('mobile-open') && !navbar.contains(e.target)) {
        navbar.classList.remove('mobile-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        const icon = menuToggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      }
    });
  }

  // ========== ANIMACIONES AL HACER SCROLL ==========
  function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.hero, .panel, .trailer-wrap');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'none';
          entry.target.offsetHeight; // Reflow
          entry.target.style.animation = 'fadeUp 0.6s ease-out forwards';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    animatedElements.forEach(el => observer.observe(el));
  }

  // ========== MEJORA DE LA GALERÍA DE PREVIEWS ==========
  function enhancePreviewShelf() {
    const shelf = document.getElementById('previewShelf');
    if (!shelf) return;

    // Scroll suave con touch
    let isDown = false;
    let startX;
    let scrollLeft;

    shelf.addEventListener('touchstart', (e) => {
      isDown = true;
      startX = e.touches[0].pageX - shelf.offsetLeft;
      scrollLeft = shelf.scrollLeft;
    });

    shelf.addEventListener('touchmove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.touches[0].pageX - shelf.offsetLeft;
      const walk = (x - startX) * 1.2;
      shelf.scrollLeft = scrollLeft - walk;
    });

    shelf.addEventListener('touchend', () => {
      isDown = false;
    });
  }

  // ========== AJUSTE DE ALTURA DEL TRÁILER EN MÓVIL ==========
  function adjustTrailerHeight() {
    const trailer = document.querySelector('.trailer-card.trailer-hero-card');
    if (!trailer) return;
    if (window.innerWidth <= 900) {
      const width = trailer.clientWidth;
      trailer.style.minHeight = `${width * 0.5625}px`; // 16:9
    } else {
      trailer.style.minHeight = '';
    }
  }

  // ========== INICIALIZAR TODO ==========
  function init() {
    initMobileMenu();
    initScrollAnimations();
    enhancePreviewShelf();
    adjustTrailerHeight();
    window.addEventListener('resize', () => {
      adjustTrailerHeight();
      // Re-observar elementos si es necesario
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();