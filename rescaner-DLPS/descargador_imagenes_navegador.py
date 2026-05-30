#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descargador de imágenes usando Playwright (navegador)
Evita bloqueos CORS/403
"""

import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# ============ CONFIGURACIÓN ============
INPUT_FILE = "gamesv3.json"
OUTPUT_FILE = "gamesv3_local.json"
IMG_DIR = r"..\..\Sony-Web\IMG\PS5"
TIMEOUT = 60000

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
    filename = url.split('/')[-1].split('?')[0]
    
    if '.' in filename:
        ext = filename.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'avif']:
            return ext
    
    return 'jpg'

def descargar_imagen(context, url, game_id, img_path):
    """Descarga una imagen usando Playwright context.request"""
    try:
        ext = obtener_extension(url)
        filename = f"{game_id}.{ext}"
        filepath = img_path / filename
        
        if filepath.exists():
            print(f"    ✓ Ya existe: {filename}")
            return filename
        
        print(f"    📥 Descargando: {url[-40:]}...")
        
        # Usar context.request con headers para evitar bloqueos
        try:
            response = context.request.get(
                url,
                timeout=TIMEOUT,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://dlpsgame.com/',
                    'Accept': 'image/*'
                }
            )
            
            if response.ok and response.status == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.body())
                print(f"    ✓ Descargado: {filename}")
                return filename
            else:
                print(f"    ⚠️  Status {response.status}")
                return None
                
        except Exception as e:
            print(f"    ❌ Error de red: {str(e)[:40]}")
            return None
        
    except Exception as e:
        print(f"    ❌ Error: {str(e)[:60]}")
        return None

def procesar_juegos():
    """Procesa juegos y descarga imágenes con navegador"""
    
    print("="*60)
    print("📥 DESCARGADOR DE IMÁGENES CON NAVEGADOR")
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
    
    try:
        with sync_playwright() as p:
            # Usar headless para no abrir ventana
            browser = p.chromium.launch(headless=True)
            
            # Primero, visitar la página principal para pasar verificación Cloudflare
            print("🔐 Pasando verificación Cloudflare...")
            context = browser.new_context()
            page = context.new_page()
            try:
                page.goto('https://dlpsgame.com', timeout=TIMEOUT, wait_until='domcontentloaded')
                print("✓ Verificación completada\n")
            except Exception as e:
                print(f"⚠️  Aviso: {str(e)[:40]}\n")
            page.close()
            
            # Ahora descargar usando context.request (reutiliza cookies/sesión)
            for i, (game_id, juego) in enumerate(juegos.items(), 1):
                titulo = juego.get('title', game_id)
                print(f"{i}. {titulo}")
                
                # Descargar imagen principal
                image_url = juego.get('image', '')
                if image_url and image_url.startswith('http'):
                    filename = descargar_imagen(context, image_url, game_id, img_path)
                    if filename:
                        juego['image'] = f"IMG/PS5/{filename}"
                        descargados += 1
                    else:
                        errores += 1
                
                # Descargar previewImages
                preview_images = juego.get('previewImages', [])
                if preview_images:
                    nuevas_previews = []
                    for j, prev_url in enumerate(preview_images):
                        if prev_url.startswith('http'):
                            preview_filename = descargar_imagen(
                                context,
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
                
                # Descargar bannerImage
                banner_url = juego.get('bannerImage', '')
                if banner_url and banner_url.startswith('http'):
                    banner_filename = descargar_imagen(
                        context,
                        banner_url,
                        f"{game_id}_banner",
                        img_path
                    )
                    if banner_filename:
                        juego['bannerImage'] = f"IMG/PS5/{banner_filename}"
                        descargados += 1
                    else:
                        errores += 1
                
                # Pausa
                time.sleep(0.5)
                
                # Guardar progreso cada 10 juegos
                if i % 10 == 0:
                    if es_estructurado:
                        datos['games'] = juegos
                    else:
                        datos = juegos
                    guardar_json(datos, OUTPUT_FILE)
                    print(f"  💾 Progreso guardado ({i}/{total})\n")
            
            browser.close()
    
    except Exception as e:
        print(f"\n❌ Error general: {e}")
    
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
