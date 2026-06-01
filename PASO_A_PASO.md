# ✅ GITHUB ACTIONS - GUÍA VISUAL PASO A PASO

## 🎯 ESTADO ACTUAL

```
✅ Script multiplatforma (PS5, PS4, PS3) - LISTO
✅ Workflow file creado - LISTO  
✅ Documentación - LISTO
⏳ Activar en GitHub - AQUÍ ESTAMOS
```

---

## 🚀 PASO 1: ABRIR GITHUB

### URL:
```
https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb
```

### Qué ver:
- ✅ Code tab
- ✅ Pull requests
- ✅ **Actions** (tab - aquí entraremos después)

---

## 📝 PASO 2: CREAR NUEVO ARCHIVO

### Opción A: Click "Add file"
```
GitHub repo → "Add file" → "Create new file"
```

### Opción B: URL directa
```
https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb/new/upload-complete-sony-web
```

### Qué verás:
- Campo: "Name your file..."
- Editor: Área para código
- Botón: "Commit new file"

---

## 📁 PASO 3: NOMBRE DEL ARCHIVO

En el campo "Name your file...":

### COPIAR ESTO:
```
.github/workflows/auto-curate.yml
```

✅ GitHub creará la carpeta `.github/workflows/` automáticamente

---

## 📄 PASO 4: CONTENIDO DEL ARCHIVO

En el editor, **BORRAR TODO** y COPIAR ESTO:

```yaml
name: 🤖 Auto-Curate Weekly (PS5, PS4, PS3)

on:
  schedule:
    # Cada LUNES a las 00:00 UTC
    - cron: '0 0 * * 1'
  
  # Permite ejecución manual desde GitHub
  workflow_dispatch:

jobs:
  curate:
    runs-on: ubuntu-latest
    
    steps:
      # 1. Descargar código
      - name: ✅ Checkout repository
        uses: actions/checkout@v4
        with:
          persist-credentials: true
          fetch-depth: 0
      
      # 2. Configurar Python
      - name: 🐍 Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      # 3. Ejecutar curaduría multiplatforma
      - name: 🎮 Run multiplatform auto-curation
        run: |
          echo "🎮 Iniciando curaduría multiplatforma (PS5, PS4, PS3)..."
          python scripts/auto_curate_multiplatform.py --weeks-forecast 3
          echo "✅ Curaduría completada"
      
      # 4. Verificar cambios
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
      
      # 5. Configurar Git
      - name: 🔧 Configure Git
        if: env.CHANGED == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
      
      # 6. Commit de cambios
      - name: 💾 Commit changes
        if: env.CHANGED == 'true'
        run: |
          git add Sony-Web/games.json
          TIMESTAMP=$(date -u +'%Y-%m-%d %H:%M:%S')
          git commit -m "🤖 Weekly auto-curation: multiplatform update ($TIMESTAMP)"
      
      # 7. Push a GitHub
      - name: 📤 Push to repository
        if: env.CHANGED == 'true'
        run: |
          git push origin ${{ github.ref }}
      
      # 8. Resumen de éxito
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

✅ Pega TODO el contenido arriba

---

## 💾 PASO 5: COMMIT EN GITHUB

### Scroll down hasta "Commit new file"

Campo: "Add an optional extended description..."

Escribir:
```
✅ Setup GitHub Actions: Auto-curate workflow

- Schedule: Every Monday 00:00 UTC
- Multiplatform: PS5, PS4, PS3
- Automatic commit and push
- Netlify deployment automatic
```

### Click: "Commit new file" (Botón verde)

---

## ✅ PASO 6: VERIFICAR

### Ve a: Actions tab

```
https://github.com/jarvisdigitalsolutions-cyber/JarvisDigitalWeb/actions
```

### Deberías ver:
```
🤖 Auto-Curate Weekly (PS5, PS4, PS3)
```

**✅ Si aparece = ÉXITO**

---

## 🧪 PASO 7: PROBAR (Opcional)

### En la página de Actions:

1. Click: "🤖 Auto-Curate Weekly"
2. Click: "Run workflow" (botón gris)
3. Click: "Run workflow" (botón verde)
4. Ver progreso en tiempo real

### Verás steps:
- ✅ Checkout repository
- ✅ Set up Python 3.11
- ✅ Run multiplatform auto-curation
- ✅ Check changes
- ✅ Configure Git
- ✅ Commit changes
- ✅ Push to repository
- ✅ Completion summary

---

## 📅 PASO 8: AUTOMATIZACIÓN ACTIVADA

Después del test, el workflow se ejecutará **AUTOMÁTICAMENTE**:

```
CADA LUNES 00:00 UTC
    ↓
Sin intervención manual
    ↓
Tu web se actualiza
    ↓
SIN QUE HAGAS NADA
```

---

## 🎊 RESULTADO FINAL

| Antes | Ahora |
|-------|-------|
| ❌ Manual | ✅ Automático |
| ❌ Cada semana | ✅ Cada lunes UTC |
| ❌ Tú haces todo | ✅ Sistema hace todo |
| ❌ Propenso a errores | ✅ Consistente |
| ❌ Dedicas tiempo | ✅ 0% intervención |

---

## ⏱️ TIEMPO TOTAL

- ✅ Crear archivo: 2 minutos
- ✅ Copiar contenido: 1 minuto
- ✅ Commit: 30 segundos
- ✅ Verificar: 30 segundos

**TOTAL: ~5 MINUTOS**

---

## 🎯 RESUMEN

```
┌─────────────────────────────────────┐
│ 1. Abre GitHub repo                 │
│ 2. Add file → Create new file       │
│ 3. Nombre: .github/workflows/...    │
│ 4. Copia contenido YAML             │
│ 5. Commit new file                  │
│ 6. Ve a Actions tab                 │
│ 7. Verifica workflow aparece        │
│ 8. (Opcional) Prueba manual         │
└─────────────────────────────────────┘
        ↓
   ✨ LISTO ✨
        ↓
   Cada lunes 00:00 UTC
   se ejecuta automáticamente
```

---

**¿Necesitas ayuda? Todos los documentos están en la carpeta raíz:**

- `CREAR_WORKFLOW_WEB.md` - Este mismo paso a paso
- `RESUMEN_FINAL.md` - Checklist y confirmación
- `GITHUB_ACTIONS_SETUP.md` - Más detalles
- `GITHUB_ACTIONS_QUICK.md` - Referencia rápida

**¡VAMOS!**
