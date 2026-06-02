## 🎮 MULTIPLATFORM CURATION SYSTEM

### 📋 ESTRUCTURA

```
games.json
└── platforms/
    ├── PS5/
    │   ├── homeFeatured     ← ESTÁTICO (no cambia)
    │   ├── popular          ← ESTÁTICO (no cambia)
    │   ├── featured         ← DINÁMICO (cambia cada semana)
    │   ├── premieres        ← DINÁMICO (cambia cada semana)
    │   └── recentReleases   ← DINÁMICO (cambia cada semana)
    │
    ├── PS4/
    │   ├── featured         ← DINÁMICO (mismo que PS5)
    │   ├── premieres        ← DINÁMICO (mismo que PS5)
    │   └── recentReleases   ← DINÁMICO (mismo que PS5)
    │
    └── PS3/
        ├── featured         ← DINÁMICO (mismo que PS5)
        ├── premieres        ← DINÁMICO (mismo que PS5)
        └── recentReleases   ← DINÁMICO (mismo que PS5)
```

### ✅ LO QUE CAMBIA

| Sección | PS5 | PS4 | PS3 | Frecuencia |
|---------|-----|-----|-----|-----------|
| **homeFeatured** | 🔒 Estático | ❌ N/A | ❌ N/A | Nunca |
| **popular** | 🔒 Estático | ❌ N/A | ❌ N/A | Nunca |
| **featured** | ✅ Dinámico | ✅ Dinámico | ✅ Dinámico | Semanalmente |
| **premieres** | ✅ Dinámico | ✅ Dinámico | ✅ Dinámico | Semanalmente |
| **recentReleases** | ✅ Dinámico | ✅ Dinámico | ✅ Dinámico | Semanalmente |
| **upcoming** | ✅ Dinámico | ❌ N/A | ❌ N/A | Semanalmente |
| **all** | ✅ Dinámico | ✅ Dinámico | ✅ Dinámico | Semanalmente |

### 🎯 DECISIONES DE DISEÑO

#### ¿Por qué homeFeatured y popular NO cambian?
- Estos son juegos **seleccionados manualmente** (hand-picked)
- Representan "clásicos" y "mejores juegos" de forma permanente
- Dar estabilidad y confianza al usuario
- Se actualizan manualmente, no automáticamente

#### ¿Por qué featured, premieres, recentReleases cambian?
- Estos **reflejan novedades** y cambios en el catálogo
- featured: Rotación de juegos recomendados (mejor scoring)
- premieres: Próximos lanzamientos (cambia con fechas)
- recentReleases: Últimos lanzados (nuevos cada semana)

#### ¿Por qué PS4 y PS3 usan el mismo criterio?
- **Código compartido**: Mismo algoritmo de scoring
- **Compatibilidad**: Los juegos multi-platform se tratan igual
- **UX consistente**: Usuarios ven selección similar en diferentes plataformas
- **Mantenibilidad**: Un solo sistema de reglas para todas

### 📊 ALGORITMO DE SCORING (Igual para todas las plataformas)

```python
Score = 
  40% × Rating (calidad del juego)
+ 25% × Recency (qué tan reciente es)
+ 15% × Discount (% descuento actual)
+ 15% × Popularity (engagement/búsquedas)
+ 5%  × Exclusive (bonus si es exclusiva)
```

### 🔮 PREDICCIONES

El sistema predice **3 semanas adelante** automáticamente:

```
Hoy (1 Junio)              → Premieres: AC Shadows, Death Stranding 2, etc.
Semana 1 (8 Junio)         → Premieres: Chronoscript, Wolf Among Us 2, etc.
Semana 2 (15 Junio)        → Premieres: GTA VI, etc.
Semana 3 (22 Junio)        → [Sistema recalcula]
```

Almacenado en: `config.curationForecast`

### 🚀 USO

#### Test (sin cambios)
```bash
python scripts/auto_curate_multiplatform.py --dry-run
```

#### Ejecutar (actualiza games.json)
```bash
python scripts/auto_curate_multiplatform.py
```

