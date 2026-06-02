## 🚀 ACTIVAR GITHUB ACTIONS - GUÍA RÁPIDA

### 🎯 LO QUE NECESITAS HACER (Sencillo, 3 pasos)

---

## OPCIÓN 1: Por GitHub Web (Más fácil - NO necesitas terminal)

### Paso 1: Ir a GitHub.com

```
https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb
```

### Paso 2: Subir archivo workflow

1. Click "Add file" → "Create new file"
2. Nombre: `.github/workflows/auto-curate.yml`
3. Copiar contenido (ver abajo)
4. Click "Commit changes"
5. Mensaje: `✅ Setup GitHub Actions auto-curate workflow`
6. Commit!

**CONTENIDO A COPIAR:**

```yaml
name: 🤖 Auto-Curate Weekly (PS5, PS4, PS3)

on:
  schedule:
    - cron: '0 0 * * 1'
  workflow_dispatch:

jobs:
  curate:
    runs-on: ubuntu-latest
    
    steps:
      - name: ✅ Checkout repository
        uses: actions/checkout@v4
        with:
          persist-credentials: true
          fetch-depth: 0
      
      - name: 🐍 Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: 🎮 Run multiplatform auto-curation
        run: |
          echo "🎮 Iniciando curaduría multiplatforma (PS5, PS4, PS3)..."
          python scripts/auto_curate_multiplatform.py --weeks-forecast 3
          echo "✅ Curaduría completada"
      
      - name: 📊 Check changes in games.json
        run: |
          echo "Revisando cambios..."
          if git diff --exit-code Sony-Web/games.json > /dev/null; then
            echo "✅ Sin cambios en games.json"
            echo "CHANGED=false" >> $GITHUB_ENV
          else
            echo "📝 Cambios detectados en games.json"
            git diff Sony-Web/games.json | head -30
            echo "CHANGED=true" >> $GITHUB_ENV
          fi
      
      - name: 🔧 Configure Git
        if: env.CHANGED == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
      
      - name: 💾 Commit changes
        if: env.CHANGED == 'true'
        run: |
          git add Sony-Web/games.json
          TIMESTAMP=$(date -u +'%Y-%m-%d %H:%M:%S')
          git commit -m "🤖 Weekly auto-curation: multiplatform update ($TIMESTAMP)"
      
      - name: 📤 Push to repository
        if: env.CHANGED == 'true'
        run: |
          git push origin ${{ github.ref }}
      
      - name: ✨ Completion summary
        run: |
          echo "=========================================="
          echo "✅ Auto-curation Workflow Completed"
          echo "=========================================="
          echo "📅 Timestamp: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
          echo "🔄 Changes: ${{ env.CHANGED }}"
          echo "🔗 Repository: ${{ github.repository }}"
          echo "📦 Branch: ${{ github.ref }}"
          echo "🚀 Next deployment: Netlify (automatic)"
          echo "=========================================="
```

### Paso 3: Listo!

Una vez commits el archivo en GitHub, el workflow está **activo**.

---

## OPCIÓN 2: Por Terminal (Si quieres)

```bash
cd d:\Proyecto\PS5-COLLECTION

# Ver rama actual
git branch

# Pushear a esa rama
git push origin [rama-actual]

# Si pide token:
# Generar en GitHub → Settings → Developer settings → Personal access tokens
# Copiar token
# Pegarlo cuando pida password
```

---

## ✅ VER QUE ESTÁ FUNCIONANDO

Una vez el archivo está en GitHub:

1. Ve a: https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb
2. Click pestaña "Actions"
3. Deberías ver: **"🤖 Auto-Curate Weekly (PS5, PS4, PS3)"**

---

## 🧪 PROBAR WORKFLOW (Opcional)

En GitHub:

1. Actions → "🤖 Auto-Curate Weekly"
2. Click "Run workflow"
3. Click el botón "Run workflow"
4. Ver progreso en tiempo real

---

## 📅 AUTOMATIZACIÓN ACTIVADA

```
CADA LUNES 00:00 UTC → Ejecuta automáticamente
  ├─ Checkout code
  ├─ Setup Python
  ├─ Run auto_curate_multiplatform.py
  ├─ Commit cambios
  ├─ Push a GitHub
  └─ Netlify deploya

SIN INTERVENCIÓN TUYA
```

---

## 🎯 RESULTADO FINAL

```
Tú:        Solo diseño, títulos, estructura
GitHub:    Curaduría automática cada lunes
Netlify:   Deploy automático
Web:       Actualizada sin tocar nada
```

---

## 📊 MONITOREO

Ver ejecuciones: https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb/actions

Ahí podrás ver:
- ✅ Ejecuciones exitosas
- ❌ Fallos (si los hay)
- ⏱️ Cuándo ejecutó
- 📝 Logs detallados

---

**La opción MÁS FÁCIL es por GitHub Web (Opción 1)**

¿Lo hacemos así?
