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
