#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para enriquecer datos PS5 usando Google Gemini API
Prueba con 10 juegos primero
"""

import json
import google.generativeai as genai

# ============ CONFIGURACIÓN ============
GEMINI_API_KEY = "AIzaSyCtRAn99V8gYXEwkGNu_1cx_1Sp2TnFLFw"
JUEGOS_PRUEBA = 10  # Solo probar con 10 juegos
INPUT_FILE = "ps5_games.json"
OUTPUT_FILE = "ps5_games_enriquecido.json"

# ============ INICIALIZAR ============
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
    Envía un juego individual a Gemini para llenar datos
    """
    
    prompt = f"""Para el videojuego PS5 "{titulo}", proporciona SOLO en formato JSON (sin markdown, sin explicaciones):

{{
  "genres": ["género1", "género2"],
  "tagline": "frase corta promocional (máx 10 palabras)",
  "trailer": "URL de YouTube o enlace del trailer (o vacío si no encuentras)"
}}

Si no encuentras información, usa valores vacíos. SOLO devuelve el JSON."""
    
    try:
        response = model.generate_content(prompt)
        respuesta_texto = response.text.strip()
        
        # Limpiar respuesta si viene con markdown
        if respuesta_texto.startswith("```json"):
            respuesta_texto = respuesta_texto[7:]
        if respuesta_texto.startswith("```"):
            respuesta_texto = respuesta_texto[3:]
        if respuesta_texto.endswith("```"):
            respuesta_texto = respuesta_texto[:-3]
        
        datos = json.loads(respuesta_texto.strip())
        return datos
        
    except json.JSONDecodeError as e:
        print(f"    ❌ Error JSON: {e}")
        return {"genres": [], "tagline": "", "trailer": ""}
    except Exception as e:
        print(f"    ❌ Error API: {e}")
        return {"genres": [], "tagline": "", "trailer": ""}

def procesar_prueba():
    """Procesa solo 10 juegos para prueba"""
    
    print("="*60)
    print("🎮 PRUEBA: ENRIQUECEDOR PS5 CON GEMINI API")
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
        print(f"   🔍 Enriqueciendo...")
        
        enriquecido = enriquecer_juego(titulo)
        
        # Actualizar datos
        juegos[jid]["genres"] = enriquecido.get("genres", [])
        juegos[jid]["tagline"] = enriquecido.get("tagline", "")
        juegos[jid]["trailer"] = enriquecido.get("trailer", "")
        
        print(f"   ✓ Géneros: {', '.join(enriquecido.get('genres', []))}")
        print(f"   ✓ Tagline: {enriquecido.get('tagline', '(vacío)')}")
        print(f"   ✓ Trailer: {'Encontrado' if enriquecido.get('trailer') else '(vacío)'}")
    
    # Guardar
    guardar_json(datos, OUTPUT_FILE)
    
    print(f"\n{'='*60}")
    print("✓ ¡PRUEBA COMPLETADA!")
    print("="*60)
    print(f"📁 Archivo guardado: {OUTPUT_FILE}")
    print(f"✅ Primeros {JUEGOS_PRUEBA} juegos enriquecidos")
    print(f"📝 Revisa ps5_games_enriquecido.json para ver los resultados")
    print("="*60)

if __name__ == "__main__":
    procesar_prueba()
