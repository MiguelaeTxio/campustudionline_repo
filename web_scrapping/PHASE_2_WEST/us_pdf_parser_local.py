# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/PHASE_2_WEST/us_pdf_parser_local.py
import requests
from bs4 import BeautifulSoup
import pdfplumber
import json
import os
import time
import random

# --- CONFIGURACIÓN ---
INPUT_FILE = "/sdcard/Download/us_clean_subjects.json"
OUTPUT_FILE = "/sdcard/Download/us_final_data_enriched.json"
STATE_FILE = "/sdcard/Download/us_parser_state.json"
TEMP_PDF = "/sdcard/Download/temp_subject.pdf"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def load_json(path, default):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def extract_content_from_pdf(pdf_path):
    objectives = []
    outline = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # Lógica de segmentación simple por palabras clave
            lines = full_text.split('\n')
            current_section = None
            
            for line in lines:
                l_lower = line.lower().strip()
                
                # Detectar Secciones
                if any(x in l_lower for x in ["objetivos", "competencias"]):
                    current_section = "OBJ"
                    continue
                elif any(x in l_lower for x in ["temario", "contenidos", "programa sintético", "bloque"]):
                    current_section = "OUT"
                    continue
                elif len(l_lower) > 50 and l_lower.isupper(): # Posible nueva sección
                    current_section = None

                # Capturar contenido
                clean_line = line.strip()
                if clean_line and len(clean_line) > 3:
                    if current_section == "OBJ":
                        objectives.append(clean_line)
                    elif current_section == "OUT":
                        outline.append(clean_line)
                        
    except Exception as e:
        print(f"      [ERROR PDF] {e}")
        
    return objectives[:20], outline[:40] # Limitar para evitar ruido excesivo

def get_data_from_us(subject):
    # 1. Obtener enlace SEVIUS desde la ficha de US
    try:
        res = requests.get(subject['link'], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        sevius_link = soup.find('a', href=lambda h: h and "sevius4.us.es" in h)
        if not sevius_link: return None, None
        
        # 2. Obtener el ID del programa desde SEVIUS (GET)
        sevius_url = sevius_link['href']
        res_sevius = requests.get(sevius_url, headers=HEADERS, timeout=15)
        soup_sevius = BeautifulSoup(res_sevius.text, 'html.parser')
        
        # El primer input con name="programa" suele ser el más reciente
        prog_input = soup_sevius.find('input', {'name': 'programa'})
        if not prog_input: return None, None
        
        prog_id = prog_input['value']
        
        # 3. Descargar PDF (POST)
        # La URL de acción del form es la misma o index.php?PyP=LISTA
        download_url = "https://sevius4.us.es/index.php?PyP=LISTA"
        payload = {'programa': prog_id}
        
        res_pdf = requests.post(download_url, data=payload, headers=HEADERS, timeout=20)
        
        if res_pdf.status_code == 200 and b'%PDF' in res_pdf.content[:100]:
            with open(TEMP_PDF, 'wb') as f:
                f.write(res_pdf.content)
            
            obj, out = extract_content_from_pdf(TEMP_PDF)
            
            if os.path.exists(TEMP_PDF):
                os.remove(TEMP_PDF)
                
            return obj, out
            
    except Exception as e:
        print(f"      [ERROR PETICIÓN] {e}")
        
    return None, None

def main():
    print("--- Harvester de Contenidos: Institución Académica de Sevilla ---")
    
    raw_data = load_json(INPUT_FILE, None)
    if not raw_data:
        print("[FATAL] No se pudo cargar el archivo de entrada.")
        return

    # Preparar contenedor final
    enriched_data = load_json(OUTPUT_FILE, {
        "university": "Institución Académica de Sevilla",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": []
    })

    # Cargar estado para reanudación
    state = load_json(STATE_FILE, {"processed_codes": []})
    processed_codes = set(state["processed_codes"])

    total_degrees = len(raw_data["data"])
    
    try:
        for d_idx, degree in enumerate(raw_data["data"]):
            print(f"\n[{d_idx+1}/{total_degrees}] Grado: {degree['degree_name']}")
            
            # Buscar si el grado ya existe en el enriquecido o crearlo
            current_degree = next((d for d in enriched_data["data"] if d["degree_name"] == degree["degree_name"]), None)
            if not current_degree:
                current_degree = {
                    "degree_name": degree["degree_name"],
                    "degree_url": degree["degree_url"],
                    "subjects": []
                }
                enriched_data["data"].append(current_degree)

            for subject in degree["subjects"]:
                code = subject["code"]
                
                if code in processed_codes:
                    continue
                
                print(f"  -> Asignatura: {subject['name']} ({code})... ", end="", flush=True)
                
                obj, out = get_data_from_us(subject)
                
                subject['learning_objectives'] = obj if obj else []
                subject['course_content_outline'] = out if out else []
                
                # Añadir a la lista del grado (evitando duplicados si se reanudó)
                if not any(s['code'] == code for s in current_degree["subjects"]):
                    current_degree["subjects"].append(subject)

                processed_codes.add(code)
                print("OK" if obj else "SIN CONTENIDO")

                # Guardado incremental y descanso
                if len(processed_codes) % 5 == 0:
                    state["processed_codes"] = list(processed_codes)
                    save_json(OUTPUT_FILE, enriched_data)
                    save_json(STATE_FILE, state)
                
                time.sleep(random.uniform(1.2, 3.0))

    except KeyboardInterrupt:
        print("\n[PAUSA] Guardando progreso...")
    finally:
        state["processed_codes"] = list(processed_codes)
        save_json(OUTPUT_FILE, enriched_data)
        save_json(STATE_FILE, state)
        print(f"--- Proceso finalizado/pausado. Revisar: {OUTPUT_FILE} ---")

if __name__ == "__main__":
    main()
