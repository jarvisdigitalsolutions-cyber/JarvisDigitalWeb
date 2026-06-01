/**
 * Image Fallback Handler
 * Muestra imagen de error cuando falla la carga
 */

const IMAGE_FALLBACK = "IMG/PS5/Loader-Error.png";

/**
 * Inicializar manejo de errores de imágenes
 */
function initImageFallback() {
  // Todas las imágenes en la página
  const images = document.querySelectorAll('img[src]');
  
  images.forEach(img => {
    // Agregar handler para error
    img.addEventListener('error', function(e) {
      console.warn(`⚠️ Error cargando imagen: ${this.src}`);
      
      // Si no es ya la imagen de fallback, cambiar
      if (!this.src.includes('Loader-Error')) {
        this.src = IMAGE_FALLBACK;
        this.alt = 'Imagen no disponible';
        this.style.opacity = '0.6';
      }
    });
    
    // Agregar timeout para imágenes lentas (5 segundos)
    const timeout = setTimeout(() => {
      if (!img.complete) {
        console.warn(`⏱️ Timeout cargando imagen: ${img.src}`);
        img.src = IMAGE_FALLBACK;
      }
    }, 5000);
    
    img.addEventListener('load', () => clearTimeout(timeout));
    img.addEventListener('error', () => clearTimeout(timeout));
  });
}

/**
 * Para imágenes dinámicas (cargadas después de inicialización)
 */
function setImageFallback(imgElement) {
  if (!imgElement) return;
  
  imgElement.addEventListener('error', function(e) {
    console.warn(`⚠️ Error cargando imagen dinámica: ${this.src}`);
    if (!this.src.includes('Loader-Error')) {
      this.src = IMAGE_FALLBACK;
      this.alt = 'Imagen no disponible';
      this.style.opacity = '0.6';
    }
  });
}

// Ejecutar cuando DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initImageFallback);
} else {
  initImageFallback();
}

// Reinicializar cada 2 segundos para capturar imágenes dinámicas
setInterval(initImageFallback, 2000);

/**
 * Comprobar elementos con background-image y aplicar fallback si la URL no carga
 */
function checkBackgroundImageFallback() {
  const els = document.querySelectorAll('[style*="background-image"]');
  els.forEach(el => {
    const bg = el.style.backgroundImage || '';
    if (!bg || bg === 'none') return;
    const m = bg.match(/url\((?:"|')?(.*?)(?:"|')?\)/);
    if (!m) return;
    const url = m[1];
    if (!url || url.includes('Loader-Error')) return;
    const img = new Image();
    let handled = false;
    img.onload = function() { handled = true; };
    img.onerror = function() {
      if (handled) return;
      handled = true;
      el.style.backgroundImage = `url('${IMAGE_FALLBACK}')`;
      el.setAttribute('aria-hidden', 'false');
    };
    img.src = url;
    // timeout para recursos muy lentos
    setTimeout(() => {
      if (!handled) {
        el.style.backgroundImage = `url('${IMAGE_FALLBACK}')`;
      }
    }, 5000);
  });
}

// Ejecutar también la comprobación para fondos cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', checkBackgroundImageFallback);
} else {
  checkBackgroundImageFallback();
}
setInterval(checkBackgroundImageFallback, 2000);
