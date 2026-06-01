# FIX: Notificaciones Spam y Viewed Status

## 🐛 Problema Original

**Usuario marcó notificación como leída pero:**
- El toast seguía apareciendo continuamente
- El estado "leído" no se preservaba cuando auto-sync detectaba cambios
- Incluso borrando localStorage, seguía saliendo

**Causa Raíz:**
```javascript
// ANTES - PROBLEMA:
this.notifications[gameId].viewed = false; // ← SIEMPRE reseteaba a false
```

Cuando auto-sync llamaba `addNotification()` nuevamente, **sobrescribía `viewed=true`** que el usuario había marcado, resetándolo a `false`.

---

## ✅ Solución Implementada

### 1. Preservar Estado Viewed del Usuario

**Archivo:** `notification-center.js`

```javascript
// DESPUÉS - CORRECTO:
} else {
  // Actualizar notificación existente - PRESERVAR viewed status del usuario
  const wasViewed = this.notifications[gameId].viewed;
  this.notifications[gameId].timestamp = gameData.lastContentUpdate;
  this.notifications[gameId].image = image;
  this.notifications[gameId].message = gameData.note?.title || 'Actualización disponible';
  this.notifications[gameId].viewed = wasViewed; // ← MANTIENE estado anterior
  this.notifications[gameId].updateCount++;
}
```

**Cambios:**
- Guardar el valor actual de `viewed` antes de actualizar
- Restaurar ese valor después (no resetearlo a `false`)
- El usuario que marcó como leído SIGUE siendo leído

---

### 2. Toast Solo en Cambios Verdaderamente Nuevos

**Archivo:** `notification-center.js`

```javascript
addNotification(gameId, gameData, showToastNotification = true) {
  // ... resto del código ...
  
  if (showToastNotification) {
    this.showToast(gameId, gameData); // ← Solo si se solicita
  }
}
```

**Cambios:**
- Agregué parámetro `showToastNotification` (default: true)
- Auto-sync controla si debe mostrar toast o no

---

### 3. Auto-Sync Inteligente - Toast Solo en Nuevos

**Archivo:** `auto-sync-changelog.js`

```javascript
async notifyChange(change, changelog) {
  // ...
  
  // Determinar si mostrar toast: Solo si NO existe notificación previa
  const existsInNotifications = gameId in notificationCenter.notifications;
  const showToast = !existsInNotifications;

  notificationCenter.addNotification(gameId, {
    // ... datos ...
  }, showToast); // ← Pasa true/false según si es nuevo
  
  console.log(`✓ Notificación registrada${showToast ? ' (Toast mostrado)' : ' (actualización silenciosa)'}`);
}
```

**Lógica:**
- Primera vez que se detecta un juego → `showToast = true` ✨
- Actualizaciones posteriores → `showToast = false` (silencioso) 🔇
- Toast SOLO aparece cuando es realmente nuevo

---

## 🔄 Flujo Completo - Ahora Funciona Así

```
TIME 0s:
└─ Auto-Sync detecta Crimson Desert v3 por PRIMERA VEZ
   └─ notificationCenter.notifications NO tiene "crimson-desert" aún
   └─ showToast = true
   └─ Toast aparece con imagen ✨
   └─ viewed = false (primera vez)
   └─ Se guarda en localStorage

TIME 10s:
└─ Usuario marca como leído
   └─ markAllAsViewedManual()
   └─ viewed = true
   └─ Se guarda en localStorage

TIME 20s:
└─ Auto-Sync hace nueva revisión
   └─ Detecta mismo cambio: Crimson Desert v3
   └─ changeKey ya está en processedChanges Set
   └─ ✓ Se ignora (no llama notifyChange)

TIME 30s:
└─ Se actualiza a Crimson Desert v4
   └─ changeKey diferente: "crimson-desert-v4-newHash"
   └─ notificationCenter.notifications SÍ tiene "crimson-desert" (marcado leído)
   └─ showToast = false (actualización silenciosa)
   └─ Actualiza timestamp/imagen
   └─ PRESERVA viewed = true ✓
   └─ NO muestra toast

TIME 40s:
└─ Usuario va a otra página
   └─ DOMContentLoaded → markAllAsViewed()
   └─ viewed = true (ya lo era)
   └─ Bell badge desaparece correctamente
```

---

## 📊 Estados Posibles de Notificación

| Escenario | viewed | Toast | Resultado |
|-----------|--------|-------|-----------|
| **Nuevo juego, primera vez** | false | ✨ SÍ | Usuario ve toast bonito |
| **Usuario marca leído** | true | - | Desaparece de panel |
| **Auto-sync actualiza juego conocido** | true ↔ true | 🔇 NO | Silencioso, preserva leído |
| **Usuario recarga página** | true | - | Auto-marca al entrar |
| **Nuevo juego completamente nuevo (v4+)** | true→false | 🔇 NO | Actualización silenciosa |

---

## 🎯 Beneficios

✅ **Usuario marca como leído → SE MANTIENE leído**
✅ **Toast solo aparece en cambios realmente nuevos**
✅ **Sin spam de notificaciones repetidas**
✅ **Actualización silenciosa después de primera notificación**
✅ **Estado se preserva en localStorage**
✅ **Auto-mark al entrar página sigue funcionando**

---

## 📱 Caso de Uso Real

```
Lunes 9:00am:
  Crimson Desert v3 se agrega
  → Toast muestra "Actualización disponible"
  → Usuario ve y marca como leído
  
Lunes 9:05am:
  Usuario recarga página
  → Badge desaparece automáticamente

Lunes 2:00pm:
  Crimson Desert se actualiza a v4
  → Toast NO aparece (actualización silenciosa)
  → Panel mostrará "✓ Leído" pero timestamp actualizado
  
Lunes 2:05pm:
  Usuario abre juego
  → Verá cambios nuevos en detalle sin notificaciones agresivas
```

---

## 🧪 Cómo Probar

### Test 1: Verificar Preservación de Viewed

```bash
# 1. Generar notificación
python update_game_timestamp.py crimson-desert

# 2. Abrir sitio, esperar 10s, ver toast
# 3. Click bell icon
# 4. Click "Marcar leído"
# 5. Abiir DevTools Console:
notificationCenter.getUnviewedCount()  # Debe retornar 0

# 6. Generar actualización nueva
python update_game_timestamp.py crimson-desert

# 7. Esperar 10s
# 8. Verificar que NO hay toast nuevo
# 9. Revisar console: "actualización silenciosa"
```

### Test 2: Verificar Toast Solo Nuevo

```bash
# Abrir console antes de hacer algo
console.clear()

# Generar juego nuevo
python update_game_timestamp.py elden-ring

# Ver:
# [TOAST APARECE] ✨
# [Console] "Toast mostrado"

# Esperar 10s, generar actualización nueva
python update_game_timestamp.py elden-ring

# Ver:
# [NO TOAST] 🔇
# [Console] "actualización silenciosa"
```

---

## 📋 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `notification-center.js` | Preservar viewed, parámetro showToastNotification |
| `auto-sync-changelog.js` | Lógica inteligente showToast basada en existencia |

---

## 🚀 Resultado Final

Usuario ahora tiene experiencia limpia:
- ✨ Notificaciones hermosas con imagen en cambios nuevos
- 🔇 Sin spam después de marcar como leído
- ✅ Estado se mantiene al recargar
- 🎯 Control total: Puede ignorar o marcar según quiera
