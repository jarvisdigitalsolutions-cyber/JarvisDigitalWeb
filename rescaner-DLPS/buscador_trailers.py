from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time
import re

# ============ CONFIGURACIÓN ============
INPUT_FILE = "game2.json"
OUTPUT_FILE = "game2_con_trailers.json"

def cargar_json(archivo):
    """Carga el archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    """Guarda datos en JSON"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def extraer_video_id(url):
    """Extrae el ID de video de una URL de YouTube"""
    # Formatos: youtube.com/watch?v=ID, youtu.be/ID, etc
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def buscar_trailer(titulo, platform="PS5"):
    """Busca el trailer oficial en YouTube"""
    
    query = f"{titulo} official trailer {platform}"
    youtube_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    
    print(f"    🔍 Buscando: {query}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Sin mostrar ventana
            page = browser.new_page()
            
            page.goto(youtube_url, timeout=30000)
            time.sleep(3)
            
            # Extraer primer resultado
            soup = BeautifulSoup(page.content(), "html.parser")
            
            # Buscar enlaces de video
            video_links = soup.select('a#video-title')
            
            if video_links:
                href = video_links[0].get('href', '')
                if href:
                    # Convertir a URL completa
                    if href.startswith('/'):
                        trailer_url = f"https://www.youtube.com{href}"
                    else:
                        trailer_url = href
                    
                    print(f"    ✓ Encontrado: {trailer_url[:60]}...")
                    browser.close()
                    return trailer_url
            
            print(f"    ❌ No encontrado")
            browser.close()
            return ""
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return ""

def procesar_juegos():
    """Procesa juegos y busca trailers faltantes"""
    
    print("="*60)
    print("🎬 BUSCADOR DE TRAILERS PARA GAME2.JSON")
    print("="*60)
    
    # Cargar JSON
    print("\n📂 Cargando datos...")
    datos = cargar_json(INPUT_FILE)
    
    if "games" in datos:
        juegos = datos["games"]
    else:
        juegos = datos
    
    total = len(juegos)
    sin_trailer = 0
    encontrados = 0
    
    print(f"📊 Total de juegos: {total}")
    
    # Contar sin trailer
    for jid, juego in juegos.items():
        if not juego.get("trailer"):
            sin_trailer += 1
    
    print(f"🎥 Sin trailer: {sin_trailer}/{total}")
    print(f"\n{'='*60}")
    
    # Procesar juegos sin trailer
    for i, (jid, juego) in enumerate(juegos.items(), 1):
        trailer = juego.get("trailer", "").strip()
        
        # Si ya tiene trailer, saltar
        if trailer:
            print(f"\n{i}. ✓ {juego['title']} (ya tiene trailer)")
            continue
        
        print(f"\n{i}. 🔎 {juego['title']}")
        platform = juego.get("platform", "PS5")
        
        # Buscar trailer
        trailer_url = buscar_trailer(juego['title'], platform)
        
        if trailer_url:
            juego['trailer'] = trailer_url
            encontrados += 1
            print(f"    ✅ Actualizado")
        else:
            print(f"    ⚠️  No se encontró")
        
        # Pausa para no sobrecargar
        time.sleep(2)
        
        # Guardar progreso cada 5 juegos
        if i % 5 == 0:
            guardar_json(datos, OUTPUT_FILE)
            print(f"    💾 Progreso guardado ({i}/{total})")
    
    # Guardar final
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n{'='*60}")
    print("✓ ¡LISTO!")
    print("="*60)
    print(f"✅ Trailers encontrados: {encontrados}/{sin_trailer}")
    print(f"📁 Archivo guardado: {OUTPUT_FILE}")
    print("="*60)

if __name__ == "__main__":
    try:
        procesar_juegos()
    except KeyboardInterrupt:
        print("\n\n⏸️  Cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
