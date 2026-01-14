import json
import requests
import pdfplumber
import io
import re
import os
import urllib3
import time

# Configuración
INPUT_FILE = "/sdcard/Download/ual_final_data.json"
OUTPUT_FILE = "/sdcard/Download/ual_final_data_enriched.json"
CURRENT_YEAR = "2025-26" # Ajustar según el año académico vigente

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_sections(text):
    """
    Intenta separar el texto del PDF en secciones lógicas usando heurística básica.
    """
    data = {
        "learning_objectives": [],
        "course_content_outline": [],
        "bibliography": {}
    }
    
    # Normalización
    text_lower = text.lower()
    
    # Heurística simple de segmentación (Puede requerir ajuste fino)
    # Buscamos índices de palabras clave
    idx_obj = text_lower.find("competencias y objetivos")
    if idx_obj == -1: idx_obj = text_lower.find("competencias")
    
    idx_tem = text_lower.find("temario")
    if idx_tem == -1: idx_tem = text_lower.find("contenidos")
    if idx_tem == -1: idx_tem = text_lower.find("bloque temático")
    
    idx_bib = text_lower.find("bibliografía")
    idx_eval = text_lower.find("evaluación")
    
    # Extracción de Temario (Prioridad)
    if idx_tem != -1:
        end_tem = idx_bib if idx_bib != -1 else idx_eval
        if end_tem == -1 or end_tem < idx_tem: end_tem = len(text)
        
        raw_content = text[idx_tem:end_tem].replace("Temario", "").replace("CONTENIDOS", "").strip()
        # Convertir líneas en lista
        data["course_content_outline"] = [line.strip() for line in raw_content.split('\n') if line.strip() and len(line) > 5]

    # Extracción de Objetivos
    if idx_obj != -1:
        end_obj = idx_tem if idx_tem != -1 else len(text)
        raw_obj = text[idx_obj:end_obj].strip()
        data["learning_objectives"] = [line.strip() for line in raw_obj.split('\n') if line.strip() and len(line) > 10]

    return data

def process_file():
    print("--- UAL PDF ENRICHER STARTING ---")
    
    if not os.path.exists(INPUT_FILE):
        print(f"CRITICAL: Input file {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        uni_data = json.load(f)

    total_processed = 0
    total_errors = 0
    
    branches = uni_data.get('branches', {})
    
    for b_name, degrees in branches.items():
        print(f"Processing Branch: {b_name}")
        for degree in degrees:
            print(f"  Degree: {degree['name']}")
            
            for subject in degree.get('subjects', []):
                subj_code = subject.get('code')
                
                # Construir URL PDF
                pdf_url = f"https://www.ual.es/guia_academica/{subj_code}/{CURRENT_YEAR}/CAS"
                
                print(f"    -> Enriqueciendo: {subject['name']} ({subj_code})...")
                
                try:
                    resp = requests.get(pdf_url, headers=HEADERS, verify=False, timeout=10)
                    
                    if resp.status_code == 200 and 'application/pdf' in resp.headers.get('Content-Type', ''):
                        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
                            full_text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    full_text += page_text + "\n"
                            
                            # Extraer datos
                            extracted = extract_sections(full_text)
                            
                            # Actualizar sujeto
                            subject['learning_objectives'] = extracted['learning_objectives']
                            subject['course_content_outline'] = extracted['course_content_outline']
                            subject['bibliography'] = extracted['bibliography'] # Placeholder
                            subject['guide_url'] = pdf_url
                            
                            total_processed += 1
                    else:
                        print(f"       [!] PDF no encontrado o error (Status: {resp.status_code})")
                        total_errors += 1
                        
                except Exception as e:
                    print(f"       [x] Error procesando PDF: {e}")
                    total_errors += 1
                
                # Guardado incremental por seguridad cada 10 asignaturas
                if total_processed % 10 == 0:
                     with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
                        json.dump(uni_data, f_out, ensure_ascii=False, indent=2)
                     print("       (Checkpoint Saved)")

    # Guardado final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        json.dump(uni_data, f_out, ensure_ascii=False, indent=2)
        
    print(f"\n--- PROCESS COMPLETED ---")
    print(f"Processed: {total_processed}")
    print(f"Errors: {total_errors}")
    print(f"Enriched data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_file()
