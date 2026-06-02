/**
 * SISTEMA DE AUTO-SYNC INTELIGENTE CON CHANGELOG
 * Detecta cambios, nuevos títulos y evita duplicados
 */

class AutoSyncChangelogSystem {
  constructor() {
    this.changelogCache = {}; // Cache del changelog
    this.gamesCache = {}; // Cache de games.json
    this.pollingInterval = 10000; // Revisar cada 10 segundos
    this.pollingTimer = null;
    this.enableAutoSync = true;
    this.lastChangelogVersion = 0;
    this.processedChanges = this.loadProcessedChanges(); // Cargar desde localStorage
  }

  /**
   * Cargar changeKeys procesadas desde localStorage
   */
  loadProcessedChanges() {
    try {
      const stored = localStorage.getItem('ps5-processed-changes');
      return new Set(stored ? JSON.parse(stored) : []);
    } catch {
      return new Set();
    }
  }

  /**
   * Guardar changeKeys procesadas en localStorage
   */
  saveProcessedChanges() {
    try {
      localStorage.setItem('ps5-processed-changes', JSON.stringify(Array.from(this.processedChanges)));
    } catch (error) {
      console.error('Error guardando processed changes:', error);
    }
  }

  /**
   * Cargar games.json con datos completos
   */
  async loadGames() {
    try {
      const response = await fetch(`./games.json?t=${Date.now()}&r=${Math.random()}`, {
        headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' }
      });
      
      if (!response.ok) return {};
      const data = await response.json();
      // games.json tiene estructura { config: {...}, games: {game-id: {...}, ...} }
      this.gamesCache = data.games || {};
      return this.gamesCache;
    } catch (error) {
      console.error('❌ Error cargando games.json:', error);
      return {};
    }
  }

  /**
   * Cargar changelog (siempre fresco)
   */
  async loadChangelog() {
    try {
      const response = await fetch(`./games-changelog.json?t=${Date.now()}&r=${Math.random()}`, {
        headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' }
      });
      
      if (!response.ok) return null;
      return await response.json();
    } catch (error) {
      console.error('❌ Error cargando changelog:', error);
      return null;
    }
  }

  /**
   * Detectar cambios comparando versiones
   */
  detectChanges(changelog) {
    if (!changelog || !changelog.games) return [];

    const changes = [];
    const currentTime = new Date().toISOString();

    for (const [gameId, entry] of Object.entries(changelog.games)) {
      // Crear clave única para este cambio
      const changeKey = `${gameId}-v${entry.version}-${entry.hash}`;

      // Si ya procesamos este cambio, ignorar
      if (this.processedChanges.has(changeKey)) {
        continue;
      }

      // Detectar tipo de cambio
      let changeType = 'unknown';
      let isNew = false;

      if (entry.isNew) {
        changeType = 'new';
        isNew = true;
      } else if (entry.changeCount > 0) {
        changeType = 'updated';
      }

      if (changeType !== 'unknown') {
        changes.push({
          gameId,
          ...entry,
          changeType,
          isNew,
          changeKey
        });

        // Marcar como procesado y guardar
        this.processedChanges.add(changeKey);
        this.saveProcessedChanges(); // GUARDAR EN LOCALSTORAGE
      }
    }

    return changes;
  }

  /**
   * Procesar cambios detectados
   */
  async processChanges(changes, changelog) {
    if (changes.length === 0) return;

    console.log(`\n📊 DETECTADOS ${changes.length} CAMBIOS:`);
    console.log('═'.repeat(60));

    for (const change of changes) {
      await this.notifyChange(change, changelog);
    }
  }

