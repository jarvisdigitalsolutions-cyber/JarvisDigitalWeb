/**
 * DEBUG HELPER - Auto-Sync Changelog
 * Copiar y pegar en consola (F12) para debuggear
 */

function debugChangelog() {
  console.log('🔍 DEBUGGING - AUTO-SYNC CHANGELOG SYSTEM\n');
  
  console.log('1️⃣ COMPONENTES DISPONIBLES:');
  console.log(`   notificationCenter: ${typeof notificationCenter !== 'undefined' ? '✅' : '❌'}`);
  console.log(`   autoSyncChangelogSystem: ${typeof autoSyncChangelogSystem !== 'undefined' ? '✅' : '❌'}`);
  
  console.log('\n2️⃣ STATUS DEL SISTEMA:');
  const status = autoSyncChangelogSystem.getStatus();
  console.log(`   Enabled: ${status.enabled}`);
  console.log(`   Running: ${status.isRunning}`);
  console.log(`   Polling: ${status.pollingInterval}ms`);
  console.log(`   Cambios procesados: ${status.processedChanges}`);
  
  console.log('\n3️⃣ CAMBIOS REGISTRADOS:');
  console.log(`   Total: ${autoSyncChangelogSystem.processedChanges.size}`);
  const processed = Array.from(autoSyncChangelogSystem.processedChanges).slice(0, 5);
  processed.forEach(p => console.log(`   • ${p}`));
  
  console.log('\n4️⃣ NOTIFICACIONES EN LOCALSTORAGE:');
  const notifs = notificationCenter.getAllNotifications();
  console.log(`   Total: ${notifs.length}`);
  if (notifs.length > 0) {
    notifs.slice(0, 3).forEach(n => {
      const status = n.viewed ? '✓' : '●';
      console.log(`   ${status} ${n.title} (${n.isNewGame ? '🆕' : '🔄'})`);
    });
  }
  
  console.log('\n5️⃣ CONTROLES:');
  console.log(`   loadChangelog() - Cargar changelog una vez`);
  console.log(`   autoSyncChangelogSystem.checkForUpdates() - Revisar cambios`);
  console.log(`   autoSyncChangelogSystem.clearProcessedChanges() - Limpiar registro`);
  console.log(`   autoSyncChangelogSystem.stop() - Detener auto-sync`);
  console.log(`   autoSyncChangelogSystem.start() - Reanudar auto-sync`);
  
  console.log('\n6️⃣ PARA VER CHANGELOG ACTUAL:');
  console.log(`   const log = await fetch('./games-changelog.json').then(r => r.json());`);
  console.log(`   console.table(log.games);`);
  
  console.log('\n');
}

// Función auxiliar para cargar changelog
window.loadChangelog = async function() {
  const response = await fetch(`./games-changelog.json?t=${Date.now()}`);
  const changelog = await response.json();
  console.log('📋 Changelog cargado:');
  console.log(`   Versión: ${changelog.version}`);
  console.log(`   Total juegos: ${changelog.totalGames}`);
  console.log(`   Total cambios: ${changelog.totalChanges}`);
  console.log(`   Última actualización: ${changelog.lastUpdated}`);
  console.log('\n   Juegos:');
  Object.entries(changelog.games).slice(0, 5).forEach(([id, entry]) => {
    const type = entry.isNew ? '🆕' : '🔄';
    console.log(`   ${type} ${id} (v${entry.version}, hash: ${entry.hash})`);
  });
  return changelog;
};

// Exponer en window
window.debugChangelog = debugChangelog;
console.log('✅ Debug helper cargado. Escribe: debugChangelog()');
