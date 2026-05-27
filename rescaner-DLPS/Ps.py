from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import re
import time

BASE_URL = "https://dlpsgame.com/category/ps5/page/{}/"
START_PAGE = 1
END_PAGE = 3  # Comenzar con 3 páginas para probar

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

games = {}
seen = set()

try:
    with sync_playwright() as p:
        # Usar chromium (más rápido que Firefox)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

games = {}
seen = set()

        for page_num in range(START_PAGE, END_PAGE + 1):
            url = BASE_URL.format(page_num)
            print(f"📄 Página {page_num}/{END_PAGE}: {url}")
            try:
                page.goto(url, wait_until="networkidle")
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
                        obj = make_game_obj(title, href, image)
                        games[obj["id"]] = obj

            except Exception as e:
                print(f"   ❌ Error en {url}: {e}")
        
        browser.close()

except Exception as e:
    print(f"Error general: {e}")

output = {
    "config": {
        "version": "1.0",
        "lastUpdated": "2026-05-27",
        "description": "Catálogo PS5 generado automáticamente desde DLPSGame"
    },
    "games": games
}

with open("ps5_games.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"✓ LISTO!")
print(f"{'='*50}")
print(f"📊 Total de juegos: {len(games)}")
print(f"📁 Archivo guardado: ps5_games.json")
print(f"{'='*50}")