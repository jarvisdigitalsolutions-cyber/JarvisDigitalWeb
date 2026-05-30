#!/usr/bin/env python3
"""
Consolidate PS3, PS4, PS5 games into a single games.json file
"""
import json
import os
from datetime import datetime

def load_json(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {"games": {}}

def consolidate_games():
    """Consolidate PS3, PS4, PS5 games into one file"""
    
    # Load all three files
    ps5_data = load_json('../Sony-Web/games.json')
    ps4_data = load_json('./ps4_games.json')
    ps3_data = load_json('./ps3_games.json')
    
    # Start with PS5 config
    consolidated = {
        "config": {
            "version": "3.0",
            "lastUpdated": datetime.now().isoformat(),
            "description": "Catálogo centralizado unificado: PS3 + PS4 + PS5",
            "showPrices": ps5_data.get("config", {}).get("showPrices", False),
            "exchangeRateCU": ps5_data.get("config", {}).get("exchangeRateCU", 500),
            "platforms": ["PS3", "PS4", "PS5"],
            "curationHistory": ps5_data.get("config", {}).get("curationHistory", []),
            "lastCurated": ps5_data.get("config", {}).get("lastCurated", ""),
            "curationSchedule": ps5_data.get("config", {}).get("curationSchedule", {})
        },
        "games": {}
    }
    
    # Merge games
    ps5_games = ps5_data.get("games", {})
    ps4_games = ps4_data.get("games", {})
    ps3_games = ps3_data.get("games", {})
    
    # Add PS5 games
    consolidated["games"].update(ps5_games)
    
    # Add PS4 games (with ID prefix if needed to avoid duplicates)
    ps4_count = 0
    for game_id, game_data in ps4_games.items():
        if game_id not in consolidated["games"]:
            consolidated["games"][game_id] = game_data
            ps4_count += 1
    
    # Add PS3 games (with ID prefix if needed to avoid duplicates)
    ps3_count = 0
    for game_id, game_data in ps3_games.items():
        if game_id not in consolidated["games"]:
            consolidated["games"][game_id] = game_data
            ps3_count += 1
    
    # Save consolidated file
    output_path = '../Sony-Web/games.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)
    
    # Print summary
    total_games = len(consolidated["games"])
    print(f"✓ Consolidation complete!")
    print(f"  PS5 games: {len(ps5_games)}")
    print(f"  PS4 games added: {ps4_count}")
    print(f"  PS3 games added: {ps3_count}")
    print(f"  Total games: {total_games}")
    print(f"  Saved to: {output_path}")
    
    return consolidated

if __name__ == "__main__":
    consolidate_games()
