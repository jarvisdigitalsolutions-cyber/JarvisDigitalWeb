// mobile-menu.js - Control del menú hamburguesa y ajustes responsive compartidos
(function() {
  // Función para inicializar el menú móvil en una página
  function initMobileMenu() {
    const navbar = document.querySelector('.navbar');
    // Buscar o crear el botón de menú
    let menuToggle = document.getElementById('navToggle');
    if (!menuToggle && navbar) {
      // Crear el botón si no existe
      menuToggle = document.createElement('button');
      menuToggle.id = 'navToggle';
      menuToggle.className = 'menu-toggle';
      menuToggle.setAttribute('aria-label', 'Abrir menú');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
      // Insertar antes de .nav-actions
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
      menuToggle.setAttribute('aria-expanded', String(isOpen));
      const icon = menuToggle.querySelector('i');
      if (icon) {
        icon.className = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
      }
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

    // Cerrar menú al hacer clic fuera (opcional)
    document.addEventListener('click', (e) => {
      if (navbar.classList.contains('mobile-open') && !navbar.contains(e.target)) {
        navbar.classList.remove('mobile-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        const icon = menuToggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      }
    });
  }

  // Ejecutar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileMenu);
  } else {
    initMobileMenu();
  }
})();