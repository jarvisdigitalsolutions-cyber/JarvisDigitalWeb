#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESTRATEGIA CORS PARA NETLIFY:
En lugar de descargar imágenes (bloqueadas por dlpsgame),
usaremos un proxy CORS o servir desde CDN.

Dos opciones:
1. Usar CORS proxy: https://cors-anywhere.herokuapp.com/ (gratuito pero limitado)
2. Usar servicio de proxy: https://images.weserv.nl/ (para redimensionar imágenes)
3. Mantener URLs externas + configurar headers CORS en Netlify
"""

import json
from pathlib import Path

INPUT_FILE = "gamesv3.json"
OUTPUT_FILE = "gamesv3_cors_fixed.json"

# Proxy CORS disponibles (prueba cada uno)
CORS_PROXIES = [
    "https://cors-anywhere.herokuapp.com/",
    "https://api.allorigins.win/get?url=",
    "https://images.weserv.nl/?url=",
]

def cargar_json(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def procesar_urls():
    """Reemplaza URLs con CORS proxy"""
    
    print("="*60)
    print("🔧 ESTRATEGIA CORS PARA NETLIFY")
    print("="*60)
    
    datos = cargar_json(INPUT_FILE)
    
    if "games" not in datos:
        print("❌ Estructura de JSON no reconocida")
        return
    
    juegos = datos["games"]
    total = len(juegos)
    
    print(f"\n📊 Total de juegos: {total}")
    print("\n" + "="*60)
    print("OPCIONES:")
    print("1. Mantener URLs externas (requiere CORS headers en Netlify)")
    print("2. Usar CORS proxy (https://images.weserv.nl/)")
    print("3. Solo procesar juegos sin URLs vacías")
    print("="*60 + "\n")
    
    opcion = input("¿Qué opción prefieres? (1/2/3): ").strip()
    
    if opcion == "2":
        print("\n📝 Aplicando CORS proxy a todas las URLs...")
        proxy = "https://images.weserv.nl/?url="
        
        for game_id, juego in juegos.items():
            # Procesar imagen principal
            if juego.get('image') and juego['image'].startswith('http'):
                juego['image'] = proxy + juego['image']
            
            # Procesar preview images
            if juego.get('previewImages'):
                juego['previewImages'] = [
                    proxy + url if url.startswith('http') else url
                    for url in juego['previewImages']
                ]
            
            # Procesar banner
            if juego.get('bannerImage') and juego['bannerImage'].startswith('http'):
                juego['bannerImage'] = proxy + juego['bannerImage']
        
        print(f"✅ URLs convertidas al proxy")
    
    elif opcion == "3":
        print("\n🔍 Filtrando juegos sin imágenes...")
        juegos_sin_imagenes = {
            gid: g for gid, g in juegos.items()
            if not g.get('image') or not g['image'].startswith('http')
        }
        print(f"❌ Juegos sin imagen: {len(juegos_sin_imagenes)}")
        print(f"✅ Juegos con imagen: {len(juegos) - len(juegos_sin_imagenes)}")
    
    else:
        print("✅ Manteniendo URLs externas")
        print("⚠️  Asegúrate de configurar CORS headers en netlify.toml")
    
    datos["games"] = juegos
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n{'='*60}")
    print(f"✓ JSON guardado: {OUTPUT_FILE}")
    print("="*60)
    
    # Mostrar estadísticas
    games_con_imagen = sum(1 for g in juegos.values() if g.get('image'))
    print(f"\n📊 Estadísticas:")
    print(f"  Total juegos: {total}")
    print(f"  Con imagen: {games_con_imagen}")
    print(f"  Sin imagen: {total - games_con_imagen}")

if __name__ == "__main__":
    try:
        procesar_urls()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
