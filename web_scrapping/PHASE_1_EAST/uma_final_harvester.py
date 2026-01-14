import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import sys
import io
import os
import re

# Dependencia crítica
try:
    import pdfplumber
except ImportError:
    print("[FATAL] 'pdfplumber' no instalado. Ejecuta: pip install pdfplumber")
    sys.exit(1)

# --- CONFIGURACIÓN ---
INPUT_FILE = '/sdcard/Download/uma_full_data_clean.json'
OUTPUT_FILE = '/sdcard/Download/uma_ready_to_deploy.json'
BATCH_SIZE = 10
DELAY = 1.0

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def get_pdf_direct_link(html_url):
    try:
        r = requests.get(html_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True).lower()
            if 'guía docente' in text or 'guia docente' in text or '.pdf' in href.lower():
                return urljoin(html_url, href)
    except Exception:
        pass
    return None

def extract_text_from_pdf(pdf_url):
    try:
        r = requests.get(pdf_url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        with pdfplumber.open(io.BytesIO(r.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            return full_text
    except Exception:
        return None

def clean_list_item(text):
    """Limpia un elemento de lista (quita guiones, números iniciales, espacios extra)."""
    # Quitar números al inicio (ej: "1. Introducción" -> "Introducción")
    text = re.sub(r'^\s*\d+[\.\)]\s*', '', text)
    # Quitar guiones/puntos al inicio
    text = re.sub(r'^\s*[-•·]\s*', '', text)
    return text.strip()

def text_to_list(raw_text):
    """Convierte un bloque de texto en una lista de strings limpia."""
    if not raw_text or len(raw_text) < 5:
        return []
    
    lines = raw_text.split('\n')
    cleaned_list = []
    
    for line in lines:
        line = line.strip()
        # Filtros de ruido: líneas muy cortas, números de página, headers repetidos
        if len(line) < 4: continue
        if re.match(r'^\d+$', line): continue # Número de página aislado
        if "guía docente" in line.lower(): continue
        
        cleaned_item = clean_list_item(line)
        if cleaned_item:
            cleaned_list.append(cleaned_item)
            
    return cleaned_list

def process_raw_content(raw_text):
    """Segmenta el texto y lo convierte a estructuras de datos (Listas/Dicts)."""
    if not raw_text:
        return None

    text_lower = raw_text.lower()
    
    # Patrones de corte más robustos
    patterns = {
        'objectives': r'(?:objetivos|competencias|resultados de aprendizaje)',
        'content': r'(?:contenidos|temario|programa de la asignatura|bloques temáticos)',
        'bibliography': r'(?:bibliografía|referencias|fuentes de información)',
        'evaluation': r'(?:evaluación|sistema de evaluación)' # Stop word para la bibliografía
    }
    
    indices = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        indices[key] = match.start() if match else -1
            
    # Ordenar secciones encontradas
    found_sections = sorted([(k, v) for k, v in indices.items() if v != -1], key=lambda item: item[1])
    
    extracted_data = {
        'learning_objectives': [], # DB expects List
        'course_content_outline': [], # DB expects List
        'bibliography': {"references": []} # DB expects Dict
    }
    
    for i, (section_name, start_idx) in enumerate(found_sections):
        if i < len(found_sections) - 1:
            end_idx = found_sections[i+1][1]
        else:
            end_idx = len(raw_text)
            
        raw_fragment = raw_text[start_idx:end_idx]
        
        # Eliminar la primera línea (el título de la sección)
        parts = raw_fragment.split('\n', 1)
        content_fragment = parts[1] if len(parts) > 1 else ""
        
        # PROCESAMIENTO SEGÚN TIPO
        if section_name == 'objectives':
            extracted_data['learning_objectives'] = text_to_list(content_fragment)
        
        elif section_name == 'content':
            extracted_data['course_content_outline'] = text_to_list(content_fragment)
            
        elif section_name == 'bibliography':
            refs = text_to_list(content_fragment)
            extracted_data['bibliography'] = {"references": refs}
            
    return extracted_data

def main():
    print("===========================================")
    print("   UMA HARVESTER V2 (READY-TO-DEPLOY)   ")
    print("===========================================")
    
    if not os.path.exists(INPUT_FILE):
        print(f"[FATAL] No input file: {INPUT_FILE}")
        return
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        subjects = json.load(f)
        
    # Reanudación
    processed_data = []
    start_index = 0
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                processed_data = json.load(f)
                start_index = len(processed_data)
                print(f"--> Reanudando desde {start_index}...")
        except: pass
    
    for i in range(start_index, len(subjects)):
        subject = subjects[i]
        print(f"[{i+1}/{len(subjects)}] {subject['name']}...", end='', flush=True)
        
        pdf_url = get_pdf_direct_link(subject['url_source'])
        
        if pdf_url:
            raw_text = extract_text_from_pdf(pdf_url)
            if raw_text:
                structured_data = process_raw_content(raw_text)
                if structured_data:
                    subject.update(structured_data)
                    subject['pdf_url'] = pdf_url # Guardamos url del pdf por referencia
                    subject['extraction_status'] = 'READY'
                    
                    # Debug visual rápido
                    n_obj = len(subject['learning_objectives'])
                    n_tem = len(subject['course_content_outline'])
                    print(f" [OK] (Obj:{n_obj}, Tem:{n_tem})")
                else:
                    subject['extraction_status'] = 'PARSE_ERROR'
                    print(" [PARSE ERROR]")
            else:
                subject['extraction_status'] = 'PDF_READ_ERROR'
                print(" [PDF ERROR]")
        else:
            subject['extraction_status'] = 'NO_PDF'
            print(" [NO PDF]")
            
        processed_data.append(subject)
        
        if (i + 1) % BATCH_SIZE == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)
        
        time.sleep(DELAY)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    print("DONE.")

if __name__ == "__main__":
    main()
