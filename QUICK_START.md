## 🚀 QUICK START GUIDE

### 📊 Estado Actual (1 Junio 2026)

✅ Sistema operativo y actualizado
✅ Curaduría para PS5, PS4, PS3
✅ Predicciones para 3 semanas
✅ Secciones estáticas: homeFeatured, popular (no cambian)
✅ Secciones dinámicas: featured, premieres, recentReleases (cambian semanalmente)

---

### 🎮 CÓMO USAR (Lo más simple)

#### Opción 1: Usar el Launcher (Recomendado)
```batch
cd d:\Proyecto\PS5-COLLECTION
curate.bat mp              ← Ejecutar curaduría multiplatforma
curate.bat mp --dry-run    ← Probar sin cambios
```

#### Opción 2: Directo Python
```bash
cd d:\Proyecto\PS5-COLLECTION

# Probar primero
python scripts/auto_curate_multiplatform.py --dry-run

# Ejecutar de verdad
python scripts/auto_curate_multiplatform.py
```

---

### 📅 QUÉS CAMBIA CADA SEMANA

```
LUNES 00:00
    ↓
Script Ejecuta
    ↓
ACTUALIZA:
✅ featured (6 juegos)
✅ premieres (4 juegos)
✅ recentReleases (4 juegos)

NO CAMBIA:
🔒 homeFeatured (8 juegos)
🔒 popular (7 juegos)
```

---

### 📊 QUÉ SE CURA

| Plataforma | featured | premieres | recientes | homeFeatured | popular |
|-----------|----------|-----------|-----------|-------------|---------|
| PS5 | ✅ | ✅ | ✅ | 🔒 | 🔒 |
| PS4 | ✅ | ✅ | ✅ | ❌ | ❌ |
| PS3 | ❌ | ❌ | ❌ | ❌ | ❌ |

---

### 🔮 PREDICCIONES (3 Semanas)

```
Hoy (1 Junio):
  - featured: biohazard-re-4, dragon-quest-iii...
  - premieres: assassins-creed-shadows, death-stranding-2...

Semana 1 (8 Junio):
  - featured: wolf-among-us-2, borderlands-4...
  - premieres: chronoscript-the-endless-end, wolf-among-us-2...

Semana 2 (15 Junio):
  - featured: ea-sports-fc-26, syphon-filter-2...
  - premieres: assassins-creed-shadows, gta-vi...
```

---

### ⚙️ CONFIGURACIÓN

Archivo: `Sony-Web/games.json`
```json
{
  "config": {
    "lastCurated": "2026-06-01T23:18:53...",
    "curationHistory": [...],           // Últimas 52 semanas
    "curationForecast": {
      "week_0": {...},                  // Hoy
      "week_1": {...},                  // Próxima semana
      "week_2": {...}                   // 2 semanas
    }
  },
  "platforms": {
    "PS5": {
      "homeFeatured": [...],            // ESTÁTICO
      "popular": [...],                 // ESTÁTICO
      "featured": [...],                // DINÁMICO
      "premieres": [...],               // DINÁMICO
      "recentReleases": [...]           // DINÁMICO
    }
  }
}
```

---

### 📁 ARCHIVOS IMPORTANTES

```
d:\Proyecto\PS5-COLLECTION\
├── Sony-Web\games.json                ← Base de datos (ACTUALIZADO)
├── scripts\
│   ├── auto_curate.py                 (v1 - Original)
│   ├── auto_curate_v2.py              (v2 - Mejorado)
│   └── auto_curate_multiplatform.py   (MP - RECOMENDADO)
├── curate.bat                         (Launcher)
├── FINAL_SUMMARY.md                   (Resumen completo)
├── MULTIPLATFORM_GUIDE.md             (Documentación)
└── Sony-Web\games.json.bak.1780355933 (Backup automático)
```

---

### 🔄 AUTOMATIZACIÓN

