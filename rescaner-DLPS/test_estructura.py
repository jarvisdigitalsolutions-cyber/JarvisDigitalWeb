#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para validar la estructura JSON que genera Ps.py
Simula algunos juegos para verificar el formato
"""

import json
import re

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text

def make_game_obj(title, url="", image=""):
    return {
        "id": slugify(title),
        "title": title,
        "tagline": "",
        "platform": "PS5",
        "edition": "",
        "developer": "",
        "release": "",
        "rating": "",
        "price": None,
        "oldPrice": None,
        "genres": [],
        "description": "",
        "features": [],
        "image": image,
        "url": url,
        "status": "Pendiente",
        "trailer": ""
    }

# Simular datos de prueba
test_games = [
    {
        "title": "Elden Ring",
        "url": "https://dlpsgame.com/elden-ring/",
        "image": "https://example.com/elden-ring.jpg"
    },
    {
        "title": "Final Fantasy VII Rebirth",
        "url": "https://dlpsgame.com/final-fantasy-vii-rebirth/",
        "image": "https://example.com/ffvii.jpg"
    },
    {
        "title": "Hogwarts Legacy",
        "url": "https://dlpsgame.com/hogwarts-legacy/",
        "image": "https://example.com/hogwarts.jpg"
    }
]

games = {}
for game_data in test_games:
    obj = make_game_obj(game_data["title"], game_data["url"], game_data["image"])
    games[obj["id"]] = obj

output = {
    "config": {
        "version": "1.0",
        "lastUpdated": "2026-05-27",
        "description": "Catálogo PS5 generado automáticamente desde DLPSGame"
    },
    "games": games
}

# Guardar JSON
with open("ps5_games_test.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✓ Estructura JSON validada correctamente")
print(f"✓ Juegos generados: {len(games)}")
print(f"✓ Archivo guardado: ps5_games_test.json")
print("\n" + "="*50)
print("ESTRUCTURA GENERADA:")
print("="*50)
print(json.dumps(output, ensure_ascii=False, indent=2))
