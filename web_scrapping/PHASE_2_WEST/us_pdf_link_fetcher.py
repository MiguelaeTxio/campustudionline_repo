import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random

# --- CONFIGURACIÓN ---
INPUT_FILE = "/sdcard/Download/us_clean_subjects.json"
OUTPUT_FILE = "/sdcard/Download/us_subjects_with_pdf_urls.json"
STATE_FILE = "/sdcard/Download/us_pdf_fetch_state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def load_json(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_pdf_url(html_url):
    if not html_url:
        return None
    
    try:
        response = requests.get(html_url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Estrategia 1: Buscar enlace que diga "Proyecto docente"
        target_link = soup.find('a', string=lambda t: t and "proyecto docente" in t.lower())
        
        # Estrategia 2: Buscar cualquier PDF si falla lo anterior
        if not target_link:
            target_link = soup.find('a', href=lambda h: h and h.endswith('.pdf'))
            
        if target_link:
            href = target_link['href']
            if href.startswith("/"):
                return f"https://www.us.es{href}"
            return href
            
    except Exception as e:
        print(f"    [ERR] {e}")
    
    return None

def main():
    print("--- Iniciando Fetcher de PDFs (Con Resume) ---")
    
    # 1. Cargar Datos
    if os.path.exists(OUTPUT_FILE):
        print("-> Cargando archivo de progreso existente...")
        data = load_json(OUTPUT_FILE)
    else:
        print("-> Cargando archivo limpio original...")
        data = load_json(INPUT_FILE)
        
    if not data:
        print("[ERROR] No hay datos de entrada.")
        return

    # 2. Cargar Estado (Códigos ya procesados)
    processed_codes = set()
    if os.path.exists(STATE_FILE):
        state = load_json(STATE_FILE)
        processed_codes = set(state.get("processed_codes", []))
        print(f"-> Reanudando sesión. {len(processed_codes)} asignaturas ya procesadas.")

    total_degrees = len(data.get("data", []))
    processed_count_session = 0
    
    try:
        for i, degree in enumerate(data.get("data", [])):
            print(f"\n[{i+1}/{total_degrees}] Grado: {degree['degree_name']}")
            
            subjects = degree.get("subjects", [])
            modified_degree = False
            
            for subject in subjects:
                code = subject.get("code")
                
                # CHECKPOINT: Si ya lo hicimos, saltar
                if code in processed_codes:
                    continue
                
                print(f"  Procesando: {subject['name']} ({code})...", end="", flush=True)
                
                # Acción
                pdf_url = get_pdf_url(subject.get("link"))
                
                if pdf_url:
                    subject["pdf_url"] = pdf_url
                    print(f" OK -> PDF encontrado.")
                else:
                    subject["pdf_url"] = None
                    print(f" FAIL -> No PDF.")
                
                # Actualizar estado
                processed_codes.add(code)
                modified_degree = True
                processed_count_session += 1
                
                # Anti-ban delay
                time.sleep(random.uniform(0.5, 1.5))
                
                # GUARDADO INCREMENTAL (Cada 10 asignaturas)
                if processed_count_session % 10 == 0:
                    save_json(OUTPUT_FILE, data)
                    save_json(STATE_FILE, {"processed_codes": list(processed_codes)})
                    print("  [SAVED] Progreso guardado.")

            # Guardar al terminar un grado completo también
            if modified_degree:
                save_json(OUTPUT_FILE, data)
                save_json(STATE_FILE, {"processed_codes": list(processed_codes)})

    except KeyboardInterrupt:
        print("\n\n[DETENIDO POR USUARIO] Guardando estado final...")
        save_json(OUTPUT_FILE, data)
        save_json(STATE_FILE, {"processed_codes": list(processed_codes)})
        print("Estado guardado de forma segura.")
        return

    print("\n--- Proceso Completado ---")
    # Limpieza del archivo de estado si termina todo
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print("Archivo de estado temporal eliminado.")

if __name__ == "__main__":
    main()
