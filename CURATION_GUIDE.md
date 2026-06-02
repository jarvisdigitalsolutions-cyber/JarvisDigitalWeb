## 🚀 MEJORAS AL SISTEMA DE CURADURÍA AUTOMÁTICA

### 📊 **Comparación de Algoritmos**

#### **v1 (Actual - Original)**
```
Score = 55% rating + 30% recency + 15% discount
```
✅ Simple y directo
❌ No considera popularidad ni engagement
❌ Premieres no ordenadas por fecha

---

#### **v2 (Mejorado - RECOMENDADO)**
```
Score = 40% rating + 25% recency + 15% discount + 15% popularity + 5% exclusive
```
✨ Cambios:
- **Reduce rating** (55% → 40%) pero agrega popularidad (15%)
- **Premieres ordenadas por fecha** → Muestra los lanzamientos más próximos primero
- **Recientes ordenadas por fecha** → Los más nuevos primero
- **Bonus para exclusivas PS5**
- **Mejor distribución de géneros** (opcional)

---

### 🎯 **CÓMO USAR**

#### Opción 1: Usar la versión mejorada (RECOMENDADO)
```bash
cd d:\Proyecto\PS5-COLLECTION

# Probar sin escribir cambios
python scripts/auto_curate_v2.py --dry-run

# Ejecutar con mejoras
python scripts/auto_curate_v2.py

# Especificar versión explícitamente
python scripts/auto_curate_v2.py --version v2 --dry-run
python scripts/auto_curate_v2.py --version v1 --dry-run
```

#### Opción 2: Comparar ambas versiones
```bash
# Ver qué selecciona v1
python scripts/auto_curate.py --dry-run

# Ver qué selecciona v2 (más inteligente)
python scripts/auto_curate_v2.py --dry-run --version v2
```

---

### 🔧 **PARÁMETROS DISPONIBLES**

```bash
python scripts/auto_curate_v2.py \
  --banner-count 3 \              # Número de banners
  --featured-count 6 \            # Número de destacados
  --premieres-count 4 \           # Número de próximos estrenos
  --recent-releases-count 4 \     # Número de lanzamientos recientes
  --no-repeat-weeks 4 \           # No repetir juegos dentro de N semanas
  --version v2 \                  # v1 (clásico) o v2 (mejorado)
  --dry-run                       # Simular sin escribir
```

---

### 📅 **AUTOMATIZACIÓN (Windows - Tareas Programadas)**

Para que se ejecute **AUTOMÁTICAMENTE cada semana**:

#### Paso 1: Crear script batch
```batch
REM C:\batch\auto_curate_weekly.bat
@echo off
cd /d "D:\Proyecto\PS5-COLLECTION"
python scripts/auto_curate_v2.py --version v2
timeout /t 10
```

#### Paso 2: Programar en Windows
1. Abrir **Tareas Programadas** (taskschd.msc)
2. Crear tarea básica:
   - Nombre: "PS5 Auto-Curate Weekly"
   - Activador: Semanal (lunes 00:00)
   - Acción: Ejecutar `C:\batch\auto_curate_weekly.bat`

---

### 🤖 **INTEGRACIÓN CON GITHUB ACTIONS (Recomendado)**

Crear archivo `.github/workflows/auto-curate.yml`:

```yaml
name: Auto-Curate Weekly

on:
  schedule:
    # Cada lunes a las 00:00 UTC
    - cron: '0 0 * * 1'
  workflow_dispatch:  # Manual trigger

jobs:
  curate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run auto-curation
        run: python scripts/auto_curate_v2.py --version v2
      
      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add Sony-Web/games.json
          git commit -m "🤖 Weekly auto-curation: $(date -u +'%Y-%m-%d')"
          git push
        if: success()
```

---

### 📈 **MÉTRICAS DE SCORING V2**

Para que funcione correctamente, agregar en `games.json`:

```json
{
  "id": "game-id",
  "title": "Game Title",
  "rating": 4.5,
  "release": 2026,
  "price": 59.99,
  "oldPrice": 79.99,
  "status": "Disponible",
  "popularity": 85,  // ← NEW: 0-100 engagement score
  "exclusive": true, // ← NEW: PS5 exclusive bonus
  "genres": ["Action", "Adventure"],
  "bannerImage": "assets/banner/game-id.jpg"
}
```

---

### 🎯 **IMPACTO ESPERADO**

**Con v1 (Actual):**
- Banners: Rating alto + recientes + descuentos
- Premieres: Mezclados sin orden de fecha

**Con v2 (Mejorado):**
- Banners: Mix de rating + recientes + populares + descuentos
- Premieres: Ordenados por **fecha próxima** (primeros los que salen antes)
- Recientes: Ordenados por **fecha lanzamiento** (primeros los más nuevos)
- ✨ Mejor UX: Usuarios ven "próximos estrenos" en orden cronológico

---

### 🔄 **MIGRACIÓN**

1. **Backup actual:**
   ```bash
   copy Sony-Web\games.json Sony-Web\games.json.backup.20260601
   ```

2. **Probar v2:**
   ```bash
   python scripts/auto_curate_v2.py --dry-run --version v2
   ```

3. **Comparar con v1:**
   ```bash
   python scripts/auto_curate.py --dry-run
   ```

4. **Si v2 es mejor:**
   ```bash
   python scripts/auto_curate_v2.py --version v2
   git add Sony-Web/games.json scripts/auto_curate_v2.py
   git commit -m "🚀 Upgrade to auto-curation v2"
   git push
   ```

---

### ✅ **RECOMENDACIONES**

1. ✅ **Usar v2** - Algoritmo más inteligente y flexible
2. ✅ **Agregar `popularity` field** a games.json si tienes datos de engagement
3. ✅ **Ejecutar semanalmente** - Configure GitHub Actions o Task Scheduler
4. ✅ **Revisar dry-run** - Verifica que la selección tenga sentido antes de aplicar
5. ✅ **Mantener v1** - Por si necesitas revertir
