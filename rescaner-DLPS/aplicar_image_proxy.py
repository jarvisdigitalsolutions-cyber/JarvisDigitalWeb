#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLUCIÓN DEFINITIVA: Imagen Proxy para Netlify
==============================================

El problema: dlpsgame.com bloquea CORS y descargas directas.
Soluciones:
1. Usar images.weserv.nl como proxy (gratuito, rápido, cachea)
2. Servir proxy desde función Netlify
3. Reemplazar URLs en JSON con proxy URLs
"""

import json
from pathlib import Path

INPUT_FILE = "gamesv3.json"
OUTPUT_FILE = "gamesv3_with_proxy.json"

# Proxy de imágenes gratuito y confiable
IMAGE_PROXY = "https://images.weserv.nl/?url="

def cargar_json(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def agregar_proxy_a_urls():
    """Agrega proxy a todas las URLs de imágenes"""
    
    print("="*70)
    print("🖼️  SOLUCIÓN CORS: Agregando Image Proxy a URLs")
    print("="*70)
    
    datos = cargar_json(INPUT_FILE)
    
    if "games" not in datos:
        print("❌ Estructura de JSON no reconocida")
        return
    
    juegos = datos["games"]
    total = len(juegos)
    
    print(f"\n📊 Total de juegos: {total}")
    print(f"🔗 Proxy a usar: {IMAGE_PROXY}")
    print(f"\n{'='*70}")
    
    actualizado = 0
    
    for game_id, juego in juegos.items():
        changed = False
        
        # Procesar imagen principal
        if juego.get('image') and juego['image'].startswith('http'):
            juego['image'] = IMAGE_PROXY + juego['image']
            changed = True
        
        # Procesar preview images
        if juego.get('previewImages'):
            nuevas_previews = []
            for url in juego['previewImages']:
                if url.startswith('http'):
                    nuevas_previews.append(IMAGE_PROXY + url)
                else:
                    nuevas_previews.append(url)
            juego['previewImages'] = nuevas_previews
            changed = True
        
        # Procesar banner image
        if juego.get('bannerImage') and juego['bannerImage'].startswith('http'):
            juego['bannerImage'] = IMAGE_PROXY + juego['bannerImage']
            changed = True
        
        if changed:
            actualizado += 1
    
    datos["games"] = juegos
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n✅ {actualizado} juegos actualizados con proxy")
    print(f"📄 Archivo guardado: {OUTPUT_FILE}")
    print(f"\n{'='*70}")
    
    # Mostrar ejemplo
    primer_juego = next(iter(juegos.values()))
    print("\n📋 Ejemplo de URL después:")
    print(f"   {primer_juego.get('image', 'N/A')[:80]}...")

if __name__ == "__main__":
    try:
        agregar_proxy_a_urls()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
