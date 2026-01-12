import json
import requests
import pdfplumber
import io
import re
import os
import urllib3
import time

# --- CONFIGURACIÓN ---
INPUT_FILE = "/sdcard/Download/ual_final_data.json"
OUTPUT_FILE = "/sdcard/Download/ual_final_data_enriched.json"
CURRENT_YEAR = "2025-26" 
MAX_RETRIES = 3
RETRY_DELAY = 5 # Segundos

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_sections(text):
    """Segmentación heurística del contenido."""
    data = {
        "learning_objectives": [],
        "course_content_outline": [],
        "bibliography": {}
    }
    text_lower = text.lower()
    
    idx_obj = text_lower.find("competencias y objetivos")
    if idx_obj == -1: idx_obj = text_lower.find("competencias")
    
    idx_tem = text_lower.find("temario")
    if idx_tem == -1: idx_tem = text_lower.find("contenidos")
    if idx_tem == -1: idx_tem = text_lower.find("bloque temático")
    
    idx_bib = text_lower.find("bibliografía")
    idx_eval = text_lower.find("evaluación")
    
    if idx_tem != -1:
        end_tem = idx_bib if idx_bib != -1 else idx_eval
        if end_tem == -1 or end_tem < idx_tem: end_tem = len(text)
        raw_content = text[idx_tem:end_tem].replace("Temario", "").replace("CONTENIDOS", "").strip()
        data["course_content_outline"] = [line.strip() for line in raw_content.split('\n') if line.strip() and len(line) > 5]

    if idx_obj != -1:
        end_obj = idx_tem if idx_tem != -1 else len(text)
        raw_obj = text[idx_obj:end_obj].strip()
        data["learning_objectives"] = [line.strip() for line in raw_obj.split('\n') if line.strip() and len(line) > 10]

    return data

def process_resumable():
    print("--- UAL PDF ENRICHER V2 (RESUMABLE) STARTING ---")
    
    # 1. Lógica de Reanudación
    if os.path.exists(OUTPUT_FILE):
        print(f"[i] Archivo de progreso encontrado: {OUTPUT_FILE}")
        print("    -> Cargando para reanudar...")
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                uni_data = json.load(f)
        except json.JSONDecodeError:
            print("    [!] Error: Archivo de progreso corrupto. Iniciando desde cero.")
            with open(INPUT_FILE, 'r', encoding='utf-8') as f:
                uni_data = json.load(f)
    else:
        print(f"[i] Iniciando desde cero con: {INPUT_FILE}")
        if not os.path.exists(INPUT_FILE):
            print("    [!] CRITICAL: No existe archivo de entrada.")
            return
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            uni_data = json.load(f)

    total_processed = 0
    total_skipped = 0
    total_errors = 0
    save_counter = 0
    
    branches = uni_data.get('branches', {})
    
    for b_name, degrees in branches.items():
        # print(f"Processing Branch: {b_name}") # Demasiado ruido
        for degree in degrees:
            # print(f"  Degree: {degree['name']}")
            
            for subject in degree.get('subjects', []):
                
                # Checkpoint de reanudación: Si ya tiene URL de guía, asumimos procesado
                if subject.get('guide_url'):
                    total_skipped += 1
                    continue

                subj_code = subject.get('code')
                pdf_url = f"https://www.ual.es/guia_academica/{subj_code}/{CURRENT_YEAR}/CAS"
                
                print(f"    -> ({total_processed + total_skipped + 1}) Procesando: {subject['name']}...")
                
                # Bucle de reintentos
                success = False
                for attempt in range(MAX_RETRIES):
                    try:
                        resp = requests.get(pdf_url, headers=HEADERS, verify=False, timeout=15)
                        
                        if resp.status_code == 200 and 'application/pdf' in resp.headers.get('Content-Type', ''):
                            with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
                                full_text = ""
                                for page in pdf.pages:
                                    extract = page.extract_text()
                                    if extract: full_text += extract + "\n"
                                
                                extracted = extract_sections(full_text)
                                
                                subject['learning_objectives'] = extracted['learning_objectives']
                                subject['course_content_outline'] = extracted['course_content_outline']
                                subject['bibliography'] = extracted['bibliography']
                                subject['guide_url'] = pdf_url # Flag de completado
                                
                                total_processed += 1
                                success = True
                                break # Salir del bucle de intentos
                        else:
                            print(f"       [!] PDF no disponible (HTTP {resp.status_code}). Saltando.")
                            subject['guide_url'] = "NOT_FOUND" # Marcamos para no reintentar eternamente
                            total_errors += 1
                            success = True # Tratamos como 'procesado' (aunque fallido) para avanzar
                            break
                            
                    except Exception as e:
                        print(f"       [x] Error red (Intento {attempt+1}/{MAX_RETRIES}): {e}")
                        time.sleep(RETRY_DELAY) # Esperar antes de reintentar
                
                if not success:
                    print("       [x] FALLO DEFINITIVO. Pasando al siguiente.")
                    total_errors += 1

                # Guardado incremental
                save_counter += 1
                if save_counter >= 10:
                     with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
                        json.dump(uni_data, f_out, ensure_ascii=False, indent=2)
                     print("       [S] Progreso guardado.")
                     save_counter = 0

    # Guardado final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        json.dump(uni_data, f_out, ensure_ascii=False, indent=2)
        
    print(f"\n--- PROCESS COMPLETED ---")
    print(f"Procesados nuevos: {total_processed}")
    print(f"Saltados (ya hechos): {total_skipped}")
    print(f"Errores: {total_errors}")

if __name__ == "__main__":
    process_resumable()
