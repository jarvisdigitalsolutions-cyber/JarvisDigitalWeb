/**
 * SISTEMA DE AUTO-SINCRONIZACIÓN DE CAMBIOS
 * Detecta cambios en games.json en tiempo real sin recargar la página
 */

class AutoSyncNotesSystem {
  constructor() {
    this.gamesCache = {}; // Cache de última versión conocida
    this.pollingInterval = 10000; // Revisar cada 10 segundos
    this.pollingTimer = null;
    this.enableAutoSync = true;
  }

  /**
   * Obtener hash simple de un objeto para detectar cambios
   */
  getObjectHash(obj) {
    const str = JSON.stringify(obj);
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(16);
  }

  /**
   * Comparar si un juego ha sido actualizado
   */
  hasGameChanged(gameId, newGame) {
    const newHash = this.getObjectHash(newGame);

    if (!this.gamesCache[gameId]) {
      // Primera vez que vemos este juego
      this.gamesCache[gameId] = {
        hash: newHash,
        lastUpdate: newGame.lastContentUpdate,
        data: JSON.parse(JSON.stringify(newGame))
      };
      return false; // No es cambio, es primer cacheo
    }

    const oldHash = this.gamesCache[gameId].hash;
    const changed = oldHash !== newHash;

    if (changed) {
      console.log(`   ↳ Hash viejo: ${oldHash}`);
      console.log(`   ↳ Hash nuevo: ${newHash}`);
      console.log(`   ↳ CAMBIO CONFIRMADO`);

      this.gamesCache[gameId] = {
        hash: newHash,
        lastUpdate: newGame.lastContentUpdate,
        data: JSON.parse(JSON.stringify(newGame))
      };
    }

    return changed;
  }

  /**
   * Recargar games.json y detectar cambios
   */
  async checkForUpdates() {
    try {
      // Cache-busting agresivo: agregar múltiples parámetros
      const timestamp = Date.now();
      const random = Math.random();
      const response = await fetch(`./games.json?t=${timestamp}&r=${random}`, {
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      });
      
      if (!response.ok) {
        console.warn('⚠️ No se pudo cargar games.json');
        return;
      }

      const gamesData = await response.json();
      const games = gamesData.games || {};

      console.log(`🔍 Auto-Sync: Revisando ${Object.keys(games).length} juegos...`);

      let changesDetected = 0;

      // Revisar cada juego
      for (const [gameId, gameData] of Object.entries(games)) {
        if (this.hasGameChanged(gameId, gameData)) {
          changesDetected++;
          console.log(`✨ CAMBIO DETECTADO EN: ${gameId}`);
          // Juego ha cambiado - actualizar interfaz
          this.notifyGameUpdate(gameId, gameData);
        }
      }

      if (changesDetected === 0) {
        console.log(`✓ Sin cambios detectados`);
      } else {
        console.log(`📊 Total cambios detectados: ${changesDetected}`);
      }
    } catch (error) {
      console.error('❌ Error en auto-sync:', error);
    }
  }

  /**
   * Mostrar notificación cuando hay cambio
   */
  notifyGameUpdate(gameId, gameData) {
    console.log(`\n📢 ╔════════════════════════════════════════════╗`);
    console.log(`   ║ NOTIFICACIÓN DE CAMBIO DETECTADO           ║`);
    console.log(`   ╚════════════════════════════════════════════╝`);
    console.log(`   Game ID: ${gameId}`);
    console.log(`   Título: ${gameData.title}`);
    console.log(`   Timestamp: ${gameData.lastContentUpdate}`);

    // Agregar a notification center
    if (typeof notificationCenter !== 'undefined') {
      console.log(`   ✓ Agregando a notificationCenter...`);
      notificationCenter.addNotification(gameId, gameData);
      console.log(`   ✓ Notificación guardada en localStorage`);
      console.log(`   ✓ Bell icon debe actualizarse`);
    } else {
      console.warn(`   ⚠️ notificationCenter NO disponible`);
    }

    // Crear notificación visual de recarga
    const notification = document.createElement('div');
    notification.className = 'auto-sync-notification';
    notification.innerHTML = `
      <div class="notification-content">
        <i class="fa-solid fa-sparkles"></i>
        <div class="notification-text">
          <strong>${gameData.title}</strong> ha sido actualizado
          <small>${gameData.note?.title || 'Nueva actualización disponible'}</small>
        </div>
        <button class="notification-reload" onclick="window.location.reload()">
          <i class="fa-solid fa-rotate-right"></i> Actualizar
        </button>
      </div>
    `;

    document.body.appendChild(notification);

    // Auto-recargar después de 5 segundos para que vea la notificación
    const reloadTimer = setTimeout(() => {
      console.log('   ✓ Recargando página en 5 segundos...');
      window.location.reload();
    }, 5000);

    // Si hace clic en Actualizar, recargar inmediatamente
    const reloadBtn = notification.querySelector('.notification-reload');
    if (reloadBtn) {
      reloadBtn.addEventListener('click', () => {
        clearTimeout(reloadTimer);
        notification.remove();
      });
    }

    // Reproducir sonido
    this.playNotificationSound();
    console.log(`\n`);
  }

