/**
 * DEBUG HELPER - Copiar y pegar esto en la consola (F12) para testear
 */

function debugAutoSync() {
  console.log('🔧 DEBUGGING AUTO-SYNC SYSTEM\n');
  
  console.log('1️⃣ ESTADO GENERAL:');
  console.log('   notificationCenter:', typeof notificationCenter !== 'undefined' ? '✅ Disponible' : '❌ NO disponible');
  console.log('   autoSyncSystem:', typeof autoSyncSystem !== 'undefined' ? '✅ Disponible' : '❌ NO disponible');
  
  console.log('\n2️⃣ STATUS AUTO-SYNC:');
  const status = autoSyncSystem.getStatus();
  console.log(`   Enabled: ${status.enabled}`);
  console.log(`   Running: ${status.isRunning}`);
  console.log(`   Polling: ${status.pollingInterval}ms`);
  console.log(`   Cached Games: ${status.cachedGames}`);
  
  console.log('\n3️⃣ NOTIFICACIONES GUARDADAS:');
  const notifs = notificationCenter.getAllNotifications();
  if (notifs.length === 0) {
    console.log('   ❌ Sin notificaciones guardadas');
  } else {
    notifs.forEach(n => {
      console.log(`   ${n.viewed ? '✓' : '●'} ${n.title} (${n.timestamp})`);
    });
  }
  
  console.log('\n4️⃣ LOCALSTORAGE:');
  const stored = localStorage.getItem('ps5-notifications');
  console.log(`   ps5-notifications: ${stored ? 'Existe (' + Object.keys(JSON.parse(stored)).length + ' juegos)' : 'NO existe'}`);
  
  console.log('\n5️⃣ CACHE DE AUTO-SYNC:');
  const cacheKeys = Object.keys(autoSyncSystem.gamesCache);
  console.log(`   Total juegos cacheados: ${cacheKeys.length}`);
  if (cacheKeys.includes('elden-ring')) {
    const eldenCache = autoSyncSystem.gamesCache['elden-ring'];
    console.log(`   ✓ Elden Ring encontrado:`);
    console.log(`     - Hash: ${eldenCache.hash}`);
    console.log(`     - Timestamp: ${eldenCache.lastUpdate}`);
  } else {
    console.log(`   ❌ Elden Ring NO está en cache (debería estar)`);
  }
  
  console.log('\n6️⃣ PARA FORZAR CAMBIO MANUALMENTE:');
  console.log(`   autoSyncSystem.checkForUpdates();`);
  
  console.log('\n7️⃣ PARA SIMULAR NOTIFICACIÓN:');
  console.log(`   notificationCenter.addNotification('test-game', {`);
  console.log(`     title: 'Test Game',`);
  console.log(`     note: { title: 'Test notification' },`);
  console.log(`     lastContentUpdate: new Date().toISOString()`);
  console.log(`   });`);
}

// Llamar función
window.debugAutoSync = debugAutoSync;
console.log('✅ Debug helper cargado. Escribe: debugAutoSync()');
