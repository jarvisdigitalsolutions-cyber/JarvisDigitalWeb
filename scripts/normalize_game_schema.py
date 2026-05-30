#!/usr/bin/env python3
import json
import shutil
import time
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


def load_games(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_games(path: Path, data: dict):
    ts = int(time.time())
    bak = path.with_name(f'games.json.bak.{ts}')
    shutil.copy2(path, bak)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return bak


def main():
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]
    games_path = repo_root / 'Sony-Web' / 'games.json'

    data = load_games(games_path)
    games = data.get('games', {})
    now_year = time.localtime().tm_year

    updated = []
    for game_id, game in games.items():
        had_changes = False

        banner_image = game.get('bannerImage')
        image = game.get('image')
        preview_images = game.get('previewImages')

        if not isinstance(preview_images, list) or not preview_images:
            if banner_image:
                derived = [banner_image]
                if image and image not in derived:
                    derived.append(image)
                game['previewImages'] = derived
            elif image:
                game['previewImages'] = [image]
            else:
                game['previewImages'] = []
            had_changes = True
        elif isinstance(preview_images, list):
            if banner_image and banner_image not in preview_images:
                preview_images.insert(0, banner_image)
                had_changes = True
            if image and image not in preview_images:
                preview_images.append(image)
                had_changes = True

        if '_score' not in game or not isinstance(game.get('_score'), (int, float)):
            game['_score'] = compute_score(game, now_year)
            had_changes = True

        if '_origStatus' not in game or not isinstance(game.get('_origStatus'), str):
            game['_origStatus'] = game.get('status') or ''
            had_changes = True

        if 'autoCuration' not in game:
            game['autoCuration'] = ''
            had_changes = True

        if had_changes:
            updated.append(game_id)

    if updated:
        bak = save_games(games_path, data)
        print(f'Normalized {len(updated)} entries in {games_path} (backup: {bak})')
    else:
        print('No schema updates needed.')


if __name__ == '__main__':
    main()
