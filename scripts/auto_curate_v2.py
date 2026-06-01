#!/usr/bin/env python3
"""
scripts/auto_curate_v2.py (MEJORADO)

Script mejorado con:
- Algoritmo de scoring más sofisticado
- Consideración de popularidad/engagement
- Mejor distribución de géneros
- Premieres ordenadas por fecha
"""
import argparse
import json
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


def parse_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def compute_score_v2(g, now_year, include_popularity=True):
    """
    Score mejorado: 
    - 40% rating (quality)
    - 25% recency (freshness)
    - 15% discount (value)
    - 15% popularity (engagement) 
    - 5% exclusivity bonus
    """
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
    
    # Popularity: visualizations or engagement score (si existe en JSON)
    popularity = parse_float(g.get('popularity', 0)) / 100.0 if include_popularity else 0.0
    
    # Exclusivity bonus: PS5 exclusive
    is_exclusive = 1.0 if g.get('exclusive', False) else 0.0
    
    norm_rating = min(1.0, rating / 5.0)
    score = (
        0.40 * norm_rating +      # Rating (quality)
        0.25 * recency +          # Recency (freshness) 
        0.15 * discount +         # Discount (value)
        0.15 * min(1.0, popularity) +  # Popularity
        0.05 * is_exclusive       # Exclusivity
    )
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
    recent_premieres = set()
    for entry in history:
        ts = entry.get('timestamp')
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            continue
        if dt >= cutoff:
            recent_banners.update(entry.get('banners', []))
            recent_featured.update(entry.get('featured', []))
            recent_premieres.update(entry.get('premieres', []))
    return recent_banners, recent_featured, recent_premieres


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


