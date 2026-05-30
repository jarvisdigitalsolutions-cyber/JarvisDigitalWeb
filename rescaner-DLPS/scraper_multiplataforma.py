from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import re
import time

# ============ CONFIGURACIÓN ============
PLATAFORMAS = {
    "PS4": {
        "url": "https://dlpsgame.com/category/ps4/page/{}/",
        "pages": 16,  # ~319 juegos
        "output": "ps4_games.json"
    },
    "PS3": {
        "url": "https://dlpsgame.com/category/ps3/page/{}/",
        "pages": 8,   # ~160 juegos
        "output": "ps3_games.json"
    }
}

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text

def make_game_obj(title, url="", image="", platform="PS5"):
    return {
        "id": slugify(title),
        "title": title,
        "tagline": "",
        "platform": platform,
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
        "trailer": "",
        "bannerImage": "",
        "_score": 0,
        "_origStatus": "Pendiente",
        "autoCuration": ""
    }

def scrape_platform(platform_name, config):
    """Scrape una plataforma específica"""
    
    print(f"\n{'='*60}")
    print(f"📱 SCRAPEANDO {platform_name}")
    print(f"{'='*60}")
    
    games = {}
    seen = set()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            for page_num in range(1, config["pages"] + 1):
                url = config["url"].format(page_num)
                print(f"\n📄 Página {page_num}/{config['pages']}: {url}")
                
                try:
                    # Reintentos automáticos si falla
                    max_intentos = 3
                    for intento in range(max_intentos):
                        try:
                            page.goto(url, wait_until="networkidle", timeout=60000)
                            break
                        except Exception as err:
                            if intento < max_intentos - 1:
                                print(f"   ⏳ Reintentando ({intento+1}/{max_intentos-1})...")
                                time.sleep(5)
                            else:
                                raise err
                    
                    time.sleep(3)
                    
                    soup = BeautifulSoup(page.content(), "html.parser")
                    cards = soup.select("div.post.bar.hentry")
                    print(f"   ✓ Encontrados {len(cards)} juegos")
                    
                    for card in cards:
                        a = card.select_one("h2.post-title.entry-title a")
                        img = card.select_one("img")
                        
                        if not a:
                            continue
                        
                        title = a.get_text(strip=True)
                        href = a.get("href", "")
                        image = img.get("src", "") if img else ""
                        
                        if title and title not in seen:
                            seen.add(title)
                            obj = make_game_obj(title, href, image, platform_name)
                            games[obj["id"]] = obj
                    
                except Exception as e:
                    print(f"   ❌ Error en página {page_num}: {e}")
            
            browser.close()
    
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    # Guardar JSON
    output = {
        "config": {
            "version": "1.0",
            "lastUpdated": "2028-05-28",
            "platform": platform_name,
            "description": f"Catálogo {platform_name} generado automáticamente desde DLPSGame"
        },
        "games": games
    }
    
    with open(config["output"], "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✓ {platform_name} LISTO!")
    print(f"{'='*60}")
    print(f"📊 Total de juegos: {len(games)}")
    print(f"📁 Archivo guardado: {config['output']}")
    print(f"{'='*60}")
    
    return len(games)

if __name__ == "__main__":
    print("🎮 SCRAPER MULTIPLATAFORMA PS3/PS4/PS5")
    print("="*60)
    
    resultados = {}
    
    for platform_name, config in PLATAFORMAS.items():
        total = scrape_platform(platform_name, config)
        resultados[platform_name] = total
    
    print(f"\n{'='*60}")
    print("📊 RESUMEN FINAL")
    print(f"{'='*60}")
    for platform, total in resultados.items():
        print(f"✅ {platform}: {total} juegos")
    print(f"{'='*60}")