#### Opción 1: Windows Task Scheduler
```
Crear tarea: "PS5 Auto-Curate"
Activador: Cada LUNES a 00:00
Comando: D:\Proyecto\PS5-COLLECTION\curate.bat mp
```

#### Opción 2: GitHub Actions (Mejor)
```
Crear: .github/workflows/auto-curate.yml
Se ejecuta: Cada lunes 00:00 UTC
Automáticamente: Commit y push a GitHub
Netlify: Deploy automático
```

---

### ✨ ALGORITMO (Todas las plataformas)

```
Score = 40% RATING + 25% RECENCY + 15% DISCOUNT + 15% POPULARITY + 5% EXCLUSIVE
```

Preferencias:
- 🌟 Juegos de buena calidad (rating alto)
- 📅 Lanzamientos recientes (recency)
- 💰 Con descuentos (ofertas)
- 👥 Populares/buscados (engagement)
- 🎮 Exclusivas PS5 (bonus)

---

### 🎯 ESTADO ESTA SEMANA

**Premieres (Próximos Estrenos):**
1. Assassin's Creed Shadows (2026)
2. Death Stranding 2 (2026)
3. Marvel 1943: Rise of Hydra (2026)
4. Marvel: Tokong Fighting Souls (2026)

**Recientes (Último Mes):**
1. Bye Sweet Carole
2. Invincible vs
3. Tormented Souls 2
4. Resident Evil: Requiem

**Featured (Recomendados):**
1. Biohazard RE:4
2. Dragon Quest III HD-2D Remake
3. Tactics Ogre: Reborn
4. Code Vein 2
5. FIFA 23
6. Pragmata

---

### 📞 PREGUNTAS FRECUENTES

**P: ¿Cómo cambio lo que aparece?**
R: homeFeatured y popular NO cambian automáticamente (son manuales).
   Featured, premieres y recientes SÍ cambian cada semana.

**P: ¿Puedo ejecutar manual?**
R: Sí, simplemente: `curate.bat mp` o `python scripts/auto_curate_multiplatform.py`

**P: ¿Qué pasa si algo va mal?**
R: El backup automático está en `games.json.bak.1780355933`
   Restaura con: `copy games.json.bak.1780355933 games.json`

**P: ¿Puedo cambiar los parámetros?**
R: Sí:
   ```bash
   python scripts/auto_curate_multiplatform.py \
     --featured-count 8 \              # 8 en lugar de 6
     --premieres-count 6 \             # 6 en lugar de 4
     --weeks-forecast 4 \              # 4 semanas en lugar de 3
     --no-repeat-weeks 6               # 6 semanas sin repetir
   ```

**P: ¿Por qué GTA VI no aparece en premieres?**
R: GTA VI es de 2028, muy lejano.
   El sistema muestra premieres de 2026 primero (próximos).

**P: ¿Funciona para PS4 y PS3?**
R: Sí, PS4 tiene featured/premieres/recientes.
   PS3 solo tiene "all" (lista completa de juegos PS3).

---

### 🚀 PRÓXIMO PASO

```bash
# Ir a d:\Proyecto\PS5-COLLECTION
cd d:\Proyecto\PS5-COLLECTION

# Opción 1: Usar launcher
curate.bat mp

# Opción 2: Directo Python
python scripts/auto_curate_multiplatform.py

# Resultado: games.json actualizado con nueva curaduría
```

---

### 📊 BACKUP AUTOMÁTICO

Cada ejecución crea backup:
```
Sony-Web/games.json.bak.TIMESTAMP
Ejemplo: games.json.bak.1780355933
```

Para restaurar:
```bash
copy games.json.bak.1780355933 games.json
```

---

**Estado**: 🟢 LISTO PARA PRODUCCIÓN
**Última actualización**: 1 Junio 2026 23:18:53 UTC
**Próxima actualización**: 8 Junio 2026 00:00:00 UTC
