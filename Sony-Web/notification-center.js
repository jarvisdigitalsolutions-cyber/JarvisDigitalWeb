/**
 * NOTIFICATION CENTER SYSTEM
 * Gestiona notificaciones de actualizaciones con estado viewed/unviewed
 */

class NotificationCenter {
  constructor() {
    this.notifications = this.loadNotifications();
    this.storageKey = 'ps5-notifications';
    this.init();
  }

  /**
   * Cargar notificaciones desde localStorage
   */
  loadNotifications() {
    try {
      const stored = localStorage.getItem('ps5-notifications');
      return stored ? JSON.parse(stored) : {};
    } catch {
      return {};
    }
  }

  /**
   * Guardar notificaciones en localStorage
   */
  saveNotifications() {
    localStorage.setItem('ps5-notifications', JSON.stringify(this.notifications));
  }

  /**
   * Agregar nueva notificación
   */
  addNotification(gameId, gameData, showToastNotification = true) {
    // Priorizar imágenes: image > bannerImage > previewImages[0] > ''
    const image = gameData.image || gameData.bannerImage || (gameData.previewImages && gameData.previewImages[0]) || '';
    
    if (!this.notifications[gameId]) {
      // Primera vez: crear nueva notificación
      this.notifications[gameId] = {
        gameId,
        title: gameData.title,
        image: image,
        timestamp: gameData.lastContentUpdate,
        viewed: false,
        message: gameData.note?.title || 'Actualización disponible',
        updateCount: 0
      };
    } else {
      // Actualizar notificación existente - PRESERVAR viewed status del usuario
      const wasViewed = this.notifications[gameId].viewed;
      this.notifications[gameId].timestamp = gameData.lastContentUpdate;
      this.notifications[gameId].image = image;
      this.notifications[gameId].message = gameData.note?.title || 'Actualización disponible';
      this.notifications[gameId].viewed = wasViewed; // Mantener estado que marcó usuario
      this.notifications[gameId].updateCount++;
    }

    this.saveNotifications();
    this.updateBellIcon();
    
    // Solo mostrar toast si se solicita (para evitar spam en cambios duplicados)
    if (showToastNotification) {
      this.showToast(gameId, gameData);
    }
  }

  /**
   * Marcar notificación como vista
   */
  markAsViewed(gameId) {
    if (this.notifications[gameId]) {
      this.notifications[gameId].viewed = true;
      this.saveNotifications();
      this.updateBellIcon();
    }
  }

  /**
   * Marcar TODAS las notificaciones como vistas (Auto)
   */
  markAllAsViewed() {
    Object.keys(this.notifications).forEach(gameId => {
      this.notifications[gameId].viewed = true;
    });
    this.saveNotifications();
    this.updateBellIcon();
  }

  /**
   * Marcar TODAS como vistas (Manual - desde panel)
   */
  markAllAsViewedManual() {
    Object.keys(this.notifications).forEach(gameId => {
      this.notifications[gameId].viewed = true;
    });
    this.saveNotifications();
    this.updateBellIcon();
    this.togglePanel(); // Cerrar panel
    this.showSimpleToast('Todas marcadas como leídas');
  }

  /**
   * Obtener notificaciones no vistas
   */
  getUnviewedCount() {
    return Object.values(this.notifications)
      .filter(n => !n.viewed)
      .length;
  }

  /**
   * Obtener todas las notificaciones ordenadas
   */
  getAllNotifications() {
    return Object.values(this.notifications).sort((a, b) => 
      new Date(b.timestamp) - new Date(a.timestamp)
    );
  }

  /**
   * Limpiar todas las notificaciones
   */
  clearAll() {
    this.notifications = {};
    this.saveNotifications();
    this.updateBellIcon();
  }

  /**
   * Actualizar el icono del bell en navbar
   */
  updateBellIcon() {
    const bellContainer = document.getElementById('notification-bell');
    if (!bellContainer) return;

    const unviewedCount = this.getUnviewedCount();
    const badge = bellContainer.querySelector('.notification-badge');

    if (unviewedCount > 0) {
      if (badge) {
        badge.textContent = unviewedCount;
      } else {
        const newBadge = document.createElement('span');
        newBadge.className = 'notification-badge';
        newBadge.textContent = unviewedCount;
        bellContainer.appendChild(newBadge);
      }
      bellContainer.classList.add('has-notifications');
    } else {
      if (badge) badge.remove();
      bellContainer.classList.remove('has-notifications');
    }
  }

