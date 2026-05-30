#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descargador de imágenes de juegos y actualizador de rutas JSON
Descarga imágenes de dlpsgame.com y reemplaza URLs por rutas locales
"""

import json
import os
import requests
from urllib.parse import urlparse
from pathlib import Path
import time

# ============ CONFIGURACIÓN ============
INPUT_FILE = "gamesv3.json"
OUTPUT_FILE = "gamesv3_local.json"
IMG_DIR = r"..\..\Sony-Web\IMG\PS5"  # Ruta relativa desde rescaner-DLPS
TIMEOUT = 30

def crear_directorio():
    """Crea el directorio si no existe"""
    img_path = Path(IMG_DIR)
    img_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Directorio: {img_path.absolute()}")
    return img_path

def cargar_json(archivo):
    """Carga el archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    """Guarda datos en JSON"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def obtener_extension(url):
    """Obtiene la extensión del archivo desde la URL"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    # Tomar la última parte (nombre de archivo)
    filename = os.path.basename(path)
    
    # Obtener extensión
    if '.' in filename:
        ext = filename.split('.')[-1].lower()
        # Validar que sea una extensión de imagen
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'avif']:
            return ext
    
    # Por defecto jpg
    return 'jpg'

def descargar_imagen(url, game_id, img_path):
    """Descarga una imagen desde una URL"""
    try:
        # Obtener extensión
        ext = obtener_extension(url)
        filename = f"{game_id}.{ext}"
        filepath = img_path / filename
        
        # Si ya existe, no descargar de nuevo
        if filepath.exists():
            print(f"    ✓ Ya existe: {filename}")
            return filename
        
        print(f"    📥 Descargando: {url[:60]}...")
        
        # Descargar
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        
        # Guardar
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"    ✓ Descargado: {filename}")
        return filename
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def procesar_juegos():
    """Procesa juegos y descarga imágenes"""
    
    print("="*60)
    print("📥 DESCARGADOR DE IMÁGENES PS5")
    print("="*60)
    
    # Crear directorio
    print("\n📁 Preparando directorio...")
    img_path = crear_directorio()
    
    # Cargar JSON
    print("\n📂 Cargando JSON...")
    datos = cargar_json(INPUT_FILE)
    
    if "games" in datos:
        juegos = datos["games"]
        es_estructurado = True
    else:
        juegos = datos
        es_estructurado = False
    
    total = len(juegos)
    print(f"📊 Total de juegos: {total}")
    
    print(f"\n{'='*60}\n")
    
    descargados = 0
    errores = 0
    
    for i, (game_id, juego) in enumerate(juegos.items(), 1):
        titulo = juego.get('title', game_id)
        print(f"{i}. {titulo}")
        
        # Descargar imagen principal
        image_url = juego.get('image', '')
        if image_url and image_url.startswith('http'):
            filename = descargar_imagen(image_url, game_id, img_path)
            if filename:
                juego['image'] = f"IMG/PS5/{filename}"
                descargados += 1
            else:
                errores += 1
        
        # Descargar previewImages si existen
        preview_images = juego.get('previewImages', [])
        if preview_images:
            nuevas_previews = []
            for j, prev_url in enumerate(preview_images):
                if prev_url.startswith('http'):
                    # Renombrar con índice para múltiples imágenes
                    preview_filename = descargar_imagen(
                        prev_url, 
                        f"{game_id}_preview{j}", 
                        img_path
                    )
                    if preview_filename:
                        nuevas_previews.append(f"IMG/PS5/{preview_filename}")
                    else:
                        errores += 1
                else:
                    nuevas_previews.append(prev_url)
            
            if nuevas_previews:
                juego['previewImages'] = nuevas_previews
        
        # Descargar bannerImage si existe
        banner_url = juego.get('bannerImage', '')
        if banner_url and banner_url.startswith('http'):
            banner_filename = descargar_imagen(
                banner_url, 
                f"{game_id}_banner", 
                img_path
            )
            if banner_filename:
                juego['bannerImage'] = f"IMG/PS5/{banner_filename}"
                descargados += 1
            else:
                errores += 1
        
        # Pausa para no sobrecargar
        time.sleep(0.5)
        
        # Guardar progreso cada 20 juegos
        if i % 20 == 0:
            if es_estructurado:
                datos['games'] = juegos
            else:
                datos = juegos
            guardar_json(datos, OUTPUT_FILE)
            print(f"  💾 Progreso guardado ({i}/{total})\n")
    
    # Guardar final
    if es_estructurado:
        datos['games'] = juegos
    else:
        datos = juegos
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n{'='*60}")
    print("✓ ¡LISTO!")
    print("="*60)
    print(f"✅ Descargados: {descargados}")
    print(f"❌ Errores: {errores}")
    print(f"📁 Imágenes en: {img_path.absolute()}")
    print(f"📄 JSON guardado: {OUTPUT_FILE}")
    print("="*60)

if __name__ == "__main__":
    try:
        procesar_juegos()
    except KeyboardInterrupt:
        print("\n\n⏸️  Cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
