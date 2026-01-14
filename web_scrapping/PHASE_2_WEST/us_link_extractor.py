import requests
from bs4 import BeautifulSoup
import json
import time
import os

# CONFIGURACIÓN ACTUALIZADA
TARGET_URL = "https://www.us.es/estudiar/que-estudiar/oferta-de-grados"
OUTPUT_FILENAME = "us_degrees.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def extract_degrees():
    print(f"--- Iniciando extracción desde: {TARGET_URL} ---")
    
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        print("Conexión establecida exitosamente.")
    except Exception as e:
        print(f"[ERROR CRÍTICO] No se pudo acceder a la web: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    degrees = []
    
    # Búsqueda amplia de enlaces
    links = soup.find_all('a', href=True)
    
    print(f"Analizando {len(links)} enlaces encontrados...")
    
    for link in links:
        href = link['href']
        text = link.get_text(strip=True)
        
        if not text or len(text) < 5:
            continue
            
        # Normalización de URL
        if href.startswith("/"):
            full_url = f"https://www.us.es{href}"
        elif href.startswith("http"):
            full_url = href
        else:
            continue

        # CRITERIO DE SELECCIÓN REFINADO:
        # Buscamos patrones que indiquen una ficha de grado
        # Patrones observados en US: /estudiar/que-estudiar/oferta-de-grados/grado-en-x
        is_degree_path = "/oferta-de-grados/" in full_url
        is_degree_text = "grado en" in text.lower() or "doble grado" in text.lower()

        if (is_degree_path or is_degree_text) and "facultad" not in text.lower():
            degrees.append({
                "name": text,
                "url": full_url
            })

    # Deduplicación
    unique_degrees = {d['url']: d for d in degrees}.values()
    final_list = list(unique_degrees)

    # SALIDA
    output_data = {
        "university": "Universidad de Sevilla (US)",
        "source": TARGET_URL,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(final_list),
        "items": final_list
    }
    
    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n--- Extracción Completada ---")
    print(f"Grados encontrados: {len(final_list)}")
    print(f"Archivo generado: {os.path.abspath(OUTPUT_FILENAME)}")

if __name__ == "__main__":
    extract_degrees()
