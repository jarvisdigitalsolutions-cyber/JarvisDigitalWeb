# One-click deploy scripts

Estos scripts permiten subir rápidamente un directorio (por ejemplo `Sony-Web`) al repositorio creando una rama automática y empujándola a `origin`.

Archivos creados:
- `scripts/deploy_one_click.ps1` — PowerShell (Windows)
- `scripts/deploy_one_click.py` — Python 3 (multiplataforma)

Uso rápido (PowerShell):
```powershell
# Ejecutar desde la raíz del repo o pasar ruta completa
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_one_click.ps1 -Path Sony-Web

# Si quieres crear branch y hacer merge automático (usar con precaución):
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_one_click.ps1 -Path Sony-Web -Merge
```

Uso rápido (Python):
```bash
python scripts/deploy_one_click.py --path Sony-Web
# merge opcional
python scripts/deploy_one_click.py --path Sony-Web --merge
```

Opciones útiles:
- `--path` / `-p`: directorio a añadir (por defecto `Sony-Web`).
- `--branch` / `-b`: nombre de branch (si no lo indicas se genera `deploy-<path>-YYYYMMDD-HHMMSS`).
- `--message` / `-m`: mensaje de commit.
- `--merge` / `-M`: intenta hacer merge de la rama en el branch `--target` (por defecto `main`) y pushearlo — usar con precaución (puede producir conflictos).

Notas y precauciones:
- Los scripts asumen que `git` está instalado y que `origin` está configurado.
- Para PowerShell en Windows puede ser necesario ajustar la política de ejecución: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` o usar la opción mostrada.
- Si tienes cambios no commiteados fuera del directorio especificado, no serán incluidos a menos que los añadas manualmente.
- El script crea una rama separada por defecto y la sube. Para desplegar directamente en `main` puedes usar la opción `--merge` (requiere permisos y puede generar conflictos).

Si quieres que el script empuje directamente a `main` sin crear branch, dime y lo ajusto (pero no lo recomiendo por seguridad).