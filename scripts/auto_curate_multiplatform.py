#!/usr/bin/env python3
"""
scripts/auto_curate_multiplatform.py

Script mejorado que cura TODAS las plataformas: PS5, PS4, PS3
- homeFeatured y popular: ESTÁTICOS (no cambian)
- featured, premieres, recentReleases: DINÁMICOS (cambian cada semana)
- Predicciones para 3 semanas
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


def compute_score_v2(g, now_year):
    """Score mejorado: 40% rating + 25% recency + 15% discount + 15% popularity + 5% exclusive"""
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
    popularity = parse_float(g.get('popularity', 0)) / 100.0
    is_exclusive = 1.0 if g.get('exclusive', False) else 0.0
    
    norm_rating = min(1.0, rating / 5.0)
    score = (
        0.40 * norm_rating +
        0.25 * recency +
        0.15 * discount +
        0.15 * min(1.0, popularity) +
        0.05 * is_exclusive
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
    recent_featured = set()
    recent_premieres = set()
    recent_releases = set()
    for entry in history:
        ts = entry.get('timestamp')
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            continue
        if dt >= cutoff:
            recent_featured.update(entry.get('featured', []))
            recent_premieres.update(entry.get('premieres', []))
            recent_releases.update(entry.get('recentReleases', []))
    return recent_featured, recent_premieres, recent_releases


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
    """Premieres ordenadas por fecha"""
    exclude_ids = set(exclude_ids or [])
    recent_premieres = set(recent_premieres or [])
    
    candidates = [g for g in sorted_games if g.get('status', '').lower() == 'próximamente']
    
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
    """Recientes ordenadas por fecha (más nuevos primero)"""
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
    parser = argparse.ArgumentParser(description='Auto-curate para PS5, PS4, PS3')
    parser.add_argument('--games', default=None, help='Ruta a Sony-Web/games.json')
    parser.add_argument('--featured-count', type=int, default=6)
    parser.add_argument('--premieres-count', type=int, default=4)
    parser.add_argument('--recent-releases-count', type=int, default=4)
    parser.add_argument('--no-repeat-weeks', type=int, default=4)
    parser.add_argument('--weeks-forecast', type=int, default=3, help='Semanas de predicción')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]
    games_path = Path(args.games) if args.games else repo_root / 'Sony-Web' / 'games.json'

    if not games_path.exists():
        print(f'❌ ERROR: no encuentro {games_path}')
        return 2

    data = load_games(games_path)
    games = data.get('games', {})
    games_list = list(games.values())

    now_year = datetime.utcnow().year
    now_date = datetime.utcnow()

    # Compute scores
    for g in games_list:
        g['_score'] = compute_score_v2(g, now_year)

    # Setup history
    cfg = data.setdefault('config', {})
    history = cfg.setdefault('curationHistory', [])

    recent_featured, recent_premieres, recent_releases = recent_ids_from_history(history, args.no_repeat_weeks)

    # Sort by score
    all_sorted = sorted(games_list, key=lambda x: x.get('_score', 0), reverse=True)

    # CURRENT selections (all platforms same source)
    current_featured = select_featured(all_sorted, recent_featured, args.featured_count)
    current_premieres = select_premieres(all_sorted, now_year, args.premieres_count, recent_premieres)
    current_recents = select_recent_releases(all_sorted, now_year, args.recent_releases_count)

    # FORECAST for N weeks
    forecasts = [{'featured': current_featured, 'premieres': current_premieres, 'recents': current_recents}]
    
    future_featured = recent_featured.union({g['id'] for g in current_featured})
    future_premieres = recent_premieres.union({g['id'] for g in current_premieres})
    future_recents = recent_releases.union({g['id'] for g in current_recents})

    for week_num in range(1, args.weeks_forecast):
        next_featured = select_featured(all_sorted, future_featured, args.featured_count, 
                                       exclude_ids={g['id'] for g in forecasts[week_num-1]['featured']})
        next_premieres = select_premieres(all_sorted, now_year, args.premieres_count, future_premieres,
                                         exclude_ids={g['id'] for g in forecasts[week_num-1]['premieres']})
        next_recents = select_recent_releases(all_sorted, now_year, args.recent_releases_count,
                                             exclude_ids={g['id'] for g in forecasts[week_num-1]['recents']})
        
        forecasts.append({'featured': next_featured, 'premieres': next_premieres, 'recents': next_recents})
        
        future_featured.update({g['id'] for g in next_featured})
        future_premieres.update({g['id'] for g in next_premieres})
        future_recents.update({g['id'] for g in next_recents})

    # Update platforms sections
    platforms = data.get('platforms', {})
    for platform_name in ['PS5', 'PS4', 'PS3']:
        if platform_name not in platforms:
            continue
        
        platform = platforms[platform_name]
        if 'sections' not in platform:
            platform['sections'] = {}
        
        sections = platform['sections']
        
        # IMPORTANT: homeFeatured y popular NO CAMBIAN (STATIC)
        # Solo actualizar: featured, premieres, recentReleases
        
        if 'featured' in sections:
            sections['featured']['games'] = [g['id'] for g in current_featured]
            print(f"  {platform_name} featured: {len(sections['featured']['games'])} juegos")
        
        if 'premieres' in sections:
            sections['premieres']['games'] = [g['id'] for g in current_premieres]
            print(f"  {platform_name} premieres: {len(sections['premieres']['games'])} juegos")
        
        if 'recentReleases' in sections:
            sections['recentReleases']['games'] = [g['id'] for g in current_recents]
            print(f"  {platform_name} recentReleases: {len(sections['recentReleases']['games'])} juegos")

    # Update history
    entry = {
        'timestamp': now_date.isoformat(),
        'featured': [g['id'] for g in current_featured],
        'premieres': [g['id'] for g in current_premieres],
        'recentReleases': [g['id'] for g in current_recents]
    }
    history.insert(0, entry)
    cfg['curationHistory'] = history[:52]
    cfg['lastCurated'] = entry['timestamp']
    
    # Build forecast schedule
    forecast_schedule = {}
    for week_num, forecast in enumerate(forecasts):
        ts = (now_date + timedelta(weeks=week_num)).isoformat()
        forecast_schedule[f'week_{week_num}'] = {
            'timestamp': ts,
            'featured': [g['id'] for g in forecast['featured']],
            'premieres': [g['id'] for g in forecast['premieres']],
            'recentReleases': [g['id'] for g in forecast['recents']]
        }
    
    cfg['curationForecast'] = forecast_schedule

    # Print summary
    print('\n' + '='*60)
    print('🎮 MULTIPLATFORM AUTO-CURATION COMPLETED')
    print('='*60)
    print(f'\n📅 Fecha: {now_date.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'🔄 Plataformas: PS5, PS4, PS3')
    print(f'📊 Secciones actualizadas: featured, premieres, recentReleases')
    print(f'⏳ Secciones ESTÁTICAS: homeFeatured, popular')
    print(f'🔮 Predicciones: {args.weeks_forecast} semanas')
    
    print('\n✅ ESTA SEMANA (Current Selection):')
    print(f'  Featured (6): {", ".join([g["id"] for g in current_featured[:3]])}...')
    print(f'  Premieres (4): {", ".join([g["id"] for g in current_premieres])}')
    print(f'  Recientes (4): {", ".join([g["id"] for g in current_recents])}')
    
    print(f'\n🔮 PRÓXIMAS {args.weeks_forecast} SEMANAS:')
    for week_num, forecast in enumerate(forecasts[1:], start=1):
        ts = (now_date + timedelta(weeks=week_num)).strftime("%Y-%m-%d")
        print(f'  Semana {week_num} ({ts}):')
        print(f'    - Premieres: {", ".join([g["id"] for g in forecast["premieres"]])}')
    
    print(f'\n📁 NOTAS:')
    print(f'  ✓ homeFeatured: SIN CAMBIOS (8 juegos fijos)')
    print(f'  ✓ popular: SIN CAMBIOS (7 juegos fijos)')
    print(f'  ✓ featured/premieres/recentReleases: Actualizados')
    
    if args.dry_run:
        print(f'\n⚠️  DRY-RUN: No se escribieron cambios')
        return 0

    bak = save_games(games_path, data)
    print(f'\n✨ Guardado en {games_path}')
    print(f'   Backup: {bak}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
