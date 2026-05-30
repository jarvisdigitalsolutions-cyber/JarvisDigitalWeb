#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertir URLs a Netlify Function Proxy
Soluciona CORS bloqueado por Cloudflare usando proxy server-side
"""

import json
import urllib.parse
from pathlib import Path

INPUT_FILE = "rescaner-DLPS\\gamesv3.json"
OUTPUT_FILE = "rescaner-DLPS\\gamesv3_netlify_proxy.json"

# URL del proxy en Netlify
NETLIFY_PROXY = "/.netlify/functions/proxy-image?url="

def cargar_json(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def convertir_urls():
    """Convierte URLs directas a proxy de Netlify"""
    
    print("="*70)
    print("🔧 Convertir URLs a Netlify Function Proxy")
    print("="*70)
    
    datos = cargar_json(INPUT_FILE)
    
    if "games" not in datos:
        print("❌ Estructura no reconocida")
        return
    
    juegos = datos["games"]
    total = len(juegos)
    
    print(f"\n📊 Total de juegos: {total}")
    print(f"🔗 Proxy: {NETLIFY_PROXY}")
    
    actualizado = 0
    
    for game_id, juego in juegos.items():
        changed = False
        
        # Procesar imagen principal
        if juego.get('image') and juego['image'].startswith('http'):
            encoded = urllib.parse.quote(juego['image'], safe='')
            juego['image'] = NETLIFY_PROXY + encoded
            changed = True
        
        # Procesar preview images
        if juego.get('previewImages'):
            nuevas_previews = []
            for url in juego['previewImages']:
                if url.startswith('http'):
                    encoded = urllib.parse.quote(url, safe='')
                    nuevas_previews.append(NETLIFY_PROXY + encoded)
                else:
                    nuevas_previews.append(url)
            juego['previewImages'] = nuevas_previews
            changed = True
        
        # Procesar banner image
        if juego.get('bannerImage') and juego['bannerImage'].startswith('http'):
            encoded = urllib.parse.quote(juego['bannerImage'], safe='')
            juego['bannerImage'] = NETLIFY_PROXY + encoded
            changed = True
        
        if changed:
            actualizado += 1
    
    datos["games"] = juegos
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n✅ {actualizado} juegos actualizados")
    print(f"📄 Archivo: {OUTPUT_FILE}")
    
    # Mostrar ejemplo
    primer_juego = next(iter(juegos.values()))
    img = primer_juego.get('image', 'N/A')
    print(f"\n📋 Ejemplo de URL:")
    print(f"   {img[:100]}...")
    print(f"\n{'='*70}")

if __name__ == "__main__":
    try:
        convertir_urls()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
