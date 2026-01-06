import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import sys
import io
import os
import re

# Intentar importar pdfplumber (Crítico)
try:
    import pdfplumber
except ImportError:
    print("[FATAL] 'pdfplumber' no instalado. Ejecuta: pip install pdfplumber")
    sys.exit(1)

# --- CONFIGURACIÓN ---
INPUT_FILE = '/sdcard/Download/uma_full_data_clean.json'
OUTPUT_FILE = '/sdcard/Download/uma_final_enriched.json'
BATCH_SIZE = 10 # Guardar cada X asignaturas
DELAY = 1.5 # Segundos entre peticiones

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def get_pdf_direct_link(html_url):
    """Entra en la ficha HTML y busca el botón de descarga del PDF."""
    try:
        r = requests.get(html_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Buscar enlaces que contengan 'guía docente' o apunten a un PDF
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True).lower()
            
            # Patrón detectado en tu captura: "Consultar la guía docente..."
            if 'guía docente' in text or 'guia docente' in text or '.pdf' in href.lower():
                return urljoin(html_url, href)
                
    except Exception as e:
        print(f"   [WARN] Error resolviendo PDF link: {e}")
    return None

def extract_text_with_pdfplumber(pdf_url):
    """Descarga el PDF en memoria y extrae el texto usando pdfplumber."""
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
            
    except Exception as e:
        print(f"   [WARN] Error descargando/leyendo PDF: {e}")
        return None

def segment_content(text):
    """
    Intenta dividir el texto bruto en secciones lógicas.
    Es una heurística básica basada en palabras clave comunes.
    """
    if not text:
        return {}, {}, {}

    text_lower = text.lower()
    
    # Definir anclas de inicio (Regex para flexibilidad)
    # Buscamos encabezados como "1. Objetivos", "Competencias", "Temario", etc.
    patterns = {
        'objectives': r'(objetivos|competencias|resultados de aprendizaje)',
        'content': r'(contenidos|temario|programa de la asignatura|bloques temáticos)',
        'bibliography': r'(bibliografía|referencias|fuentes de información)'
    }
    
    indices = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            indices[key] = match.start()
        else:
            indices[key] = -1
            
    # Ordenar las secciones encontradas por su posición en el texto
    found_sections = sorted([(k, v) for k, v in indices.items() if v != -1], key=lambda item: item[1])
    
    extracted = {
        'learning_objectives': "Contenido no extraíble automáticamente.",
        'course_content_outline': "Contenido no extraíble automáticamente.",
        'bibliography': "Contenido no extraíble automáticamente."
    }
    
    for i, (section_name, start_idx) in enumerate(found_sections):
        # El final de esta sección es el inicio de la siguiente, o el final del documento
        if i < len(found_sections) - 1:
            end_idx = found_sections[i+1][1]
        else:
            end_idx = len(text)
            
        # Extraer y limpiar
        raw_fragment = text[start_idx:end_idx]
        # Quitar el título de la sección (aprox)
        lines = raw_fragment.split('\n')
        if len(lines) > 1:
            clean_fragment = '\n'.join(lines[1:]).strip()
        else:
            clean_fragment = raw_fragment
            
        # Mapear nombres internos
        if section_name == 'objectives':
            extracted['learning_objectives'] = clean_fragment
        elif section_name == 'content':
            extracted['course_content_outline'] = clean_fragment
        elif section_name == 'bibliography':
            extracted['bibliography'] = clean_fragment
            
    return extracted

def main():
    print("===========================================")
    print("   UMA CONTENT HARVESTER (PDFPLUMBER)   ")
    print("===========================================")
    
    # 1. Cargar datos previos
    if not os.path.exists(INPUT_FILE):
        print(f"[FATAL] No se encuentra el archivo de entrada: {INPUT_FILE}")
        return
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        subjects = json.load(f)
        
    print(f"Cargadas {len(subjects)} asignaturas para procesar.")
    
    # 2. Gestión de reanudación (Comprobar si ya existe el output parcial)
    processed_data = []
    start_index = 0
    
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                processed_data = json.load(f)
                start_index = len(processed_data)
                print(f"--> Reanudando desde el índice {start_index}...")
        except json.JSONDecodeError:
            print("--> Archivo de salida corrupto o vacío. Empezando de cero.")
    
    # 3. Bucle de procesamiento
    for i in range(start_index, len(subjects)):
        subject = subjects[i]
        print(f"[{i+1}/{len(subjects)}] {subject['name']}...", end='', flush=True)
        
        # A. Obtener link PDF
        pdf_url = get_pdf_direct_link(subject['url_source'])
        
        if pdf_url:
            subject['pdf_url'] = pdf_url
            # B. Extraer texto
            raw_text = extract_text_with_pdfplumber(pdf_url)
            
            if raw_text:
                # C. Segmentar
                sections = segment_content(raw_text)
                subject.update(sections)
                subject['extraction_status'] = 'SUCCESS'
                print(" [OK]")
            else:
                subject['extraction_status'] = 'PDF_READ_ERROR'
                print(" [PDF ERROR]")
        else:
            subject['extraction_status'] = 'NO_PDF_LINK'
            print(" [NO PDF]")
            
        processed_data.append(subject)
        
        # D. Guardado por lotes
        if (i + 1) % BATCH_SIZE == 0:
            print(f"   [SAVING BATCH] Guardando progreso ({len(processed_data)} registros)...")
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)
                
        # E. Delay
        time.sleep(DELAY)

    # Guardado final
    print("\nProceso finalizado. Guardando archivo completo...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    print("DONE.")

if __name__ == "__main__":
    main()
