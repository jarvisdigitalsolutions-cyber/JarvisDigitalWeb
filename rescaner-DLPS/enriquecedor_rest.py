#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para enriquecer datos PS5 usando Google Gemini API REST
Sin usar la librería deprecada
"""

import json
import requests
import time

# ============ CONFIGURACIÓN ============
GEMINI_API_KEY = "AIzaSyCtRAn99V8gYXEwkGNu_1cx_1Sp2TnFLFw"
JUEGOS_PRUEBA = 10
INPUT_FILE = "ps5_games.json"
OUTPUT_FILE = "ps5_games_enriquecido.json"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

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
    Envía un juego a Gemini REST API para llenar datos
    """
    
    prompt = f"""Para el videojuego PS5 "{titulo}", proporciona SOLO en formato JSON (sin markdown, sin explicaciones):

{{
  "genres": ["género1", "género2"],
  "tagline": "frase corta promocional",
  "trailer": "URL del trailer o vacío"
}}

Si no encuentras información, usa valores vacíos."""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 500
        }
    }
    
    # Reintentos
    max_intentos = 3
    for intento in range(max_intentos):
        try:
            if intento > 0:
                espera = 10 * intento
                print(f"    ⏳ Esperando {espera}s antes de reintentar...")
                time.sleep(espera)
            
            print(f"    📤 Enviando a Gemini API REST...")
            response = requests.post(API_URL, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                respuesta_texto = result['candidates'][0]['content']['parts'][0]['text'].strip()
                
                # Limpiar respuesta
                if respuesta_texto.startswith("```json"):
                    respuesta_texto = respuesta_texto[7:]
                if respuesta_texto.startswith("```"):
                    respuesta_texto = respuesta_texto[3:]
                if respuesta_texto.endswith("```"):
                    respuesta_texto = respuesta_texto[:-3]
                
                datos = json.loads(respuesta_texto.strip())
                return datos
            else:
                print(f"    ⚠️  Respuesta vacía")
                return {"genres": [], "tagline": "", "trailer": ""}
            
        except json.JSONDecodeError as e:
            print(f"    ❌ Error JSON: {e}")
            if intento == max_intentos - 1:
                return {"genres": [], "tagline": "", "trailer": ""}
        except requests.exceptions.RequestException as e:
            if "429" in str(e):
                print(f"    ⚠️  Rate limit (429) - Reintentando...")
                if intento == max_intentos - 1:
                    return {"genres": [], "tagline": "", "trailer": ""}
            else:
                print(f"    ❌ Error HTTP: {e}")
                return {"genres": [], "tagline": "", "trailer": ""}
        except Exception as e:
            print(f"    ❌ Error: {e}")
            if intento == max_intentos - 1:
                return {"genres": [], "tagline": "", "trailer": ""}

def procesar_prueba():
    """Procesa solo 10 juegos para prueba"""
    
    print("="*60)
    print("🎮 PRUEBA: ENRIQUECEDOR PS5 CON GEMINI (REST API)")
    print("="*60)
    
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
    
    for i, jid in enumerate(juegos_ids, 1):
        titulo = juegos[jid]["title"]
        print(f"\n{i}. {titulo}")
        
        enriquecido = enriquecer_juego(titulo)
        
        # Actualizar datos
        juegos[jid]["genres"] = enriquecido.get("genres", [])
        juegos[jid]["tagline"] = enriquecido.get("tagline", "")
        juegos[jid]["trailer"] = enriquecido.get("trailer", "")
        
        print(f"   ✓ Géneros: {', '.join(enriquecido.get('genres', []))}")
        print(f"   ✓ Tagline: {enriquecido.get('tagline', '(vacío)')}")
        print(f"   ✓ Trailer: {'Sí' if enriquecido.get('trailer') else 'No'}")
        
        # Pequeña pausa MAYOR para no sobrecargar
        time.sleep(5)  # 5 segundos entre solicitudes
    
    # Guardar
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n{'='*60}")
    print("✓ ¡PRUEBA COMPLETADA!")
    print("="*60)
    print(f"📁 Archivo guardado: {OUTPUT_FILE}")
    print(f"✅ Primeros {JUEGOS_PRUEBA} juegos enriquecidos")
    print("="*60)

if __name__ == "__main__":
    procesar_prueba()
