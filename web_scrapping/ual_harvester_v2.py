import requests
import json
import time
import urllib3

# Desactivar advertencias de SSL inseguro (necesario para Termux/Android)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://campus.ual.es/webual/json/academica"
OUTPUT_FILE = "ual_raw_data.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.ual.es/"
}

def log(msg):
    print(f"[UAL-HARVESTER] {msg}")

def fetch_json(url):
    try:
        # verify=False es OBLIGATORIO en Termux para evitar errores de certificados SSL
        r = requests.get(url, headers=HEADERS, timeout=20, verify=False)
        if r.status_code == 200:
            return r.json()
        log(f"Error HTTP {r.status_code} en {url}")
    except Exception as e:
        log(f"Excepción de conexión: {e}")
    return None

def main():
    log("Iniciando descarga (Modo Inseguro SSL activado)...")
    
    # 1. Catálogo
    url_cat = f"{BASE_URL}/titulaciones/GRA/es"
    data = fetch_json(url_cat)
    
    if not data or 'planes' not in data:
        log("FATAL: No se pudo descargar el catálogo.")
        return

    planes = [p for p in data['planes'] if p.get('referencia')]
    log(f"Planes encontrados: {len(planes)}")
    
    final_data = []
    
    # 2. Detalles
    for i, p in enumerate(planes):
        cod = p['referencia']
        nom = p.get('nom_plan', 'Sin nombre')
        log(f"[{i+1}/{len(planes)}] {nom}")
        
        # Estructura
        p['structure'] = fetch_json(f"{BASE_URL}/planestudios/{cod}/es")
        final_data.append(p)
        time.sleep(0.1)

    # 3. Guardar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    log(f"FIN. Guardado en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
