## 🚀 CONFIGURAR GITHUB ACTIONS (Automatización Semanal)

### 🎯 QUÉ VA A PASAR

```
CADA LUNES a las 00:00 UTC (Automáticamente)
    ↓
GitHub Actions ejecuta script
    ↓
Cura PS5, PS4, PS3
    ↓
Actualiza games.json
    ↓
Hace commit automático
    ↓
Sube cambios a GitHub
    ↓
Netlify deploya (automático)
    ↓
Web actualizada SIN que hagas nada
```

---

### 📋 REQUISITOS

✅ Ya tenemos:
- `.github/workflows/auto-curate.yml` ← Ya creado
- `scripts/auto_curate_multiplatform.py` ← Ya existe
- GitHub repository conectado ← Verificar

Necesitas:
- Acceso a GitHub
- Repository en GitHub
- Conexión entre tu repo local y GitHub (ya existe)

---

### ⚙️ PASO 1: VERIFICAR CONFIGURACIÓN GITHUB

En la terminal:

```bash
cd d:\Proyecto\PS5-COLLECTION

# Ver remote origin
git remote -v

# Debería mostrar algo como:
# origin  https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb.git (fetch)
# origin  https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb.git (push)
```

Si no sale nada, ejecutar:
```bash
git remote add origin https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb.git
```

---

### ⚙️ PASO 2: PUSH DEL WORKFLOW A GITHUB

```bash
cd d:\Proyecto\PS5-COLLECTION

# Ver cambios
git status

# Añadir todo
git add .

# Commit
git commit -m "✅ Setup GitHub Actions auto-curate workflow"

# PUSH a GitHub
git push origin main
# o
git push origin upload-complete-sony-web

# (Depende de tu rama actual)
```

✅ **Si ve un error de autenticación**: Usar token de GitHub:
```bash
git push https://[TU-TOKEN]@github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb.git main
```

Para obtener token:
1. GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Scopes: `repo` (full control)
4. Copy token y usarlo en el comando arriba

---

### ⚙️ PASO 3: VERIFICAR EN GITHUB

1. Ve a: https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb
2. Click en pestaña "Actions"
3. Deberías ver: **"🤖 Auto-Curate Weekly (PS5, PS4, PS3)"**

---

### ⚙️ PASO 4: PROBAR MANUALMENTE (Opcional)

Desde GitHub:
1. Ve a Actions
2. Selecciona "🤖 Auto-Curate Weekly (PS5, PS4, PS3)"
3. Click "Run workflow" → "Run workflow"
4. Verá progreso en tiempo real

O desde terminal:
```bash
# Trigger workflow manual
gh workflow run auto-curate.yml

# (Necesita tener instalado GitHub CLI)
```

---

### 📅 AUTOMATIZACIÓN CONFIGURADA

```yaml
# Cron expression: 0 0 * * 1
# Significa: 
#   - Minuto 0
#   - Hora 0 (00:00)
#   - Cualquier día del mes
#   - Cualquier mes
#   - Lunes (1 = Monday)

Equivalentes en tu zona horaria:
  ├─ UTC (Londres):           Lunes 00:00
  ├─ EST (New York):          Domingo 20:00 (-5)
  ├─ CET (España/Europa):     Lunes 01:00 (+1)
  ├─ ART (Argentina):         Lunes 21:00 (-3)
  └─ COL (Colombia):          Lunes 19:00 (-5)
```

¿Quieres cambiar la hora? Edita el archivo:
```yaml
# En .github/workflows/auto-curate.yml
schedule:
  - cron: '0 0 * * 1'   # Cambia estos números
```

Ejemplos:
```yaml
- cron: '0 12 * * 1'    # Lunes 12:00 UTC
- cron: '30 23 * * 0'   # Domingo 23:30 UTC
- cron: '0 0 * * *'     # Cada día a 00:00 UTC
```

---

### 📊 QUÉ HACE CADA SEMANA

```
LUNES 00:00:00 UTC
    ↓
✅ Paso 1: Checkout code
✅ Paso 2: Setup Python 3.11
✅ Paso 3: Execute auto_curate_multiplatform.py
   └─ Cura PS5, PS4, PS3
   └─ Predice 3 semanas
   └─ Actualiza games.json
✅ Paso 4: Check for changes
✅ Paso 5: Configure Git
✅ Paso 6: Commit changes (si hay)
✅ Paso 7: Push to GitHub
✅ Paso 8: Success summary
    ↓
📤 GitHub recibe cambios
    ↓
🚀 Netlify Deploy automático
    ↓
💻 Web actualizada LIVE
```

---

### 🔍 MONITOREAR EJECUCIONES

#### Opción 1: GitHub Web UI
```
https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb/actions
```

