import requests
import os

"""
UAL JS FETCHER
Objetivo: Descargar los archivos JS que definen las rutas de la API.
"""

BASE_URL = "https://www.ual.es/application/blocks/ual_db_rest/js/"
TARGETS = [
    "academica_titulaciones.js",
    "academica_planestudios.js",
    "academica_asignaturas.js"
]

OUTPUT_DIR = "ual_js_definitions"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def main():
    ensure_dir()
    print("[*] Iniciando descarga de definiciones JS...")
    
    for filename in TARGETS:
        url = BASE_URL + filename
        print(f"    Descargando: {filename}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                local_path = os.path.join(OUTPUT_DIR, filename)
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"    [OK] Guardado en {local_path}")
            else:
                print(f"    [ERROR] Status {r.status_code} para {url}")
        except Exception as e:
            print(f"    [FAIL] {e}")

    print("\n[FIN] Archivos listos para subir al servidor.")

if __name__ == "__main__":
    main()
