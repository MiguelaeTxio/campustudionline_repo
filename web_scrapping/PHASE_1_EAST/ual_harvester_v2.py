import requests
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Endpoint JBoss descubierto en 'academica_titulaciones.js'
# Dominio corregido: campus.ual.es
URL = "https://campus.ual.es/ual/api/estudios/planes/titulaciones/GRA/es"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Origin": "https://www.ual.es",
    "Referer": "https://www.ual.es/"
}

def harvest_degrees():
    print(f"--- UAL HARVESTER V2 (DEGREES FIX) ---")
    print(f"Target: {URL}")
    
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=30, verify=False)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            filename = "ual_grados_jboss.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Análisis rápido de estructura
            if isinstance(data, list):
                print(f"SUCCESS: Retrieved list with {len(data)} items.")
            elif isinstance(data, dict):
                print(f"SUCCESS: Retrieved root object with keys: {list(data.keys())}")
            
            print(f"Saved to: {os.path.abspath(filename)}")
        else:
            print(f"FAIL: Status {resp.status_code}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    harvest_degrees()
