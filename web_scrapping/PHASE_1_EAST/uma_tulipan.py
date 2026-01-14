import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import json
import time
import io
import re
import os
import sys

# --- CONFIGURACIÓN PARA ANDROID ---
OUTPUT_FILE = '/sdcard/Download/uma_tulipan_data.json'
LOG_FILE = '/sdcard/Download/uma_tulipan_log.txt'
BASE_URL = "https://sara.uma.es/pls/apex/"
PDF_BASE = "https://sara.uma.es"

# Headers simulando navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}

try:
    import pdfplumber
except ImportError:
    print("[FATAL] 'pdfplumber' no instalado. Ejecuta: pip install pdfplumber")
    sys.exit(1)

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    print(formatted_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(formatted_msg + "\n")

def save_incremental(data_list):
    """Guarda el JSON completo cada vez (enfoque seguro para volumen medio)."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

def clean_text_list(raw_text):
    if not raw_text: return []
    # Umbral bajado a 3 chars para no borrar autores o siglas
    lines = [l.strip() for l in raw_text.split('\n') if len(l.strip()) > 3]
    cleaned = []
    for l in lines:
        if re.match(r'^\d+$', l): continue # Eliminar números de página sueltos
        if "guía docente" in l.lower(): continue
        # Eliminar bullets numéricos o símbolos
        item = re.sub(r'^\s*(\d+[\.\)]|[-•·])\s*', '', l).strip()
        if item: cleaned.append(item)
    return cleaned

def process_pdf_content(raw_text):
    if not raw_text: return {}
    t = raw_text.lower()
    
    # Patrones de sección ampliados
    patterns = {
        'objectives': r'(?:1\.|1\s)\s*(?:objetivos|competencias|resultados de aprendizaje)|(?:objetivos|competencias)',
        'content': r'(?:contenidos|temario|programa de la asignatura|bloques temáticos)',
        'bibliography': r'(?:bibliografía|referencias|fuentes de información)',
        # Stop words para cortar la lectura si llegamos a evaluación
        'stop': r'(?:evaluación|sistema de evaluación|metodología docente)'
    }
    
    indices = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, t)
        indices[key] = match.start() if match else -1
    
    # Ordenar secciones encontradas por posición
    found_sections = sorted([(k, v) for k, v in indices.items() if v != -1 and k != 'stop'], key=lambda x: x[1])
    
    extracted = {
        'learning_objectives': [],
        'course_content_outline': [],
        'bibliography': {"references": []}
    }
    
    stop_idx = indices['stop'] if indices['stop'] != -1 else len(t)
    
    for i, (section_name, start_idx) in enumerate(found_sections):
        # El final es el inicio de la siguiente sección encontrada, o el stop_idx, o el fin del archivo
        next_start = stop_idx
        
        # Buscar la siguiente sección válida que esté después de la actual
        for _, next_s_idx in found_sections[i+1:]:
             if next_s_idx > start_idx:
                 next_start = next_s_idx
                 break
        
        # Si el stop está antes de la siguiente sección (raro pero posible), usar stop
        if stop_idx > start_idx and stop_idx < next_start:
            next_start = stop_idx
            
        fragment = raw_text[start_idx:next_start]
        
        # Limpieza básica del título de la sección
        lines = fragment.split('\n')
        if len(lines) > 0:
            # Asumimos que la primera línea es el título y la descartamos si es corta
            if len(lines[0]) < 50:
                fragment = "\n".join(lines[1:])
        
        cleaned_list = clean_text_list(fragment)
        
        if section_name == 'objectives':
            extracted['learning_objectives'] = cleaned_list
        elif section_name == 'content':
            extracted['course_content_outline'] = cleaned_list
        elif section_name == 'bibliography':
            extracted['bibliography'] = {"references": cleaned_list}
            
    return extracted

def extract_pdf_data(session, pdf_url):
    try:
        r = session.get(pdf_url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        with pdfplumber.open(io.BytesIO(r.content)) as pdf:
            full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            return process_pdf_content(full_text)
    except Exception as e:
        log(f"Error PDF {pdf_url}: {e}")
        return None

def get_subjects_from_table(session, center_id, degree_id, year, center_name, degree_name):
    # URL Base del listado
    url = (
        f"{BASE_URL}f?p=101:1:::::"
        f"INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,"
        f"INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES,"
        f"INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:"
        f"3,2025,{center_id},{degree_id},1,{year}"
    )
    
    subjects_found = []
    try:
        r = session.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # SELECCIÓN QUIRÚRGICA: Solo tablas de reporte
        report_table = soup.find("table", class_="t-Report-report")
        
        if not report_table:
            # A veces no hay tabla si no hay asignaturas
            return []
            
        # Iterar filas (saltando header)
        rows = report_table.find_all("tr")
        for row in rows:
            # Buscar celdas
            cells = row.find_all("td")
            if not cells: continue 
            
            # Buscar enlace en alguna celda (normalmente la 2ª o 3ª es el nombre)
            link = row.find("a", href=True)
            if not link: continue
            
            href = link['href']
            # Validar que es un enlace de detalle APEX (página 3)
            if "f?p=101:3" not in href: continue
            
            subject_name = link.get_text(strip=True)
            detail_url = urljoin(BASE_URL, href)
            
            subjects_found.append({
                "name": subject_name,
                "url": detail_url,
                "center": center_name,
                "degree": degree_name,
                "year": year
            })
            
    except Exception as e:
        log(f"Error obteniendo listado asignaturas: {e}")
        
    return subjects_found

def process_subject_detail(session, subject_data):
    try:
        r = session.get(subject_data['url'], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Buscar enlace PDF "Consultar la guía docente"
        # Usamos una regex flexible para el texto
        pdf_link_tag = soup.find("a", string=re.compile(r"gu[ií]a docente", re.IGNORECASE))
        
        if pdf_link_tag and 'href' in pdf_link_tag.attrs:
            pdf_url = urljoin(PDF_BASE, pdf_link_tag['href'])
            subject_data['pdf_url'] = pdf_url
            
            log(f"   -> Procesando PDF: {subject_data['name']}")
            pdf_data = extract_pdf_data(session, pdf_url)
            
            if pdf_data:
                subject_data.update(pdf_data)
                subject_data['status'] = 'COMPLETE'
            else:
                subject_data['status'] = 'PDF_ERROR'
        else:
            subject_data['status'] = 'NO_PDF'
            log(f"   -> Sin PDF: {subject_data['name']}")
            
    except Exception as e:
        subject_data['status'] = 'DETAIL_ERROR'
        log(f"Error detalle {subject_data['name']}: {e}")
        
    return subject_data

def get_options(session, url_or_soup, select_id=None, ajax_params=None):
    """Helper para extraer opciones de selects o respuestas AJAX."""
    options = {}
    try:
        if ajax_params:
            # Lógica AJAX para Titulaciones (si aplica)
            url = (f"{BASE_URL}wwv_flow.show?p_flow_id=101&p_flow_step_id=1"
                   f"&p_instance=0&request=PLUGIN=apex.widget.selectlist"
                   f"&x01={ajax_params['x01']}&x02={ajax_params['x02']}")
            r = session.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("option")
        elif select_id:
            # Lógica HTML estático
            if isinstance(url_or_soup, str):
                r = session.get(url_or_soup, headers=HEADERS, timeout=15)
                soup = BeautifulSoup(r.text, "html.parser")
            else:
                soup = url_or_soup
            select = soup.find("select", {"id": select_id}) or soup.find("select", {"name": select_id})
            items = select.find_all("option") if select else []
        
        for o in items:
            val = o.get("value")
            txt = o.get_text(strip=True)
            if val and val.isdigit() and val != "-1":
                options[val] = txt
                
    except Exception as e:
        log(f"Error obteniendo opciones: {e}")
        
    return options

def main():
    log("=== INICIANDO TULIPÁN SCRAPER ===")
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # Cargar datos existentes si hay reanudación
    all_data = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
            log(f"Cargados {len(all_data)} registros previos.")
        except: pass
    
    # Evitar re-procesar (set de URLs procesadas)
    processed_urls = {d['url_source'] for d in all_data if 'url_source' in d}
    
    # 1. Obtener Centros
    log("Obteniendo Centros...")
    centros = get_options(session, f"{BASE_URL}f?p=101:1", select_id="INICIO_LOV_CENTROS")
    log(f"Centros encontrados: {len(centros)}")
    
    for c_id, c_name in centros.items():
        log(f"CENTRO [{c_id}]: {c_name}")
        
        # 2. Obtener Titulaciones (AJAX)
        grados = get_options(session, None, ajax_params={'x01': 'INICIO_LOV_TITULACIONES', 'x02': c_id})
        
        for d_id, d_name in grados.items():
            # Filtro opcional: Solo procesar grados, no masters si se desea (Tipo 3 es Grado)
            # El script original filtraba por INICIO_LOV_TIPO_ESTUDIO: 3 en la URL de búsqueda, así que está implícito.
            
            log(f"  GRADO [{d_id}]: {d_name}")
            
            for year in range(1, 5): # Cursos 1 a 4
                log(f"    Curso {year}...")
                
                # 3. Obtener Asignaturas (Lista)
                subjects = get_subjects_from_table(session, c_id, d_id, year, c_name, d_name)
                log(f"      Encontradas: {len(subjects)}")
                
                for subj in subjects:
                    if subj['url'] in processed_urls:
                        continue
                        
                    # 4. Procesar Detalle y PDF
                    final_data = process_subject_detail(session, subj)
                    final_data['url_source'] = subj['url'] # Asegurar key para unicidad
                    
                    all_data.append(final_data)
                    save_incremental(all_data)
                    processed_urls.add(subj['url'])
                    
                    time.sleep(1) # Cortesía
                    
    log("=== FINALIZADO ===")

if __name__ == "__main__":
    main()
