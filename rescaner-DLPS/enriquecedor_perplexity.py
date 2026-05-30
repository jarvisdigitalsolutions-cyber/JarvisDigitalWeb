#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para enriquecer datos PS5 usando Perplexity API
Más rápido y con mejor rate limit que Gemini
"""

import json
import requests
import time

# ============ CONFIGURACIÓN ============
PERPLEXITY_API_KEY = "tu-api-key-aqui"  # ⚠️ REEMPLAZA CON TU API KEY
JUEGOS_PRUEBA = 10
INPUT_FILE = "ps5_games.json"
OUTPUT_FILE = "ps5_games_enriquecido.json"

API_URL = "https://api.perplexity.ai/chat/completions"

def cargar_json(archivo):
    """Carga el archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    """Guarda datos en JSON"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def enriquecer_juego(titulo):
    """
    Envía un juego a Perplexity API para llenar datos
    """
    
    prompt = f"""Para el videojuego PS5 "{titulo}", responde EXACTAMENTE en este formato JSON (sin markdown):

{{
  "genres": ["género1", "género2"],
  "tagline": "frase corta promocional máx 10 palabras",
  "trailer": "URL del trailer en YouTube o vacío"
}}

Responde SOLO el JSON, nada más."""
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 400,
        "temperature": 0.2
    }
    
    try:
        print(f"    📤 Enviando a Perplexity API...")
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            respuesta_texto = result['choices'][0]['message']['content'].strip()
            
            # Limpiar respuesta
            if respuesta_texto.startswith("```json"):
                respuesta_texto = respuesta_texto[7:]
            if respuesta_texto.startswith("```"):
                respuesta_texto = respuesta_texto[3:]
            if respuesta_texto.endswith("```"):
                respuesta_texto = respuesta_texto[:-3]
            
            datos = json.loads(respuesta_texto.strip())
            print(f"    ✓ Éxito")
            return datos
        else:
            print(f"    ⚠️  Respuesta vacía")
            return {"genres": [], "tagline": "", "trailer": ""}
        
    except json.JSONDecodeError as e:
        print(f"    ❌ Error JSON: {e}")
        print(f"       Respuesta: {respuesta_texto[:100]}...")
        return {"genres": [], "tagline": "", "trailer": ""}
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Error HTTP: {e}")
        return {"genres": [], "tagline": "", "trailer": ""}
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return {"genres": [], "tagline": "", "trailer": ""}

def procesar_prueba():
    """Procesa solo 10 juegos para prueba"""
    
    print("="*60)
    print("🎮 PRUEBA: ENRIQUECEDOR PS5 CON PERPLEXITY API")
    print("="*60)
    
    # Verificar API Key
    if PERPLEXITY_API_KEY == "tu-api-key-aqui":
        print("❌ ERROR: Reemplaza 'tu-api-key-aqui' con tu API Key de Perplexity")
        print("📌 Obtén una en: https://www.perplexity.ai/settings/api")
        exit(1)
    
    # Cargar JSON
    print("\n📂 Cargando datos...")
    datos = cargar_json(INPUT_FILE)
    juegos = datos["games"]
    total_juegos = len(juegos)
    
    print(f"📊 Total disponible: {total_juegos}")
    print(f"🧪 Procesando: {JUEGOS_PRUEBA} juegos (PRUEBA)")
    
    # Procesar solo los primeros 10
    juegos_ids = list(juegos.keys())[:JUEGOS_PRUEBA]
    
    print(f"\n{'='*60}")
    
    éxitos = 0
    fallos = 0
    
    for i, jid in enumerate(juegos_ids, 1):
        titulo = juegos[jid]["title"]
        print(f"\n{i}. {titulo}")
        
        enriquecido = enriquecer_juego(titulo)
        
        # Actualizar datos
        juegos[jid]["genres"] = enriquecido.get("genres", [])
        juegos[jid]["tagline"] = enriquecido.get("tagline", "")
        juegos[jid]["trailer"] = enriquecido.get("trailer", "")
        
        if enriquecido.get("genres") or enriquecido.get("tagline"):
            print(f"   ✓ Géneros: {', '.join(enriquecido.get('genres', []))}")
            print(f"   ✓ Tagline: {enriquecido.get('tagline', '(vacío)')}")
            éxitos += 1
        else:
            fallos += 1
        
        # Pausa entre solicitudes (Perplexity es más tolerante)
        time.sleep(2)
    
    # Guardar
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n{'='*60}")
    print("✓ ¡PRUEBA COMPLETADA!")
    print("="*60)
    print(f"✅ Éxitos: {éxitos}/{JUEGOS_PRUEBA}")
    print(f"❌ Fallos: {fallos}/{JUEGOS_PRUEBA}")
    print(f"📁 Archivo guardado: {OUTPUT_FILE}")
    print("="*60)

if __name__ == "__main__":
    procesar_prueba()