  /**
   * Actualizar o crear badge en la tarjeta del juego
   */
  updateCardBadge(gameId, gameData) {
    // Buscar todas las tarjetas con este gameId
    const cards = document.querySelectorAll(
      `[data-game-id="${gameId}"], [data-id="${gameId}"]`
    );

    cards.forEach(card => {
      // Remover badge antiguo si existe
      const oldBadge = card.querySelector('.update-badge');
      if (oldBadge) oldBadge.remove();

      // Crear y añadir nuevo badge
      const badge = document.createElement('div');
      badge.className = 'update-badge new';
      badge.dataset.gameId = gameId;
      badge.innerHTML = '✨ ACTUALIZADO';

      card.style.position = 'relative';
      card.prepend(badge);

      // Auto-remover después de 30 segundos
      setTimeout(() => {
        badge.classList.add('dismissing');
        setTimeout(() => badge.remove(), 500);
      }, 30000);
    });
  }

  /**
   * Reproducir sonido de notificación (opcional)
   */
  playNotificationSound() {
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      // Sonido: do-mi (happy chime)
      oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // Do
      oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1); // Mi
      
      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.3);
    } catch (e) {
      // Silent fail - algunos navegadores no permiten AudioContext
    }
  }

  /**
   * Iniciar el sistema de auto-sincronización
   */
  start() {
    if (!this.enableAutoSync) {
      console.log('Auto-sync deshabilitado');
      return;
    }

    console.log('✨ Auto-Sync iniciado - Revisando cada 10 segundos');
    
    // Primera revisión inmediata
    this.checkForUpdates();

    // Revisar periódicamente
    this.pollingTimer = setInterval(() => {
      this.checkForUpdates();
    }, this.pollingInterval);
  }

  /**
   * Detener el sistema
   */
  stop() {
    if (this.pollingTimer) {
      clearInterval(this.pollingTimer);
      this.pollingTimer = null;
      console.log('Auto-Sync detenido');
    }
  }

  /**
   * Cambiar intervalo de polling
   */
  setPollingInterval(ms) {
    this.pollingInterval = ms;
    if (this.pollingTimer) {
      this.stop();
      this.start();
    }
  }

  /**
   * Obtener status actual
   */
  getStatus() {
    return {
      enabled: this.enableAutoSync,
      pollingInterval: this.pollingInterval,
      isRunning: this.pollingTimer !== null,
      cachedGames: Object.keys(this.gamesCache).length
    };
  }
}

// Instancia global
const autoSyncSystem = new AutoSyncNotesSystem();

// Auto-iniciar cuando DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  console.log('🔧 DOMContentLoaded: Inicializando Auto-Sync...');
  
  // Verificar que notificationCenter existe
  if (typeof notificationCenter === 'undefined') {
    console.warn('⚠️ notificationCenter NO disponible, esperando 100ms...');
    setTimeout(() => {
      autoSyncSystem.start();
    }, 100);
  } else {
    console.log('✅ notificationCenter disponible');
    autoSyncSystem.start();
  }
});

// Exportar para uso manual
window.autoSyncSystem = autoSyncSystem;
