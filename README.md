# PS5 Collection - Deploy en Netlify

Este repositorio contiene la web estática de PS5 Collection y la lógica de auto-curación semanal.

## Qué hace el proyecto

- `Sony-Web/` contiene la web principal y los datos `games.json`.
- `netlify/functions/` contiene funciones backend para registro/login/activación.
- `.github/workflows/auto-curate.yml` ejecuta semanalmente la curación automática y actualiza `Sony-Web/games.json`.
- `netlify.toml` configura Netlify para publicar `Sony-Web` y usar `netlify/functions`.

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
