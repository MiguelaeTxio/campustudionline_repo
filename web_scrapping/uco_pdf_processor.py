import json
import requests
import io
import re
import time
import os
import pdfplumber

# --- CONFIGURACIÓN ---
INPUT_FILE = 'uco_master_map.json'
OUTPUT_FILE = 'uco_final_data.json'
SAVE_INTERVAL = 5

def clean_text(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_section(full_text, headers, next_headers_pool):
    text_lower = full_text.lower()
    start_idx = -1
    
    for h in headers:
        idx = text_lower.find(h.lower())
        if idx != -1:
            start_idx = idx + len(h)
            break
            
    if start_idx == -1:
        return ""
        
    end_idx = len(full_text)
    for next_h in next_headers_pool:
        idx = text_lower.find(next_h.lower(), start_idx)
        if idx != -1 and idx < end_idx:
            end_idx = idx
            
    raw_section = full_text[start_idx:end_idx]
    if len(raw_section) < 5:
        return ""
    return clean_text(raw_section)

def process_pdf_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Android 10; Mobile; rv:109.0)'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    full_text += extracted + "\n"
                
        # Heurística de Secciones
        objectives = extract_section(
            full_text, 
            ['OBJETIVOS', 'COMPETENCIAS', 'RESULTADOS DE APRENDIZAJE', 'BREVE DESCRIPCIÓN DE CONTENIDOS'], 
            ['TEMARIO', 'CONTENIDOS', 'BIBLIOGRAFÍA', 'METODOLOGÍA', 'EVALUACIÓN', 'PROGRAMA']
        )
        
        outline = extract_section(
            full_text,
            ['TEMARIO', 'CONTENIDOS', 'PROGRAMA', 'DESCRIPCIÓN DE CONTENIDOS', 'PROGRAMA DE LA ASIGNATURA'],
            ['BIBLIOGRAFÍA', 'METODOLOGÍA', 'ACTIVIDADES', 'EVALUACIÓN', 'SYSTEM OF EVALUATION']
        )
        
        bibliography = extract_section(
            full_text,
            ['BIBLIOGRAFÍA', 'REFERENCIAS', 'BIBLIOGRAPHY'],
            ['EVALUACIÓN', 'METODOLOGÍA', 'COORDINACIÓN', 'ANEXO', 'CRITERIOS']
        )
        
        return {
            'full_text_length': len(full_text),
            'learning_objectives': objectives,
            'course_content_outline': outline,
            'bibliography': bibliography,
            'parse_success': True
        }

    except Exception as e:
        return {'parse_success': False, 'error': str(e)}

def main():
    print("=== UCO PDF PROCESSOR (Engine: pdfplumber) ===")
    
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: No se encuentra {INPUT_FILE}")
        return

    processed_ids = set()
    processed_data = []
    
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                processed_data = json.load(f)
                for item in processed_data:
                    uid = f"{item.get('url_source')}|{item.get('name')}"
                    processed_ids.add(uid)
            print(f"--> Reanudando: {len(processed_data)} registros previos.")
        except:
            pass

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    total = len(source_data)
    count = 0
    newly_processed = 0
    
    print(f"--> Total a procesar: {total}")

    for item in source_data:
        count += 1
        uid = f"{item.get('url_source')}|{item.get('name')}"
        
        if uid in processed_ids:
            continue
            
        pdf_url = item.get('pdf_url')
        # Print compacto para móvil
        print(f"[{count}/{total}] {item.get('name')[:30]}...", end=" ", flush=True)
        
        if pdf_url:
            pdf_data = process_pdf_url(pdf_url)
            item.update(pdf_data)
            
            if pdf_data.get('parse_success'):
                txt_len = pdf_data.get('full_text_length', 0)
                print(f"OK ({txt_len})")
            else:
                print("FAIL")
        else:
            print("SKIP (No URL)")
            item['parse_success'] = False

        processed_data.append(item)
        newly_processed += 1
        
        if newly_processed % SAVE_INTERVAL == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    
    print(f"\nCOMPLETADO. Datos en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
