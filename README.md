# Jarvis Digital Solutions - Catálogo PS3/PS4/PS5

Catálogo unificado de juegos con datos dinámicos, filtros por plataforma, búsqueda avanzada y fichas detalladas.

## ✅ Características Implementadas

### 1. **Consolidación de Plataformas**
- ✅ Games.json unificado: **1,058 juegos** (PS3: 159 + PS4: 291 + PS5: 608)
- ✅ Filtros dinámicos por plataforma en inicio y catálogo
- ✅ Búsqueda global para todas las plataformas

### 2. **UI/UX Mejorada**
- ✅ Barra de filtros por plataforma (Todos, PS3, PS4, PS5) con colores activos
- ✅ Títulos dinámicos según filtro seleccionado
- ✅ Secciones de Destacados y Estrenos actualizables por plataforma
- ✅ Branding unificado "Jarvis Digital Solutions" (removido "PlayStore")

### 3. **Fichas de Detalle (PS-Details.html)**
- ✅ Rating de estrellas (5 estrellas con soporte para media estrella)
- ✅ Preview shelf mejorado (90x120px, efectos hover premium)
- ✅ Modal para vistas previas de imágenes
- ✅ Trailer YouTube integrado y separado de previews
- ✅ Tema claro/oscuro con localStorage

### 4. **Mejoras Frontend**
- ✅ index.html: Filtros por plataforma + descripción general
- ✅ collection-p5.html: Catálogo con búsqueda y filtros
- ✅ PS-Details.html: Ficha completa con rating, previews y trailer
- ✅ detail-beta.html: Diseño alternativo con tres columnas
- ✅ Responsive design para móvil/tablet/desktop

### 5. **Datos & Config**
- ✅ games.json versión 3.0 con soporte PS3/PS4/PS5
- ✅ Config unificado con curation schedule
- ✅ Preview images para juegos (extensible)
- ✅ Data validada sin errores de sintaxis

## 📁 Estructura del Proyecto

```
PS5-COLLECTION/
├── Sony-Web/
│   ├── index.html              # Página inicio con filtros plataforma
│   ├── collection-p5.html      # Catálogo con búsqueda/filtros
│   ├── PS-Details.html         # Ficha detalle (rating, previews, trailer)
│   ├── detail-beta.html        # Diseño alternativo (3 columnas)
│   ├── games.json              # ✅ 1,058 juegos unificados
│   ├── IMG/                    # Imágenes de juegos
│   ├── registro.html           # Formulario registro
│   └── ...
├── rescaner-DLPS/
│   ├── ps3_games.json          # ✅ Consolidado
│   ├── ps4_games.json          # ✅ Consolidado
│   ├── consolidate_games.py    # Script consolidación
│   └── ...
├── netlify/
│   └── functions/              # Backend (login, register, activate)
├── scripts/
│   ├── auto_curate.py          # Curación IA semanal
│   └── ...
└── .github/workflows/          # GitHub Actions para auto-deploy

```

## 🚀 Cómo Usar

### 1. **Navegar Localmente**
Abre `Sony-Web/index.html` o `Sony-Web/collection-p5.html` en el navegador para ver el catálogo completo con filtros.

### 2. **Cambiar Plataforma**
- Usa los botones "Todos / PS5 / PS4 / PS3" en la sección de filtros
- Los juegos, estrenos y destacados se actualizan dinámicamente
- La búsqueda global funciona en todas las plataformas

### 3. **Ver Detalle de un Juego**
- Haz clic en cualquier juego para abrir `PS-Details.html?id=GAME_ID`
- Verás: rating, precio, trailer, preview images, especificaciones, features

### 4. **Cambiar Tema**
- Botón sol/luna en navbar para alternar claro/oscuro
- Preferencia guardada en localStorage

## 📊 Validación de Datos

✅ **games.json Consolidado**
- Versión 3.0 con 1,058 juegos (PS3, PS4, PS5)
- Validación JSON: ✅ Sin errores de sintaxis
- Estructura: config + games object
- Duplicados evitados: IDs únicos

✅ **HTML/CSS/JS**
- index.html: ✅ Sin errores
- collection-p5.html: ✅ Sin errores
- PS-Details.html: ✅ Sin errores (incluye rating + preview shelf mejorado)

✅ **Funcionalidad**
- Filtros por plataforma: ✅ Funcionando
- Búsqueda global: ✅ Funcionando
- Tema claro/oscuro: ✅ Funcionando y persistente
- Fichas detalle: ✅ Cargando correctamente

## 🔄 Cómo Actualizar Netlify

```bash
cd D:\Proyecto\PS5-COLLECTION
git add .
git commit -m "Consolidar PS3+PS4+PS5, agregar filtros plataforma, mejorar UI/branding"
git push origin main
```

Netlify hará deploy automático cuando detecte cambios en `main`.

## 📝 Curación Automática Semanal

El script `scripts/auto_curate.py` ejecuta cada semana (GitHub Actions):
- Actualiza secciones de Destacados, Estrenos, Banners
- Guarda selección actual en `config.curationSchedule.current`
- Previsión de próxima semana en `config.curationSchedule.next`

Para ejecutar manualmente:

```bash
python scripts/auto_curate.py
```

## 🎮 Próximas Mejoras Opcionales

- [ ] Agregar filtro por género en catálogo
- [ ] Expandir previewImages en más juegos
- [ ] Agregar integración con API de precios
- [ ] Crear dashboard de estadísticas
- [ ] PWA (offline support)

## 📞 Soporte

## Cómo actualizar Netlify

1. Hacer cambios locales en el proyecto.
2. Agregar y confirmar los cambios con Git:

```bash
cd D:\Proyecto\PS5-COLLECTION
git add .
git commit -m "Actualizo sitio con compatibilidad IA y ajustes de Netlify"
git push origin main
```

3. Si el repo está conectado en Netlify a la rama `main`, Netlify hará el deploy automático.

## Ver el estado actual

- La rama actual es `main`.
- El repo ya está conectado a `origin/main`.
- `netlify.toml` ya está creado para publicar `Sony-Web`.

## Nota

Si no ves los cambios en Netlify inmediatamente, revisa el deploy en el panel de Netlify; puede tardar unos minutos en finalizar.

## Verificación de la curación IA

El script `scripts/auto_curate.py` actualiza `Sony-Web/games.json` con la selección actual y una previsión de la próxima semana.

Para revisar cómo quedó la curación en local:

1. Ejecuta:
```bash
cd D:\Proyecto\PS5-COLLECTION
python scripts/auto_curate.py
```
2. Observa el resumen en pantalla:
   - `Banners:` → banners actuales
   - `Featured:` → destacados actuales
   - `Premieres:` → estrenos actuales
   - `Siguiente semana (previsión):` → los próximos picks sugeridos

3. En `Sony-Web/games.json` revisa el objeto `config.curationSchedule`:
   - `current` → selección actual
   - `next` → previsión para la siguiente semana

4. Si estás listo, confirma y sube:
```bash
git add Sony-Web/games.json
git commit -m "Actualizo curación IA y previsión semanal"
git push origin main
```

Netlify actualizará después del deploy con la nueva selección de curación.