def select_by_genres(candidates, genre_count=None):
    """Distribuye selección por géneros para diversidad"""
    if not genre_count:
        return candidates
    
    by_genre = defaultdict(list)
    for g in candidates:
        genres = g.get('genres', [])
        main_genre = genres[0] if genres else 'Other'
        by_genre[main_genre].append(g)
    
    selected = []
    for genre in by_genre:
        # Máximo N juegos por género
        selected.extend(by_genre[genre][:max(1, len(candidates) // len(by_genre))])
    
    return selected[:len(candidates)]


def select_banners(candidates, recent_banners, banner_count, exclude_ids=None):
    exclude_ids = set(exclude_ids or [])
    selected = [
        g for g in candidates 
        if g['id'] not in exclude_ids and g['id'] not in recent_banners
    ][:banner_count]
    
    if len(selected) < banner_count:
        for g in candidates:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= banner_count:
                break
    return selected


def select_featured(sorted_games, recent_featured, featured_count, exclude_ids=None):
    exclude_ids = set(exclude_ids or [])
    selected = [
        g for g in sorted_games 
        if g['id'] not in exclude_ids and g['id'] not in recent_featured
    ][:featured_count]
    
    if len(selected) < featured_count:
        for g in sorted_games:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= featured_count:
                break
    return selected


def select_premieres(sorted_games, now_year, premieres_count, recent_premieres=None, exclude_ids=None):
    """Premieres ordenadas por fecha de lanzamiento (más próximas primero)"""
    exclude_ids = set(exclude_ids or [])
    recent_premieres = set(recent_premieres or [])
    
    # Filtrar por status Próximamente
    candidates = [g for g in sorted_games if g.get('status', '').lower() == 'próximamente']
    
    # Ordenar por release date (más próximas primero = menor año/mes)
    def sort_key(x):
        try:
            release = int(x.get('release') or 2099)
        except (ValueError, TypeError):
            release = 2099
        return (release, x.get('id', ''))
    
    candidates.sort(key=sort_key)
    
    selected = [
        g for g in candidates 
        if g['id'] not in exclude_ids and g['id'] not in recent_premieres
    ][:premieres_count]
    
    if len(selected) < premieres_count:
        for g in candidates:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= premieres_count:
                break
    
    return selected


def select_recent_releases(sorted_games, now_year, recent_releases_count, exclude_ids=None):
    """Recientes por fecha (más nuevos primero)"""
    exclude_ids = set(exclude_ids or [])
    
    candidates = []
    for g in sorted_games:
        if g.get('status', '').lower() == 'disponible':
            try:
                release = int(g.get('release', now_year))
                if release >= 2025:
                    candidates.append(g)
            except (ValueError, TypeError):
                pass
    
    # Ordenar por release descendente (más reciente primero)
    candidates.sort(key=lambda x: int(x.get('release', 0)), reverse=True)
    
    selected = [
        g for g in candidates 
        if g['id'] not in exclude_ids
    ][:recent_releases_count]
    
    if len(selected) < recent_releases_count:
        for g in candidates:
            if g['id'] not in exclude_ids and g not in selected:
                selected.append(g)
            if len(selected) >= recent_releases_count:
                break
    
    return selected


def main():
    parser = argparse.ArgumentParser(description='Auto-curate con algoritmo mejorado')
    parser.add_argument('--games', default=None, help='Ruta a Sony-Web/games.json')
    parser.add_argument('--banner-count', type=int, default=3)
    parser.add_argument('--featured-count', type=int, default=6)
    parser.add_argument('--premieres-count', type=int, default=4)
    parser.add_argument('--recent-releases-count', type=int, default=4)
    parser.add_argument('--no-repeat-weeks', type=int, default=4)
    parser.add_argument('--version', choices=['v1', 'v2'], default='v2', help='Versión de algoritmo')
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

    # Elegir versión de scoring
    if args.version == 'v2':
        score_func = lambda g: compute_score_v2(g, now_year)
        print('🚀 Usando algoritmo MEJORADO v2 (40% rating, 25% recency, 15% discount, 15% popularity, 5% exclusive)')
    else:
        score_func = lambda g: compute_score_v2(g, now_year, include_popularity=False)
        print('📊 Usando algoritmo clásico v1 (55% rating, 30% recency, 15% discount)')

    # Compute scores
    for g in games_list:
        g['_score'] = score_func(g)

    # Ensure history
    cfg = data.setdefault('config', {})
    history = cfg.setdefault('curationHistory', [])

    recent_banners, recent_featured, recent_premieres = recent_ids_from_history(history, args.no_repeat_weeks)

    # Select current
    banner_candidates = [g for g in games_list if valid_banner_candidate(g)]
    banner_candidates.sort(key=lambda x: x.get('_score', 0), reverse=True)

    all_sorted = sorted(games_list, key=lambda x: x.get('_score', 0), reverse=True)
    
    selected_banners = select_banners(banner_candidates, recent_banners, args.banner_count)
    selected_featured = select_featured(all_sorted, recent_featured, args.featured_count)
    selected_premieres = select_premieres(all_sorted, now_year, args.premieres_count, recent_premieres)
    selected_recent_releases = select_recent_releases(all_sorted, now_year, args.recent_releases_count)

    # Next week forecast
    future_recent_banners = recent_banners.union({g['id'] for g in selected_banners})
    future_recent_featured = recent_featured.union({g['id'] for g in selected_featured})
    future_recent_premieres = recent_premieres.union({g['id'] for g in selected_premieres})
    
    next_banners = select_banners(banner_candidates, future_recent_banners, args.banner_count, 
                                   exclude_ids={g['id'] for g in selected_banners})
    next_featured = select_featured(all_sorted, future_recent_featured, args.featured_count,
                                    exclude_ids={g['id'] for g in selected_featured})
    next_premieres = select_premieres(all_sorted, now_year, args.premieres_count, future_recent_premieres,
                                      exclude_ids={g['id'] for g in selected_premieres})
    next_recent_releases = select_recent_releases(all_sorted, now_year, args.recent_releases_count,
                                                 exclude_ids={g['id'] for g in selected_recent_releases})

    # Prepare banners objects
    banners_out = []
    for i, g in enumerate(selected_banners, start=1):
        img = g.get('bannerImage') or g.get('image')
        banners_out.append({
            'id': f'banner-{g.get("id")}',
            'title': g.get('title'),
            'subtitle': g.get('tagline') or '',
            'image': img,
            'link': f'PS-Details.html?id={g.get("id")}',
            'gameId': g.get('id'),
            'priority': i
        })

    # Update PS5 sections
    ps5 = data.get('platforms', {}).get('PS5')
    if ps5 and 'sections' in ps5:
        sections = ps5['sections']
        if 'featured' in sections:
            sections['featured']['games'] = [g['id'] for g in selected_featured]
        if 'premieres' in sections:
            sections['premieres']['games'] = [g['id'] for g in selected_premieres]
        if 'recentReleases' in sections:
            sections['recentReleases']['games'] = [g['id'] for g in selected_recent_releases]

    # Update statuses
    for g in games_list:
        g['_origStatus'] = g.get('status', '')
        g.pop('autoCuration', None)
        g['autoCuration'] = ''

    for g in selected_featured:
        games[g['id']]['autoCuration'] = 'Destacado'
    for g in selected_premieres:
        games[g['id']]['autoCuration'] = 'Próximo'
    for g in selected_banners:
        games[g['id']]['autoCuration'] = 'Banner'

    # History entry
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'banners': [g['id'] for g in selected_banners],
        'featured': [g['id'] for g in selected_featured],
        'premieres': [g['id'] for g in selected_premieres],
        'recentReleases': [g['id'] for g in selected_recent_releases]
    }
    history.insert(0, entry)
    cfg['curationHistory'] = history[:52]
    cfg['lastCurated'] = entry['timestamp']
    cfg['curationSchedule'] = {
        'current': entry,
        'next': {
            'timestamp': (datetime.utcnow() + timedelta(weeks=1)).isoformat(),
            'banners': [g['id'] for g in next_banners],
            'featured': [g['id'] for g in next_featured],
            'premieres': [g['id'] for g in next_premieres],
            'recentReleases': [g['id'] for g in next_recent_releases]
        }
    }

    # Output
    print('\n✅ Resumen curación ACTUAL:')
    print(f'  🎨 Banners ({len(selected_banners)}):', ', '.join([g['id'] for g in selected_banners]))
    print(f'  ⭐ Featured ({len(selected_featured)}):', ', '.join([g['id'] for g in selected_featured]))
    print(f'  🎬 Premieres ({len(selected_premieres)}):', ', '.join([g['id'] for g in selected_premieres]))
    print(f'  🆕 Recientes ({len(selected_recent_releases)}):', ', '.join([g['id'] for g in selected_recent_releases]))
    
    print('\n📅 Previsión PRÓXIMA SEMANA:')
    print(f'  🎨 Banners ({len(next_banners)}):', ', '.join([g['id'] for g in next_banners]))
    print(f'  ⭐ Featured ({len(next_featured)}):', ', '.join([g['id'] for g in next_featured]))
    print(f'  🎬 Premieres ({len(next_premieres)}):', ', '.join([g['id'] for g in next_premieres]))
    print(f'  🆕 Recientes ({len(next_recent_releases)}):', ', '.join([g['id'] for g in next_recent_releases]))

    if args.dry_run:
        print('\n⚠️  Dry-run: no se escribieron cambios')
        return 0

    data['banners'] = banners_out
    bak = save_games(games_path, data)
    print(f'\n✨ Actualizado {games_path}')
    print(f'   Backup: {bak}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
