// collection-mobile.js - Menú hamburguesa y toggle de filtros para catálogo
(function() {
  'use strict';

  // ---- Menú móvil ----
  function initMobileMenu() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    // Buscar o crear el botón de menú
    let menuToggle = document.getElementById('navToggle');
    if (!menuToggle) {
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

    // Cerrar menú al redimensionar a escritorio (>900px)
    window.addEventListener('resize', () => {
      if (window.innerWidth > 900 && navbar.classList.contains('mobile-open')) {
        navbar.classList.remove('mobile-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        const icon = menuToggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      }
    });

    // Cerrar menú al hacer clic fuera (opcional pero mejora UX)
    document.addEventListener('click', (e) => {
      if (navbar.classList.contains('mobile-open') && !navbar.contains(e.target)) {
        navbar.classList.remove('mobile-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        const icon = menuToggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      }
    });
  }

  // ---- Toggle de filtros (colapsable) ----
  function initFilterToggle() {
    const filtersSection = document.querySelector('.filters');
    if (!filtersSection) return;

    // Solo aplicar en móvil (ancho <= 900px)
    function applyFilterToggle() {
      if (window.innerWidth > 900) {
        // Si ya existe el toggle y wrapper, limpiar para volver a estado original
        const existingToggle = filtersSection.querySelector('.filter-toggle');
        const existingWrapper = filtersSection.querySelector('.filter-groups-wrapper');
        if (existingToggle && existingWrapper) {
          // Restaurar estructura original (mover hijos fuera del wrapper)
          const children = Array.from(existingWrapper.children);
          children.forEach(child => {
            filtersSection.insertBefore(child, existingToggle);
          });
          existingToggle.remove();
          existingWrapper.remove();
        }
        return;
      }

      // En móvil: crear toggle y wrapper si no existen
      let toggleBtn = filtersSection.querySelector('.filter-toggle');
      let wrapper = filtersSection.querySelector('.filter-groups-wrapper');

      if (!toggleBtn && !wrapper) {
        // Crear wrapper y mover todos los hijos actuales (excepto posibles futuros)
        wrapper = document.createElement('div');
        wrapper.className = 'filter-groups-wrapper';
        
        // Mover todos los hijos directos (los .filter-group y .status-copy) al wrapper
        const children = Array.from(filtersSection.children);
        children.forEach(child => {
          wrapper.appendChild(child);
        });
        
        // Crear botón toggle
        toggleBtn = document.createElement('button');
        toggleBtn.className = 'filter-toggle';
        toggleBtn.innerHTML = '<span><i class="fa-solid fa-sliders-h"></i> Filtrar juegos</span> <i class="fa-solid fa-chevron-down"></i>';
        toggleBtn.setAttribute('aria-expanded', 'false');
        
        // Vaciar filtersSection y agregar toggle + wrapper
        filtersSection.innerHTML = '';
        filtersSection.appendChild(toggleBtn);
        filtersSection.appendChild(wrapper);
      } else if (!toggleBtn) {
        // Solo wrapper existe? Recrear toggle
        toggleBtn = document.createElement('button');
        toggleBtn.className = 'filter-toggle';
        toggleBtn.innerHTML = '<span><i class="fa-solid fa-sliders-h"></i> Filtrar juegos</span> <i class="fa-solid fa-chevron-down"></i>';
        toggleBtn.setAttribute('aria-expanded', 'false');
        filtersSection.insertBefore(toggleBtn, wrapper);
      } else if (!wrapper) {
        // Solo toggle existe? Recrear wrapper y mover hijos
        wrapper = document.createElement('div');
        wrapper.className = 'filter-groups-wrapper';
        const children = Array.from(filtersSection.children);
        // Excluir el toggleBtn de los que se mueven
        children.forEach(child => {
          if (child !== toggleBtn) wrapper.appendChild(child);
        });
        filtersSection.appendChild(wrapper);
      }

      // Asegurar referencias actualizadas
      toggleBtn = filtersSection.querySelector('.filter-toggle');
      wrapper = filtersSection.querySelector('.filter-groups-wrapper');
      if (!toggleBtn || !wrapper) return;

      function updateToggleState() {
        const isOpen = wrapper.classList.contains('open');
        toggleBtn.setAttribute('aria-expanded', isOpen);
        const icon = toggleBtn.querySelector('.fa-chevron-down, .fa-chevron-up');
        if (icon) {
          icon.className = isOpen ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down';
        }
        if (isOpen) {
          toggleBtn.classList.add('open');
        } else {
          toggleBtn.classList.remove('open');
        }
      }

      // Remover event listener previo para evitar duplicados
      const newToggleBtn = toggleBtn.cloneNode(true);
      toggleBtn.parentNode.replaceChild(newToggleBtn, toggleBtn);
      const finalToggle = filtersSection.querySelector('.filter-toggle');
      const finalWrapper = filtersSection.querySelector('.filter-groups-wrapper');

      finalToggle.addEventListener('click', (e) => {
        e.preventDefault();
        finalWrapper.classList.toggle('open');
        updateToggleState();
      });

      // Estado inicial: cerrado en móvil
      if (window.innerWidth <= 900) {
        finalWrapper.classList.remove('open');
      } else {
        finalWrapper.classList.add('open');
      }
      updateToggleState();
    }

    // Ejecutar al cargar y en cada resize
    applyFilterToggle();
    window.addEventListener('resize', () => {
      applyFilterToggle();
    });
  }

  // ---- Inicializar cuando el DOM esté listo ----
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initMobileMenu();
      initFilterToggle();
    });
  } else {
    initMobileMenu();
    initFilterToggle();
  }
})();