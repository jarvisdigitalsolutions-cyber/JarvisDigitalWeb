#!/usr/bin/env python3
"""
scripts/auto_curate.py

Script server-side que ejecuta la mini-IA de curación y actualiza
`Sony-Web/games.json` con `banners`, `platforms.PS5.sections.featured.games` y
`platforms.PS5.sections.premieres.games`.

Parámetros y comportamiento:
- Evita repetir banners/featured dentro de una ventana configurable (por defecto 4 semanas).
- Intervalo de curación pensado para ejecutarse semanalmente (7 días).
- Guarda historial de curaciones en `config.curationHistory`.

Uso:
  python scripts/auto_curate.py --dry-run
  python scripts/auto_curate.py

"""
import argparse
import json
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path


def parse_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def compute_score(g, now_year):
    rating = parse_float(g.get('rating') or 0)
    release = g.get('release')
    try:
        release_year = int(release) if str(release).strip() else now_year
    except Exception:
        release_year = now_year
    age = max(0, now_year - release_year)
    recency = 1.0 if age <= 0 else 1.0 / (1 + age)
    oldp = parse_float(g.get('oldPrice'))
    p = parse_float(g.get('price'))
    discount = ((oldp - p) / oldp) if (oldp and p and oldp > p) else 0.0
    norm_rating = min(1.0, rating / 5.0)
    score = (0.55 * norm_rating) + (0.30 * recency) + (0.15 * discount)
    return score


def load_games(games_path: Path):
    with games_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_games(games_path: Path, data: dict):
    ts = int(time.time())
    bak = games_path.with_name(f'games.json.bak.{ts}')
    shutil.copy2(games_path, bak)
    with games_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return bak


def recent_ids_from_history(history, weeks):
    cutoff = datetime.utcnow() - timedelta(weeks=weeks)
    recent_banners = set()
    recent_featured = set()
    for entry in history:
        ts = entry.get('timestamp')
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            continue
        if dt >= cutoff:
            recent_banners.update(entry.get('banners', []))
            recent_featured.update(entry.get('featured', []))
    return recent_banners, recent_featured


def valid_banner_candidate(g):
    bi = g.get('bannerImage')
    if not bi:
        return False
    if '/banner/' not in str(bi).lower():
        return False
    flag = g.get('bannerImageShow')
    if flag is False:
        return False
    if isinstance(flag, str) and flag.lower() in ('no', 'false', '0', 'off'):
        return False
    return True


def select_banners(candidates, recent_banners, banner_count, exclude_ids=None):
    exclude_ids = set(exclude_ids or [])
    selected = [g for g in candidates if g['id'] not in exclude_ids and g['id'] not in recent_banners][:banner_count]
    if len(selected) < banner_count:
        for g in candidates:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= banner_count:
                break
    return selected


def select_featured(sorted_games, recent_featured, featured_count, exclude_ids=None):
    exclude_ids = set(exclude_ids or [])
    selected = [g for g in sorted_games if g['id'] not in exclude_ids and g['id'] not in recent_featured][:featured_count]
    if len(selected) < featured_count:
        for g in sorted_games:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= featured_count:
                break
    return selected


def select_premieres(sorted_games, now_year, premieres_count, exclude_ids=None):
    exclude_ids = set(exclude_ids or [])
    candidates = [g for g in sorted_games if (str(g.get('release') or '')).isdigit() and int(g.get('release')) >= now_year - 1]
    selected = [g for g in candidates if g['id'] not in exclude_ids][:premieres_count]
    if len(selected) < premieres_count:
        for g in candidates:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= premieres_count:
                break
    return selected