  /**
   * Mostrar toast con imagen (para notificaciones de cambios)
   */
  showToast(gameId, gameData) {
    const toast = document.createElement('div');
    toast.className = 'notification-toast notification-toast-game';
    
    const image = gameData.images?.hero || gameData.images?.banner || '';
    const imageHtml = image ? `<img src="${image}" alt="${gameData.title}" class="toast-game-image">` : '';
    
    toast.innerHTML = `
      <div class="toast-content">
        ${imageHtml}
        <div class="toast-text">
          <div class="toast-title">✨ Actualización</div>
          <div class="toast-game-title">${gameData.title}</div>
          <div class="toast-message">${gameData.note?.title || 'Cambios disponibles'}</div>
        </div>
      </div>
    `;
    
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  /**
   * Mostrar toast simple (para mensajes sin imagen)
   */
  showSimpleToast(message) {
    const toast = document.createElement('div');
    toast.className = 'notification-toast notification-toast-simple';
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  /**
   * Renderizar panel de notificaciones
   */
  renderPanel() {
    const notifications = this.getAllNotifications();
    const unviewedCount = this.getUnviewedCount();

    let html = `
      <div class="notification-panel-header">
        <h3>Actualizaciones</h3>
        <div class="notification-header-stats">
          <span class="notification-count">${notifications.length}</span>
          ${unviewedCount > 0 ? `<span class="unviewed-indicator">${unviewedCount} sin ver</span>` : ''}
        </div>
      </div>
      <div class="notification-panel-content">
    `;

    if (notifications.length === 0) {
      html += '<div class="notification-empty">Sin notificaciones</div>';
    } else {
      notifications.forEach(notif => {
        const date = new Date(notif.timestamp);
        const timeStr = this.formatTime(date);
        const viewedClass = notif.viewed ? 'viewed' : 'unviewed';
        const viewedBadge = notif.viewed ? '✓ Leído' : '● Sin leer';
        const imageHtml = notif.image ? `<img src="${notif.image}" alt="${notif.title}" class="notification-item-image">` : '<div class="notification-item-placeholder">🎮</div>';

        html += `
          <div class="notification-item ${viewedClass}" onclick="notificationCenter.markAsViewed('${notif.gameId}'); window.location.href='PS-Details.html?id=${notif.gameId}'">
            <div class="notification-item-media">
              ${imageHtml}
            </div>
            <div class="notification-item-body">
              <div class="notification-item-header">
                <strong>${notif.title}</strong>
                <span class="notification-item-viewed ${viewedClass}-badge">${viewedBadge}</span>
              </div>
              <p>${notif.message}</p>
              <div class="notification-item-footer">
                <small>${timeStr}</small>
                ${notif.updateCount > 1 ? `<span class="update-count">+${notif.updateCount}</span>` : ''}
              </div>
            </div>
          </div>
        `;
      });
    }

    html += `
      </div>
      <div class="notification-panel-footer">
        <button onclick="notificationCenter.markAllAsViewedManual()" class="notification-action-btn mark-read-btn" title="Marcar todo como leído">
          <i class="fa-solid fa-check-double"></i> Marcar leído
        </button>
        <button onclick="notificationCenter.clearAll()" class="notification-action-btn clear-btn" title="Eliminar todas las notificaciones">
          <i class="fa-solid fa-trash"></i> Limpiar
        </button>
      </div>
    `;

    return html;
  }

  /**
   * Formatear tiempo relativo
   */
  formatTime(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Hace unos segundos';
    if (diffMins < 60) return `Hace ${diffMins}m`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    if (diffDays < 7) return `Hace ${diffDays}d`;

    return date.toLocaleDateString('es-ES');
  }

  /**
   * Mostrar/ocultar panel
   */
  togglePanel() {
    const panel = document.getElementById('notification-panel');
    if (!panel) this.createPanel();

    const existingPanel = document.getElementById('notification-panel');
    if (existingPanel.classList.contains('show')) {
      existingPanel.classList.remove('show');
    } else {
      existingPanel.innerHTML = this.renderPanel();
      existingPanel.classList.add('show');
    }
  }

  /**
   * Crear panel DOM
   */
  createPanel() {
    const panel = document.createElement('div');
    panel.id = 'notification-panel';
    panel.className = 'notification-panel';
    document.body.appendChild(panel);

    // Cerrar al hacer clic fuera
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#notification-bell') && 
          !e.target.closest('#notification-panel')) {
        panel.classList.remove('show');
      }
    });
  }

  /**
   * Inicializar sistema
   */
  init() {
    this.updateBellIcon();

    // Escuchar cambios en storage (para multi-tab sync)
    window.addEventListener('storage', (e) => {
      if (e.key === 'ps5-notifications') {
        this.notifications = this.loadNotifications();
        this.updateBellIcon();
      }
    });
  }
}

// Instancia global
const notificationCenter = new NotificationCenter();

// Auto-inicializar cuando DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  console.log('📢 Notification Center inicializado');
  notificationCenter.init();
});

// Exportar para uso global
window.notificationCenter = notificationCenter;