#### Personalización
```bash
# 2 semanas de predicción (en lugar de 3)
python scripts/auto_curate_multiplatform.py --weeks-forecast 2

# No repetir juegos en 6 semanas (en lugar de 4)
python scripts/auto_curate_multiplatform.py --no-repeat-weeks 6

# 8 featured en lugar de 6
python scripts/auto_curate_multiplatform.py --featured-count 8
```

### 📅 CRONOGRAMA RECOMENDADO

```
Cada LUNES a las 00:00 UTC → python scripts/auto_curate_multiplatform.py
```

GitHub Actions (`.github/workflows/auto-curate.yml`):
```yaml
on:
  schedule:
    - cron: '0 0 * * 1'  # Lunes 00:00 UTC
```

### 📝 EJEMPLO: Cómo cambia el contenido

#### Hoy (1 Junio 2026)
```json
{
  "PS5": {
    "sections": {
      "homeFeatured": ["tlou-3", "gow-ragnarok", ...],      ← NO CAMBIA
      "popular": ["uncharted-4", "batman-arkham-knight", ...], ← NO CAMBIA
      "featured": ["biohazard-re-4", "dragon-quest-iii-hd-2d-remake", ...], ← CAMBIA
      "premieres": ["assassins-creed-shadows", "death-stranding-2", ...], ← CAMBIA
      "recentReleases": ["bye-sweet-carole", "invincible-vs", ...]   ← CAMBIA
    }
  }
}
```

#### Próxima semana (8 Junio 2026)
```json
{
  "PS5": {
    "sections": {
      "homeFeatured": ["tlou-3", "gow-ragnarok", ...],      ← IGUAL
      "popular": ["uncharted-4", "batman-arkham-knight", ...], ← IGUAL
      "featured": ["code-vein-2", "fifa-23", ...],           ← NUEVO
      "premieres": ["chronoscript-the-endless-end", "wolf-among-us-2", ...], ← NUEVO
      "recentReleases": ["ninja-gaiden-2-black", "dragon-quest-vii-reimagined", ...] ← NUEVO
    }
  }
}
```

### 🎯 VENTAJAS

1. ✅ **Multi-plataforma**: PS5, PS4, PS3 cubiertas
2. ✅ **Estabilidad**: homeFeatured y popular son permanentes
3. ✅ **Novedad**: featured, premieres, recientes se actualizan
4. ✅ **Predictibilidad**: Sistema sabe qué vendrá 3 semanas
5. ✅ **Automatización**: Sin intervención manual
6. ✅ **Evita repetición**: No repite juegos en 4 semanas
7. ✅ **Versátil**: Parámetros ajustables

### ⚙️ CONFIGURACIÓN

En `config.json` se guardan:
- `lastCurated`: Timestamp última ejecución
- `curationHistory`: Últimas 52 semanas
- `curationForecast`: Predicciones futuras (3 semanas)

### 🔄 CICLO DE VIDA

```
Semana 0 (Hoy):           featured_A, premieres_A, recents_A
                            ↓
Semana 1:                 featured_B, premieres_B, recents_B (predefinido en forecast)
                            ↓
Semana 2:                 featured_C, premieres_C, recents_C (predefinido en forecast)
                            ↓
Semana 3:                 featured_D, premieres_D, recents_D (predefinido en forecast)
                            ↓
[Script ejecuta nuevamente] → Recalcula forecast siguiente
```

### 📊 ESTADÍSTICAS

- **Juegos totales**: 150+
- **Juegos PS5**: ~120
- **Juegos PS4**: ~40
- **Juegos PS3**: ~30
- **Premieres (Próximamente)**: 11 activos
- **Juegos por sección**: featured=6, premieres=4, recents=4
- **Histórico**: 52 semanas
- **Predicción**: 3 semanas

### ✨ SIGUIENTES PASOS

1. Ejecutar el script multiplatforma
2. Verificar que PS4 y PS3 tienen contenido
3. Configurar GitHub Actions para ejecución semanal
4. Monitorear si las predicciones son acertadas
5. Ajustar pesos de scoring si es necesario
