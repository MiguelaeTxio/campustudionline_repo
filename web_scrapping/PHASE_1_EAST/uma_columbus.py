import requests
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN TABULA RASA ---
URL_OBJETIVO = "https://sara.uma.es/pls/apex/f?p=101:1"
DEBUG_FILE = '/sdcard/Download/uma_debug_dump.html'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

print(f"--- INICIO EXPLORACIÓN: {URL_OBJETIVO} ---")

try:
    # 1. Conexión cruda
    r = requests.get(URL_OBJETIVO, headers=HEADERS, timeout=20)
    print(f"Status Code: {r.status_code}")
    
    if r.status_code != 200:
        print("!!! ERROR: La página no responde correctamente.")
        exit()

    # 2. Volcado de Seguridad (Empirismo Puro)
    with open(DEBUG_FILE, 'w', encoding='utf-8') as f:
        f.write(r.text)
    print(f"HTML volcado en: {DEBUG_FILE}")

    # 3. Análisis de Superficie
    soup = BeautifulSoup(r.text, 'html.parser')
    print(f"Título de la página: {soup.title.string.strip() if soup.title else 'SIN TÍTULO'}")

    # 4. Búsqueda de Selectores (SIN ASUMIR NOMBRES)
    print("\n--- BUSCANDO SELECTORES (<select>) ---")
    selects = soup.find_all('select')
    
    if not selects:
        print("ATENCIÓN: No se han encontrado elementos <select>.")
        print("Posibles causas: La página carga vía JavaScript o nos han bloqueado.")
    else:
        for s in selects:
            s_id = s.get('id', 'NO_ID')
            s_name = s.get('name', 'NO_NAME')
            options_count = len(s.find_all('option'))
            print(f"ENCONTRADO -> Tag: select | ID: '{s_id}' | Name: '{s_name}' | Opciones: {options_count}")
            # Imprimir las primeras 3 opciones para ver si tienen datos reales
            first_opts = s.find_all('option')[:3]
            for opt in first_opts:
                print(f"   Option sample: {opt.get_text(strip=True)} (Val: {opt.get('value')})")
            print("-" * 30)

except Exception as e:
    print(f"ERROR CRÍTICO: {e}")

print("--- FIN EXPLORACIÓN ---")
