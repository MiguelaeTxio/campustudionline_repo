import requests
import json
import os
import time
import urllib3

# Desactivar warnings de SSL para garantizar ejecución en entornos Android antiguos/Termux
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Objetivos reconstruidos mediante ingeniería inversa
TARGETS = [
    {
        "name": "GRADOS_MAESTRO",
        "file": "ual_grados_legacy.json",
        "url": "https://campus.ual.es/webual/json/academica/bTitulaciones_OficialesJSON.jsp",
        "params": {
            "ramas": "",
            "tipo_titulacion": "GRA", # Grados
            "idioma": "es",
            "historico": "No",
            "extincion": "No"
        }
    },
    {
        "name": "ASIGNATURAS_EJEMPLO_6210",
        "file": "ual_asignaturas_legacy_6210.json",
        "url": "https://campus.ual.es/webual/json/academica/bAsignaturasJSON.jsp",
        "params": {
            "idTit": "6210", # ID extraído del ejemplo visual
            "idioma": "es"
        }
    },
    {
        "name": "RAMAS_API",
        "file": "ual_ramas_api.json",
        "url": "https://campus.ual.es/ual/api/estudios/planes/ramas/es",
        "params": {}
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Origin": "https://www.ual.es",
    "Referer": "https://www.ual.es/"
}

def run_harvester():
    print("--- UAL HARVESTER V1 (RECONSTRUCTED) ---")
    
    for target in TARGETS:
        print(f"\n[+] Target: {target['name']}")
        print(f"    URL: {target['url']}")
        
        try:
            # verify=False es crucial en scraping rápido desde dispositivos móviles para evitar líos de certificados CA
            resp = requests.get(target['url'], params=target['params'], headers=HEADERS, timeout=30, verify=False)
            print(f"    Status: {resp.status_code}")
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    # Guardamos el JSON crudo para análisis de esquema
                    with open(target['file'], 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    count = len(data) if isinstance(data, list) else len(data.keys())
                    print(f"    SUCCESS: Retrieved {count} items.")
                    print(f"    Saved to: {os.path.abspath(target['file'])}")
                    
                except json.JSONDecodeError:
                    print(f"    FAIL: Response is not JSON.")
                    print(f"    Preview: {resp.text[:200]}")
            else:
                print(f"    FAIL: Non-200 Status Code.")
            
        except Exception as e:
            print(f"    ERROR: {e}")
        
        # Cortesía básica
        time.sleep(1)

if __name__ == "__main__":
    run_harvester()
