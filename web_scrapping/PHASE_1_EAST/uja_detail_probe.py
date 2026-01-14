# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uja_detail_probe.py
import json
import requests
import os

INPUT_FILE = "uja_raw_data.json"
OUTPUT_HTML = "uja_subject_detail.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def probe():
    print("🕵️ INICIANDO SONDA DE DETALLE UJA...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ No encuentro {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Buscar una asignatura aleatoria (o la primera)
    if not data or not data[0].get('subjects'):
        print("❌ El JSON parece vacío o sin asignaturas.")
        return

    # Cogemos la primera asignatura del primer grado
    target_subject = data[0]['subjects'][0]
    url = target_subject['guide_url']
    name = target_subject['name']

    print(f"🎯 Objetivo: {name}")
    print(f"🔗 URL: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"✅ HTML guardado en: {OUTPUT_HTML}")
        print("📤 Por favor, sube este archivo para analizar dónde está el dato del 'Curso'.")
        
    except Exception as e:
        print(f"❌ Error descargando detalle: {e}")

if __name__ == "__main__":
    probe()