Verá:
- ✅ Executions exitosas (verde)
- ❌ Executions fallidas (rojo)
- ⏱️ Timestamp y duración
- 📝 Logs detallados

#### Opción 2: Desde terminal
```bash
# Ver últimas ejecuciones
gh run list -w auto-curate.yml

# Ver detalles de última ejecución
gh run view --workflow=auto-curate.yml

# Ver logs
gh run view --log --workflow=auto-curate.yml
```

---

### 📧 NOTIFICACIONES (Opcional)

GitHub puede notificar por email:

1. GitHub.com → Settings → Notifications
2. Enable: "Actions: Run completed"
3. Recibirá email si falla o cuando Complete

---

### 🐛 TROUBLESHOOTING

#### Problema: "Workflow file not found"
**Solución:**
```bash
git add .github/workflows/auto-curate.yml
git commit -m "Add GitHub Actions workflow"
git push origin main
```

#### Problema: "Permission denied"
**Solución:** Verificar token en GitHub o usar SSH:
```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Agregar public key a GitHub → Settings → SSH keys
# Cambiar remote a SSH
git remote set-url origin git@github.com:jarvisdigitalsolutions-cyber/JarvisDigitalWeb.git
```

#### Problema: "No changes to commit"
**Significa:** El script ejecutó pero no encontró cambios. Normal si:
- Ya hay juegos similares en la DB
- Predicción no cambió
- Sin cambios = No hace commit ✅

#### Problema: Script falla
**Revisar logs:**
1. GitHub Actions → Click workflow fallido
2. Expandir "Run multiplatform auto-curation"
3. Ver error exacto

---

### 📝 MONITORING AVANZADO

#### Crear tabla de ejecuciones
```bash
# Ver todas las ejecuciones
gh run list -w auto-curate.yml -L 10

# Formato:
# STATUS  TITLE                           WORKFLOW              BRANCH  EVENT       ID
# ✓       Weekly auto-curate: multipl...  Auto-Curate Weekly    main    scheduled   12345
# ✓       Weekly auto-curate: multipl...  Auto-Curate Weekly    main    scheduled   12344
```

#### Export logs
```bash
# Descargar logs de última ejecución
gh run view --log --workflow=auto-curate.yml > last_run.log

# Revisar
cat last_run.log
```

---

### 🎯 ESTADO FINAL (Una vez activado)

| Aspecto | Estado |
|---------|--------|
| Workflow activado | ✅ Sí |
| Cron schedule | ✅ Lunes 00:00 UTC |
| Auto-curation | ✅ Multiplatform (PS5, PS4, PS3) |
| Predicción | ✅ 3 semanas |
| Commit automático | ✅ Sí (si hay cambios) |
| Deployment | ✅ Netlify (automático) |
| Monitoreo | ✅ GitHub Actions logs |
| Tu esfuerzo | ✅ 0% (completamente automático) |

---

### 📌 RESUMEN (LO MÁS IMPORTANTE)

```bash
# 1. Asegúrate de que los cambios están en GitHub
git status
git add .
git commit -m "Update GitHub Actions workflow"
git push origin main

# 2. Ve a GitHub Actions y verifica
https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb/actions

# 3. Listo. Cada lunes a las 00:00 UTC se ejecuta automáticamente
# Tu web se actualiza SIN que hagas NADA
```

---

### 🎊 VENTAJAS

✅ **100% Automático** - Sin intervención manual
✅ **Semanal** - Lunes a las 00:00 UTC
✅ **Multiplatforma** - PS5, PS4, PS3 cubiertas
✅ **Predicción** - 3 semanas calculadas
✅ **Commit automático** - Si hay cambios
✅ **Deployment automático** - Netlify se dispara
✅ **Monitoreable** - Logs en GitHub Actions
✅ **Seguro** - Token de GitHub, no expone credenciales
✅ **Reversible** - Puedes desactivar en cualquier momento

---

### 💡 TUS RESPONSABILIDADES

Después de esto:

✅ **Mantener juegos actualizados en games.json** (manual)
✅ **Cambiar titles, estructura, diseño** (manual) 
✅ **Revisar cambios semanalmente en GitHub Actions** (opcional)

❌ **NO necesitas:** Ejecutar scripts, hacer commit, push, nada de eso

---

### 🚀 SIGUIENTES PASOS

1. ✅ Ejecutar: `git push origin main`
2. ✅ Ir a: GitHub Actions en repo
3. ✅ Verificar que workflow aparece
4. ✅ Click "Run workflow" para probar
5. ✅ Ver logs si quieres confirmar
6. ✅ Listo. Cada lunes se ejecuta automáticamente.

---

**Estado**: 🟢 COMPLETAMENTE CONFIGURADO
**Próxima ejecución**: Próximo lunes 00:00 UTC
**Tu acción requerida**: 0% (es automático)
