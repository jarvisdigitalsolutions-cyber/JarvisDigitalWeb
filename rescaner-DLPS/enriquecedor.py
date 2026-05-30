#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para enriquecer datos PS5 usando DeepSeek API
Llena: genres, tagline, trailer
Usa bloques de juegos para optimizar llamadas a la API
"""

import json
import os
from openai import OpenAI

# ============ CONFIGURACIÓN ============
DEEPSEEK_API_KEY = "sk-f0768e54725a4b93984374c9f0e71efa"  # ⚠️ REEMPLAZA CON TU API KEY
BLOQUE_SIZE = 10  # Procesa 10 juegos por llamada API
INPUT_FILE = "ps5_games.json"
OUTPUT_FILE = "ps5_games_enriquecido.json"
BACKUP_FILE = "ps5_games_backup.json"

# ============ INICIALIZAR CLIENTE ============
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def cargar_json(archivo):
    """Carga el archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(datos, archivo):
    """Guarda datos en JSON"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def enriquecer_bloque(juegos_bloque):
    """
    Envía un bloque de juegos a DeepSeek para llenar datos
    juegos_bloque: dict con {titulo: datos_juego}
    """
    
    # Construir prompt con los juegos
    titulos = list(juegos_bloque.keys())
    prompt = f"""Eres experto en videojuegos PS5. Para cada uno de estos juegos, proporciona:
- genres: Lista de géneros (máx 3)
- tagline: Frase corta promocional (máx 10 palabras)
- trailer: URL de trailer en YouTube (o dejar vacío si no encuentras)

Devuelve EXACTAMENTE en formato JSON. Solo el JSON, nada más:

Juegos:
{json.dumps(titulos, ensure_ascii=False, indent=2)}

Responde en este formato exacto (sin markdown):
{{
  "juego-title-1": {{"genres": ["Genre1", "Genre2"], "tagline": "frase", "trailer": "url"}},
  "juego-title-2": {{"genres": ["Genre1"], "tagline": "frase", "trailer": ""}}
}}
"""
    
    try:
        print(f"  📤 Enviando bloque de {len(titulos)} juegos a DeepSeek...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        respuesta_texto = response.choices[0].message.content.strip()
        
        # Limpiar respuesta (puede venir con markdown)
        if respuesta_texto.startswith("```json"):
            respuesta_texto = respuesta_texto[7:]
        if respuesta_texto.startswith("```"):
            respuesta_texto = respuesta_texto[3:]
        if respuesta_texto.endswith("```"):
            respuesta_texto = respuesta_texto[:-3]
        
        datos_enriquecidos = json.loads(respuesta_texto.strip())
        print(f"  ✓ Respuesta recibida y parseada")
        
        return datos_enriquecidos
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Error al parsear JSON: {e}")
        print(f"     Respuesta: {respuesta_texto[:200]}...")
        return {}
    except Exception as e:
        print(f"  ❌ Error en API: {e}")
        return {}

def procesar_juegos():
    """Procesa todos los juegos en bloques"""
    
    print("="*60)
    print("🎮 ENRIQUECEDOR DE DATOS PS5 CON DEEPSEEK")
    print("="*60)
    
    # Cargar JSON
    print("\n📂 Cargando datos...")
    datos = cargar_json(INPUT_FILE)
    
    # Hacer backup
    guardar_json(datos, BACKUP_FILE)
    print(f"✓ Backup guardado: {BACKUP_FILE}")
    
    juegos = datos["games"]
    total_juegos = len(juegos)
    print(f"📊 Total de juegos: {total_juegos}")
    
    # Procesar en bloques
    juegos_ids = list(juegos.keys())
    bloques_procesados = 0
    
    for i in range(0, total_juegos, BLOQUE_SIZE):
        bloque_ids = juegos_ids[i:i+BLOQUE_SIZE]
        bloque = {jid: juegos[jid]["title"] for jid in bloque_ids}
        
        inicio = i + 1
        fin = min(i + BLOQUE_SIZE, total_juegos)
        print(f"\n📄 Bloque {bloques_procesados + 1}: Juegos {inicio}-{fin}/{total_juegos}")
        
        # Enriquecer bloque
        datos_enriquecidos = enriquecer_bloque(bloque)
        
        # Actualizar JSON con nuevos datos
        for jid in bloque_ids:
            if jid in datos_enriquecidos:
                enriquecido = datos_enriquecidos[jid]
                juegos[jid]["genres"] = enriquecido.get("genres", [])
                juegos[jid]["tagline"] = enriquecido.get("tagline", "")
                juegos[jid]["trailer"] = enriquecido.get("trailer", "")
                print(f"  ✓ {juegos[jid]['title']}")
            else:
                print(f"  ⚠️  No se procesó: {jid}")
        
        bloques_procesados += 1
        
        # Guardar progreso cada bloque
        guardar_json(datos, OUTPUT_FILE)
        print(f"  💾 Progreso guardado ({fin}/{total_juegos})")
    
    print("\n" + "="*60)
    print("✓ ¡LISTO!")
    print("="*60)
    print(f"📊 Bloques procesados: {bloques_procesados}")
    print(f"📁 Archivo guardado: {OUTPUT_FILE}")
    print(f"💾 Backup disponible: {BACKUP_FILE}")
    print("="*60)

if __name__ == "__main__":
    # Verificar API Key
    if DEEPSEEK_API_KEY == "tu-api-key-aqui":
        print("❌ ERROR: Reemplaza 'tu-api-key-aqui' con tu API Key de DeepSeek")
        print("📌 Obtén una gratis en: https://platform.deepseek.com")
        exit(1)
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: No se encontró {INPUT_FILE}")
        exit(1)
    
    procesar_juegos()
