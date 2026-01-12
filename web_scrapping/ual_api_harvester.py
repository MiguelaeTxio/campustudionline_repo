import requests
import json
import os
import sys

"""
UAL API HARVESTER
Objetivo: Extraer el catálogo de grados directamente de la API JSON de AngularJS.
Fuente descubierta: https://campus.ual.es/webual/json/academica/
"""

# Configuración basada en ingeniería inversa del HTML
BASE_API = "https://campus.ual.es/webual/json/academica/"
OUTPUT_DIR = "ual_data_json"

# Endpoints probables basados en ngResource: .get({tipo:"GRA", idioma:"es"})
# Patrones comunes de API REST en UAL/Angular
ENDPOINTS_TO_TRY = [
    f"{BASE_API}titulaciones/GRA/es",       # Patrón RESTful estricto
    f"{BASE_API}titulaciones?tipo=GRA&idioma=es", # Patrón Query Params
    f"{BASE_API}titulaciones/tipo/GRA/idioma/es"  # Patrón Verbose
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.ual.es/'
}

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[OK] Directorio creado: {OUTPUT_DIR}")

def fetch_json(url):
    print(f"[*] Probando endpoint: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15, verify=True) # verify=False si hay problemas de SSL en Termux antiguo
        print(f"    Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                # Validación básica: debe ser una lista o dict no vacío
                if data:
                    print(f"    [EXITO] Datos JSON obtenidos. Longitud/Claves: {len(data)}")
                    return data
            except json.JSONDecodeError:
                print("    [FALLO] La respuesta no es JSON válido.")
    except Exception as e:
        print(f"    [ERROR] {e}")
    return None

def main():
    ensure_dir()
    
    catalog_data = None
    
    # 1. Intentar obtener el catálogo general
    for url in ENDPOINTS_TO_TRY:
        catalog_data = fetch_json(url)
        if catalog_data:
            break
            
    if catalog_data:
        filename = os.path.join(OUTPUT_DIR, "ual_grados_catalogo.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(catalog_data, f, indent=4, ensure_ascii=False)
        print(f"\n[MISION CUMPLIDA] Catálogo guardado en: {filename}")
        print("Por favor, sube este archivo al servidor para proceder con la normalización.")
    else:
        print("\n[FRACASO] No se pudo conectar con la API JSON por ninguno de los métodos estándar.")
        print("Es posible que la URL requiera una estructura específica definida en 'academica_titulaciones.js'.")

if __name__ == "__main__":
    main()
