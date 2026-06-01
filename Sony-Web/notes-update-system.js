/**
 * Sistema de Actualizaciones de Notas
 * Maneja la visualización de badges en tarjetas cuando hay notas nuevas
 */

class NotesUpdateSystem {
  constructor() {
    this.updateBadgeDuration = 30000; // 30 segundos antes de ocultarse automáticamente
    this.dismissedUpdates = this.loadDismissedUpdates();
  }

  /**
   * Cargar IDs de actualizaciones ya vistas
   */
  loadDismissedUpdates() {
    try {
      const stored = localStorage.getItem('dismissedGameUpdates');
      return stored ? JSON.parse(stored) : {};
    } catch (e) {
      console.error('Error loading dismissed updates:', e);
      return {};
    }
  }

  /**
   * Guardar IDs de actualizaciones vistas
   */
  saveDismissedUpdates() {
    try {
      localStorage.setItem('dismissedGameUpdates', JSON.stringify(this.dismissedUpdates));
    } catch (e) {
      console.error('Error saving dismissed updates:', e);
    }
  }

  /**
   * Obtener fecha formateada en español
   */
  formatDate(isoString) {
    try {
      const date = new Date(isoString);
      const now = new Date();
      const diff = now - date;
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor(diff / (1000 * 60));

      if (minutes < 1) return 'Hace unos segundos';
      if (minutes < 60) return `Hace ${minutes} min`;
      if (hours < 24) return `Hace ${hours}h`;

      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      if (days === 1) return 'Ayer';
      if (days < 7) return `Hace ${days} días`;

      return date.toLocaleDateString('es-ES');
    } catch (e) {
      return 'Actualizado recientemente';
    }
  }

  /**
   * Crear badge de actualización
   */
  createUpdateBadge(gameId, game) {
    const badge = document.createElement('div');
    badge.className = 'update-badge new';
    badge.dataset.gameId = gameId;
    badge.innerHTML = '✨ ACTUALIZADO';

    // Crear tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'update-tooltip';
    const updateText = game.lastContentUpdate ? this.formatDate(game.lastContentUpdate) : 'Recientemente';
    tooltip.textContent = updateText;

    badge.appendChild(tooltip);

    // Remover animación de entrada después de completarse
    setTimeout(() => {
      badge.classList.remove('new');
    }, 600);

    return badge;
  }

  /**
   * Insertar badge en tarjeta
   */
  addBadgeToCard(cardElement, gameId, game) {
    if (!cardElement || !game) return;

    // Evitar duplicados
    if (cardElement.querySelector('.update-badge')) return;

    const badge = this.createUpdateBadge(gameId, game);
    cardElement.style.position = 'relative';
    cardElement.prepend(badge);

    // Auto-remover después del tiempo definido
    setTimeout(() => {
      this.removeBadge(badge);
    }, this.updateBadgeDuration);

    // Remover al hacer clic o interactuar
    const removeOnInteraction = () => {
      this.removeBadge(badge);
      cardElement.removeEventListener('click', removeOnInteraction);
      cardElement.removeEventListener('mouseenter', removeOnInteraction);
    };

    cardElement.addEventListener('click', removeOnInteraction);
    cardElement.addEventListener('mouseenter', removeOnInteraction);
  }

  /**
   * Remover badge con animación
   */
  removeBadge(badge) {
    if (!badge) return;
    const gameId = badge.dataset.gameId;
    
    badge.classList.add('dismissing');
    setTimeout(() => {
      badge.remove();
      if (gameId) {
        this.dismissedUpdates[gameId] = new Date().toISOString();
        this.saveDismissedUpdates();
      }
    }, 500);
  }

  /**
   * Procesar tarjetas de mini-carousel
   */
  processMiniCards(gamesData) {
    const miniCards = document.querySelectorAll('.mini-card');
    miniCards.forEach(card => {
      const gameId = card.dataset.gameId || card.getAttribute('data-id');
      if (gameId && gamesData.games && gamesData.games[gameId]) {
        const game = gamesData.games[gameId];
        if (game.hasNewUpdates && !this.dismissedUpdates[gameId]) {
          this.addBadgeToCard(card, gameId, game);
        }
      }
    });
  }

  /**
   * Procesar tarjetas bento
   */
  bentoBentoItems(gamesData) {
    const bentoItems = document.querySelectorAll('.bento-item');
    bentoItems.forEach(item => {
      const gameId = item.dataset.gameId || item.getAttribute('data-id');
      if (gameId && gamesData.games && gamesData.games[gameId]) {
        const game = gamesData.games[gameId];
        if (game.hasNewUpdates && !this.dismissedUpdates[gameId]) {
          this.addBadgeToCard(item, gameId, game);
        }
      }
    });
  }

  /**
   * Procesar tarjetas premiere
   */
  processPremiereCards(gamesData) {
    const premiereCards = document.querySelectorAll('.premiere-card');
    premiereCards.forEach(card => {
      const gameId = card.dataset.gameId || card.getAttribute('data-id');
      if (gameId && gamesData.games && gamesData.games[gameId]) {
        const game = gamesData.games[gameId];
        if (game.hasNewUpdates && !this.dismissedUpdates[gameId]) {
          this.addBadgeToCard(card, gameId, game);
        }
      }
    });
  }

  /**
   * Inicializar sistema
   */
  async init(gamesData) {
    if (!gamesData || !gamesData.games) {
      console.warn('Games data not available for NotesUpdateSystem');
      return;
    }

    // Procesar todas las tarjetas
    this.processMiniCards(gamesData);
    this.bentoBentoItems(gamesData);
    this.processPremiereCards(gamesData);

    console.log('✨ Sistema de actualizaciones inicializado');
  }

  /**
   * Forzar actualización (útil para testing)
   */
  markAsUpdated(gameId) {
    delete this.dismissedUpdates[gameId];
    this.saveDismissedUpdates();
  }

  /**
   * Limpiar todas las actualizaciones vistas
   */
  clearDismissed() {
    this.dismissedUpdates = {};
    this.saveDismissedUpdates();
    console.log('✨ Actualizaciones limpiadas');
  }
}

// Instancia global
const notesUpdateSystem = new NotesUpdateSystem();

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  // Buscar datos de juegos en el DOM o variable global
  if (window.gamesData) {
    notesUpdateSystem.init(window.gamesData);
  } else {
    // Intentar cargar desde archivo de datos
    fetch('games.json')
      .then(res => res.json())
      .then(data => {
        window.gamesData = data;
        notesUpdateSystem.init(data);
      })
      .catch(err => console.warn('No games.json found:', err));
  }
});
