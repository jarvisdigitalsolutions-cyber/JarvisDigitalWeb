#!/usr/bin/env python3
"""
scripts/add_banner_images.py

Escanea la carpeta de banners y actualiza `Sony-Web/games.json` añadiendo
el campo `bannerImage` con rutas del tipo `IMG/PS5/Banner/<archivo>` cuando
encuentre coincidencias por nombre (basado en `image` o `id`).

Uso:
  python scripts/add_banner_images.py [--dry-run] [--overwrite]

Por seguridad crea una copia de seguridad `games.json.bak.<timestamp>` antes de sobrescribir.
"""
import argparse
import json
import shutil
import time
from pathlib import Path
import difflib
import unicodedata
import re


def _normalize_str(s):
    if not s:
        return ''
    # descomponer acentos y eliminar marcas
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    # reemplazar separadores por guion
    s = re.sub(r'[\s+._]+', '-', s)
    # mantener solo alfanuméricos y guiones
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s


def find_best_banner(base_names, banner_files):
    """Devuelve el nombre de archivo del banner mejor coincidente o None.
    Usa normalización y, si falla, un fallback con difflib para coincidencias aproximadas.
    """
    bases = [bn for bn in base_names if bn]
    norm_bases = [_normalize_str(b) for b in bases]

    # preprocesar banner files
    banner_map = {}
    norm_names = []
    for bf in banner_files:
        stem = bf.stem
        n = _normalize_str(stem)
        banner_map[n] = bf.name
        norm_names.append(n)

    best = None
    best_score = 0

    for n in norm_names:
        score = 0
        for bnorm in norm_bases:
            if not bnorm:
                continue
            if n == bnorm:
                score = max(score, 120)
            elif n == bnorm + 'banner' or n == bnorm + '-banner':
                score = max(score, 110)
            elif bnorm in n:
                score = max(score, 95)
            elif n in bnorm:
                score = max(score, 75)
            elif n.replace('-', '') == bnorm.replace('-', ''):
                score = max(score, 100)
        if score > best_score:
            best_score = score
            best = n

    # si encontramos una coincidencia clara, retornarla
    if best and best_score >= 75:
        return banner_map.get(best)

    # fallback: usar difflib para sugerencias aproximadas
    for bnorm in norm_bases:
        matches = difflib.get_close_matches(bnorm, norm_names, n=1, cutoff=0.62)
        if matches:
            return banner_map.get(matches[0])

    return None


def main():
    parser = argparse.ArgumentParser(description='Autocompleta bannerImage en Sony-Web/games.json')
    parser.add_argument('--games', default=None, help='Ruta a games.json (por defecto se detecta)')
    parser.add_argument('--banner-dir', default=None, help='Ruta a la carpeta de banners (por defecto se detecta)')
    parser.add_argument('--dry-run', action='store_true', help='Mostrar cambios propuestos pero no escribir')
    parser.add_argument('--overwrite', action='store_true', help='Sobrescribir bannerImage existentes')
    args = parser.parse_args()

    # determinar rutas relativas al repo (este script está en /scripts)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]
    default_games = repo_root / 'Sony-Web' / 'games.json'
    default_banner_dir = repo_root / 'Sony-Web' / 'IMG' / 'PS5' / 'Banner'

    games_path = Path(args.games) if args.games else default_games
    banner_dir = Path(args.banner_dir) if args.banner_dir else default_banner_dir

    if not games_path.exists():
        print(f'ERROR: no encuentro games.json en {games_path}')
        return 2
    if not banner_dir.exists() or not banner_dir.is_dir():
        print(f'ERROR: no encuentro la carpeta de banners en {banner_dir}')
        return 3

    banner_files = [p for p in banner_dir.iterdir() if p.is_file()]
    if not banner_files:
        print(f'No hay archivos en {banner_dir} para usar como banners.')
        return 0

    with games_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    games = data.get('games', {})

    updated = []
    skipped = []
    unmatched = []

    for gid, g in games.items():
        # respeto la bandera de exclusión si está explicitada
        flag = g.get('bannerImageShow')
        if flag is False:
            skipped.append(gid)
            continue
        if isinstance(flag, str) and flag.lower() in ('no', 'false', '0', 'off'):
            skipped.append(gid)
            continue

        has_existing = bool(g.get('bannerImage'))
        if has_existing and not args.overwrite:
            skipped.append(gid)
            continue

        image_field = g.get('image') or ''
        image_base = Path(image_field).stem if image_field else ''
        id_base = str(g.get('id') or '')

        candidate = find_best_banner([image_base, id_base], banner_files)
        if candidate:
            banner_path = f'IMG/PS5/Banner/{candidate}'
            if g.get('bannerImage') != banner_path:
                g['bannerImage'] = banner_path
                updated.append((gid, banner_path))
            else:
                skipped.append(gid)
        else:
            unmatched.append(gid)

    # mostrar resultado
    print('\nResumen:')
    print(f'  candidatos encontrados y actualizados: {len(updated)}')
    print(f'  saltados (existente o excluidos): {len(skipped)}')
    print(f'  sin coincidencia: {len(unmatched)}')

    if args.dry_run:
        if updated:
            print('\nPropuestas:')
            for gid, p in updated:
                print(f'  - {gid}: {p}')
        if unmatched:
            print('\nSin banner detectado para (ejemplos):')
            print(', '.join(unmatched[:20]))
        print('\nDry-run: no se modificó el archivo.')
        return 0

    if not updated:
        print('Nada que actualizar. No se modificó games.json.')
        return 0

    # backup
    ts = int(time.time())
    bak = games_path.with_name(f'games.json.bak.{ts}')
    shutil.copy2(games_path, bak)
    with games_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Wrote {games_path} (backup: {bak})')
    if updated:
        print('\nActualizaciones aplicadas:')
        for gid, p in updated:
            print(f'  - {gid}: {p}')

    if unmatched:
        print('\nSin coincidencia para estos juegos (revisar manualmente):')
        print(', '.join(unmatched[:50]))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
