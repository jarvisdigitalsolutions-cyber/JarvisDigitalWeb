# Sistema de Actualizaciones de Notas - Documentación

## Descripción General

El **Sistema de Actualizaciones de Notas** (Notes Update System) muestra un badge visual (✨ ACTUALIZADO) en tarjetas de juegos cuando tienen notas nuevas o actualizadas. El badge desaparece automáticamente o cuando el usuario interactúa con la tarjeta.

## Estructura JSON Requerida

Cada juego en `games.json` debe tener esta estructura mínima:

```json
{
  "id": "game-id",
  "title": "Game Title",
  "lastContentUpdate": "2026-06-01T14:32:00Z",
  "hasNewUpdates": true,
  
  "note": {
    "title": "Título de la nota",
    "author": "Autor/Equipo",
    "noteId": "UNIQUE-ID",
    "info": "Descripción de la actualización",
    "link": "https://...",
    "timestamp": "2026-06-01T14:32:00Z",
    "version": "X.X.X",
    "isNew": true
  },
  
  "technicalNotes": [
    {
      "id": "tech-note-1",
      "title": "Título técnico",
      "author": "Autor",
      "info": "Información técnica",
      "link": "https://...",
      "badge": "BADGE-NAME",
      "timestamp": "2026-06-01T14:32:00Z"
    }
  ]
}
```

## Campos Importantes

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `lastContentUpdate` | ISO String | Fecha/hora de última actualización (formato ISO 8601) |
| `hasNewUpdates` | Boolean | Si true, muestra el badge en la tarjeta |
| `note.timestamp` | ISO String | Cuándo se actualizó la nota principal |
| `note.isNew` | Boolean | Indica si la nota es nueva (opcional) |
| `technicalNotes[].timestamp` | ISO String | Cuándo se publicó cada nota técnica |

## Cómo Funciona

1. **Detección**: El sistema carga `games.json` y busca juegos con `hasNewUpdates: true`
2. **Visualización**: Muestra el badge en todas las tarjetas (mini-cards, bento-items, premiere-cards)
3. **Persistencia**: Guarda en `localStorage` qué badges ya fueron vistos
4. **Auto-ocultar**: El badge desaparece después de 30 segundos o cuando el usuario interactúa

## Integración en HTML

### 1. Mini-Cards
```html
<div class="mini-card" data-game-id="game-id">
  <!-- contenido de la tarjeta -->
</div>
```

### 2. Bento-Items
```html
<div class="bento-item" data-game-id="game-id">
  <!-- contenido de la tarjeta -->
</div>
```

### 3. Premiere-Cards
```html
<div class="premiere-card" data-game-id="game-id">
  <!-- contenido de la tarjeta -->
</div>
```

## API del Sistema

### Métodos Disponibles

```javascript
// Inicializar manualmente
notesUpdateSystem.init(gamesData);

// Marcar un juego como actualizado (para testing)
notesUpdateSystem.markAsUpdated('game-id');

// Limpiar todas las actualizaciones vistas
notesUpdateSystem.clearDismissed();

// Acceder a los datos
console.log(notesUpdateSystem.dismissedUpdates);
```

## Personalización

### Cambiar duración del badge
```javascript
notesUpdateSystem.updateBadgeDuration = 60000; // 60 segundos
```

### Cambiar formato de fecha
Editar el método `formatDate()` en `notes-update-system.js`:
```javascript
formatDate(isoString) {
  // Tu lógica de formato personalizado
}
```

### Cambiar estilos del badge
Editar `notes-update-system.css`:
```css
.update-badge {
  background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
  /* Personalizar colores, sombras, etc */
}
```

## Ejemplo Completo - Spider-Man 2

```json
{
  "spider-man-2": {
    "id": "spider-man-2",
    "title": "Spider-Man 2",
    "platform": "PS5",
    "release": "2023",
    "rating": "4.9",
    "price": 59.99,
    
    "lastContentUpdate": "2026-06-01T14:32:00Z",
    "hasNewUpdates": true,
    
    "note": {
      "title": "Actualización de simbionte y rendimiento",
      "author": "Equipo Insomniac / Marvel Games",
      "noteId": "SM2-NOTE-2025",
      "info": "Parche 2.001 mejora la tasa de fotogramas, combates mejorados contra simbiontes...",
      "link": "https://insomniac.games/spiderman2/parche-notas",
      "timestamp": "2026-06-01T14:32:00Z",
      "version": "2.001.000",
      "isNew": true
    },
    
    "technicalNotes": [
      {
        "id": "ffpkg-v2",
        "title": "Formato de paquete (FFPKG v2)",
        "author": "Insomniac Games",
        "info": "Versión actualizada del paquete con mejor compresión...",
        "link": "https://developer.sony.com/ffpkg-v2",
        "badge": "FFPKG v2",
        "timestamp": "2025-03-15T08:00:00Z"
      }
    ]
  }
}
```

## Testing

### Habilitar badge para testing
```javascript
// En consola del navegador:
notesUpdateSystem.markAsUpdated('spider-man-2');
location.reload();
```

### Ver todos los badges vistos
```javascript
console.log(notesUpdateSystem.dismissedUpdates);
```

### Limpiar historial de badges
```javascript
notesUpdateSystem.clearDismissed();
location.reload();
```

## Animaciones

### Animación de Entrada del Badge
- **Duración**: 600ms
- **Easing**: cubic-bezier(0.22, 0.61, 0.36, 1)
- **Efecto**: Scale + Translate

### Animación de Pulso
- **Duración**: 2 segundos (loop infinito)
- **Efecto**: Glow pulsante

### Animación de Salida
- **Duración**: 500ms
- **Efecto**: Scale + Fade Out

## LocalStorage

El sistema guarda en `dismissedGameUpdates`:
```json
{
  "game-id-1": "2026-06-01T15:00:00Z",
  "game-id-2": "2026-06-01T16:30:00Z"
}
```

## Notas de Desarrollo

- ✅ Compatible con todas las tarjetas (mini, bento, premiere)
- ✅ Respeta localStorage para no molestar al usuario
- ✅ Animaciones suaves y performantes
- ✅ Tooltips con fecha de actualización
- ✅ Auto-remover después de tiempo definido
- ✅ Remover al hacer clic/hover

## Troubleshooting

### El badge no aparece
1. Verificar que `hasNewUpdates: true` en `games.json`
2. Verificar que `data-game-id` coincida con el `id` en JSON
3. Abrir consola y ejecutar: `notesUpdateSystem.clearDismissed()`
4. Recargar página

### El badge desaparece muy rápido
- Cambiar `updateBadgeDuration` en `notes-update-system.js`

### Las fechas no se ven bien
- Editar método `formatDate()` para tu idioma/zona horaria

## Contacto y Soporte

Para reportar errores o sugerencias, revisar la consola del navegador (F12).
