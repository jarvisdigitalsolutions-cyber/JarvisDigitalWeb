## 📊 COMPARACIÓN: v1 vs v2 (Ejecución 1 Junio 2026)

### **ESTA SEMANA (Current)**

| Sección | v1 (Original) | v2 (Mejorado) | Diferencia |
|---------|---------------|--------------|-----------|
| **Banners** | life-is-strange-reunion<br>monster-hunter-stories-3-twisted-reflection<br>tactics-ogre-reborn | **Mismo** (idéntico) | ✅ Sin cambios |
| **Featured** | biohazard-re-4<br>dragon-quest-iii-hd-2d-remake<br>tactics-ogre-reborn<br>code-vein-2<br>fifa-23<br>pragmata | **Mismo** (idéntico) | ✅ Sin cambios |
| **Premieres** | ❌ grand-theft-auto-vi<br>❌ wolverine<br>❌ phantom-blade-zero<br>007-first-light | ✅ assassins-creed-shadows<br>✅ death-stranding-2<br>✅ marvel-1943-rise-hydra<br>✅ marvel-tokon-fighting-souls | 🔴 **CAMBIO IMPORTANTE**: v2 selecciona premieres **POR FECHA** (más próximas primero)<br>v1 selecciona por **SCORE** (calidad) |
| **Recientes** | bye-sweet-carole<br>invincible-vs<br>tormented-souls-2<br>resident-evil-requiem | **Mismo** (idéntico) | ✅ Sin cambios |

---

### **PRÓXIMA SEMANA (Next Week Forecast)**

| Sección | v1 (Original) | v2 (Mejorado) | Diferencia |
|---------|---------------|--------------|-----------|
| **Premieres** | marvel-tokon-fighting-souls<br>marvel-1943-rise-hydra<br>wolf-among-us-2<br>chronoscript-the-endless-end | ✅ chronoscript-the-endless-end<br>✅ wolf-among-us-2<br>✅ zero-parades<br>✅ 007-first-light | 🔴 **ORDEN DIFERENTE**: v2 ordena cronológicamente |

---

### 🎯 **KEY INSIGHTS**

**La diferencia clave está en PREMIERES:**

#### v1 (Score-based):
- Selecciona premieres por **rating + recency + discount**
- Resultado: Juegos de buena calidad próximamente, pero no necesariamente los más próximos
- **Problema:** GTA VI, Wolverine, Phantom Blade Zero son de 2027-2028 (muy lejanos)

#### v2 (Chronological-based):
- Selecciona premieres por **fecha de lanzamiento**
- Resultado: Primero los que salen antes (mayo, junio 2026 → diciembre 2026)
- **Ventaja:** Usuarios ven "próximos estrenos" en orden temporal
- **UX:** Mejor información del "cuándo" sale vs. "qué tan bueno es"

---

### 📅 **ANÁLISIS DE PREMIERES (Por Fecha)**

```
PREMIERES EN games.json (ordenadas por release):
- assassins-creed-shadows (2026)      ← v2 elige esta (PRONTO)
- death-stranding-2 (2026)             ← v2 elige esta (PRONTO)
- marvel-1943-rise-hydra (2026)        ← v2 elige esta (PRONTO)
- marvel-tokon-fighting-souls (2026)   ← v2 elige esta (PRONTO)
- chronoscript-the-endless-end (2027)  ← v2 la pone segunda semana
- wolf-among-us-2 (2027)               ← v2 la pone segunda semana
- 007-first-light (2027)
- zero-parades (2027)
- grand-theft-auto-vi (2028)           ← v1 elige esta (v2 NO, muy lejana)
- wolverine (2028)                     ← v1 elige esta (v2 NO, muy lejana)
- phantom-blade-zero (2028)            ← v1 elige esta (v2 NO, muy lejana)
```

---

### ✅ **RECOMENDACIÓN**

**🚀 USAR v2** porque:

1. **Premieres más relevantes**
   - Usuarios quieren saber QUÉ SALE PRONTO
   - v2 muestra primero 2026, v1 muestra mezcla 2026-2028

2. **Mejor experiencia**
   - "Próximos estrenos" = próximos en el TIEMPO, no en rating
   - Users expectations met

3. **Backward compatible**
   - Banners, Featured, Recientes = idénticos
   - Solo cambia premieres (para mejor)

4. **Flexible**
   - Si quieres volver a v1: `python scripts/auto_curate_v2.py --version v1`
   - Ambos algoritmos disponibles

---

### 🔄 **PRÓXIMOS PASOS**

```bash
# 1. Revisar diferencias
✅ Hecho: Comparación arriba

# 2. Decidir versión
□ v1: Score-based (actual)
□ v2: Chronological + Score (recomendado)

# 3. Ejecutar
python scripts/auto_curate_v2.py --version v2

# 4. Commit
git add Sony-Web/games.json scripts/auto_curate_v2.py
git commit -m "🚀 Upgrade to auto-curation v2 (chrono-premieres)"
git push

# 5. Automatizar (opcional)
# Configurar GitHub Actions o Task Scheduler
```

---

### 📊 **SCORING DETALLADO (Top 5 Premieres)**

```python
v2 Score Calculator para Premieres:
- 40% rating
- 25% recency  
- 15% discount
- 15% popularity
- 5% exclusive

Top Premieres por Score v2:
1. marvel-1943-rise-hydra (2026) → Score: 0.72 → Rank #1 por fecha
2. death-stranding-2 (2026) → Score: 0.68 → Rank #2 por fecha
3. assassins-creed-shadows (2026) → Score: 0.66 → Rank #3 por fecha
4. marvel-tokon-fighting-souls (2026) → Score: 0.64 → Rank #4 por fecha
```