def main():
    parser = argparse.ArgumentParser(description='Auto-curate banners/featured/premieres into Sony-Web/games.json')
    parser.add_argument('--games', default=None, help='Ruta a Sony-Web/games.json')
    parser.add_argument('--banner-count', type=int, default=3)
    parser.add_argument('--featured-count', type=int, default=6)
    parser.add_argument('--premieres-count', type=int, default=3)
    parser.add_argument('--no-repeat-weeks', type=int, default=4, help='No repetir picks dentro de N semanas')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]
    games_path = Path(args.games) if args.games else repo_root / 'Sony-Web' / 'games.json'

    if not games_path.exists():
        print(f'ERROR: no encuentro {games_path}')
        return 2

    data = load_games(games_path)
    games = data.get('games', {})
    games_list = list(games.values())

    now_year = datetime.utcnow().year

    # compute scores
    for g in games_list:
        g['_score'] = compute_score(g, now_year)

    # ensure curation history exists
    cfg = data.setdefault('config', {})
    history = cfg.setdefault('curationHistory', [])

    recent_banners, recent_featured = recent_ids_from_history(history, args.no_repeat_weeks)

    banner_candidates = [g for g in games_list if valid_banner_candidate(g)]
    banner_candidates.sort(key=lambda x: x.get('_score', 0), reverse=True)

    # select current curated items
    selected_banners = select_banners(banner_candidates, recent_banners, args.banner_count)
    all_sorted = sorted(games_list, key=lambda x: x.get('_score', 0), reverse=True)
    selected_featured = select_featured(all_sorted, recent_featured, args.featured_count)
    selected_premieres = select_premieres(all_sorted, now_year, args.premieres_count)

    # prepare next-week forecast
    future_recent_banners = recent_banners.union({g['id'] for g in selected_banners})
    future_recent_featured = recent_featured.union({g['id'] for g in selected_featured})
    next_banners = select_banners(banner_candidates, future_recent_banners, args.banner_count, exclude_ids={g['id'] for g in selected_banners})
    next_featured = select_featured(all_sorted, future_recent_featured, args.featured_count, exclude_ids={g['id'] for g in selected_featured})
    next_premieres = select_premieres(all_sorted, now_year, args.premieres_count, exclude_ids={g['id'] for g in selected_premieres})

    # prepare banners objects
    banners_out = []
    for i, g in enumerate(selected_banners, start=1):
        img = g.get('bannerImage')
        if not img:
            img = g.get('image')
        banners_out.append({
            'id': f'banner-{g.get("id")}',
            'title': g.get('title'),
            'subtitle': g.get('tagline') or '',
            'image': img,
            'link': f'PS-Details.html?id={g.get("id")}',
            'gameId': g.get('id'),
            'priority': i
        })

    # update platforms entries for PS5 if present
    ps5 = data.get('platforms', {}).get('PS5')
    if ps5 and 'sections' in ps5:
        sections = ps5['sections']
        if 'featured' in sections:
            sections['featured']['games'] = [g['id'] for g in selected_featured]
        if 'premieres' in sections:
            sections['premieres']['games'] = [g['id'] for g in selected_premieres]

    # update game statuses (preserve original in _origStatus)
    for g in games_list:
        g['_origStatus'] = g.get('status', '')
        g.pop('autoCuration', None)
        g['autoCuration'] = ''

    for g in selected_featured:
        games[g['id']]['autoCuration'] = 'Destacado'
    for g in selected_premieres:
        games[g['id']]['autoCuration'] = 'Estreno'
    for g in selected_banners:
        games[g['id']]['autoCuration'] = 'Banner'

    # append to history
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'banners': [g['id'] for g in selected_banners],
        'featured': [g['id'] for g in selected_featured],
        'premieres': [g['id'] for g in selected_premieres]
    }
    history.insert(0, entry)
    # keep history reasonable
    cfg['curationHistory'] = history[:52]
    cfg['lastCurated'] = entry['timestamp']
    cfg['curationSchedule'] = {
        'current': entry,
        'next': {
            'timestamp': (datetime.utcnow() + timedelta(weeks=1)).isoformat(),
            'banners': [g['id'] for g in next_banners],
            'featured': [g['id'] for g in next_featured],
            'premieres': [g['id'] for g in next_premieres]
        }
    }

    # write changes
    print('\nResumen curación:')
    print('  Banners:', ', '.join([g['id'] for g in selected_banners]))
    print('  Featured:', ', '.join([g['id'] for g in selected_featured]))
    print('  Premieres:', ', '.join([g['id'] for g in selected_premieres]))
    print('Siguiente semana (previsión):')
    print('  Banners:', ', '.join([g['id'] for g in next_banners]))
    print('  Featured:', ', '.join([g['id'] for g in next_featured]))
    print('  Premieres:', ', '.join([g['id'] for g in next_premieres]))

    if args.dry_run:
        print('\nDry-run: no se escribieron cambios en games.json')
        return 0

    # apply
    data['banners'] = banners_out
    bak = save_games(games_path, data)
    print(f'Wrote {games_path} (backup: {bak})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
