import json
import requests
import os

# --- RUTAS ABSOLUTAS ---
INPUT_FILE = "/sdcard/Download/uja_raw_data.json"
OUTPUT_HTML = "/sdcard/Download/uja_failure_debug.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def probe():
    print("🕵️ SONDA DE FALLOS UJA (Inteligencia Artificial)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No encuentro {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    target_url = None
    target_name = None

    # Buscar el grado fallido específico (157A)
    for d in data:
        code = d.get('degree_code', '')
        if "157A" in code: # Grado en IA
            if d.get('subjects'):
                subj = d['subjects'][0]
                target_url = subj['guide_url']
                target_name = subj['name']
                print(f"🎯 Titulación fallida encontrada: {d['degree']}")
                print(f"📍 Asignatura objetivo: {target_name}")
                break
    
    if target_url:
        print(f"🔗 Descargando: {target_url}")
        try:
            r = requests.get(target_url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            
            with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
                f.write(r.text)
                
            print(f"✅ ÉXITO. HTML guardado en: {OUTPUT_HTML}")
            print("📤 Por favor, sube este archivo. Necesito ver por qué el parser V6 lo ignora.")
            
        except Exception as e:
            print(f"❌ Error de descarga: {e}")
    else:
        print("❌ No se encontró el Grado 157A en el JSON.")

if __name__ == "__main__":
    probe()