  /**
   * Notificar un cambio específico
   */
  async notifyChange(change, changelog) {
    const { gameId, changeType, isNew, version, changedFields, lastChanged } = change;

    // Obtener datos COMPLETOS del juego desde gamesCache
    const fullGameData = this.gamesCache[gameId] || {};

    console.log(`\n   ${isNew ? '🆕' : '🔄'} ${gameId.toUpperCase()}`);
    console.log(`      Tipo: ${changeType === 'new' ? 'NUEVO TÍTULO' : 'CAMBIO'}`);
    console.log(`      Versión: ${version}`);

    if (changedFields && changedFields.length > 0) {
      console.log(`      Cambios: ${changedFields.join(', ')}`);
    }

    // Agregar a notification center
    if (typeof notificationCenter !== 'undefined') {
      // Determinar si mostrar toast: Solo si NO existe notificación previa (es realmente nuevo)
      const existsInNotifications = gameId in notificationCenter.notifications;
      const showToast = !existsInNotifications;

      // Pasar datos completos del juego (incluye image, bannerImage, etc)
      const notificationData = {
        title: fullGameData.title || gameId,
        image: fullGameData.image,
        bannerImage: fullGameData.bannerImage,
        previewImages: fullGameData.previewImages,
        note: { title: isNew ? '🆕 Nuevo título agregado' : `Actualización #${version}` },
        lastContentUpdate: lastChanged,
        isNewGame: isNew
      };

      notificationCenter.addNotification(gameId, notificationData, showToast);

      console.log(`      ✓ Notificación registrada${showToast ? ' (Toast mostrado)' : ' (actualización silenciosa)'}`);
    }
  }

  /**
   * Revisión principal de changelog
   */
  async checkForUpdates() {
    try {
      // Cargar games.json si no está en cache
      if (Object.keys(this.gamesCache).length === 0) {
        await this.loadGames();
      }

      const changelog = await this.loadChangelog();

      if (!changelog) {
        console.log('⚠️ No se pudo cargar changelog');
        return;
      }

      console.log(`🔍 REVISION #${Math.floor(Date.now() / 10000)}`);
      console.log(`   Changelog: ${changelog.totalGames} juegos, v${changelog.version}`);

      // Detectar cambios
      const changes = this.detectChanges(changelog);

      if (changes.length === 0) {
        console.log(`   ✓ Sin cambios nuevos`);
      } else {
        console.log(`   ✨ ${changes.length} CAMBIO(S) DETECTADO(S)`);
        await this.processChanges(changes, changelog);
        
        // Mostrar resumen
        const newGames = changes.filter(c => c.isNew).length;
        const updatedGames = changes.filter(c => !c.isNew).length;
        
        console.log('\n' + '═'.repeat(60));
        console.log(`📊 RESUMEN: ${newGames} nuevos, ${updatedGames} actualizados`);
        console.log('═'.repeat(60) + '\n');
      }

    } catch (error) {
      console.error('❌ Error en auto-sync:', error);
    }
  }

  /**
   * Iniciar el sistema
   */
  start() {
    if (!this.enableAutoSync) {
      console.log('⚠️ Auto-sync deshabilitado');
      return;
    }

    console.log('✨ Auto-Sync Changelog iniciado - Revisando cada 10 segundos');

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
   * Obtener status
   */
  getStatus() {
    return {
      enabled: this.enableAutoSync,
      pollingInterval: this.pollingInterval,
      isRunning: this.pollingTimer !== null,
      processedChanges: this.processedChanges.size
    };
  }

  /**
   * Limpiar cambios procesados (para testing)
   */
  clearProcessedChanges() {
    this.processedChanges.clear();
    console.log('✓ Cambios procesados limpiados');
  }
}

// Instancia global
const autoSyncChangelogSystem = new AutoSyncChangelogSystem();

// Auto-inicializar cuando DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  console.log('🔧 DOMContentLoaded: Inicializando Auto-Sync Changelog...');

  if (typeof notificationCenter === 'undefined') {
    console.warn('⚠️ notificationCenter NO disponible, esperando 100ms...');
    setTimeout(() => {
      autoSyncChangelogSystem.start();
    }, 100);
  } else {
    console.log('✅ notificationCenter disponible');
    autoSyncChangelogSystem.start();
  }
});

// Exportar para uso manual
window.autoSyncChangelogSystem = autoSyncChangelogSystem;
