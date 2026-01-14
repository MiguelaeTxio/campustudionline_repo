import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin, parse_qs, urlparse
import json
import io
import re
import sys
import time
import os

# --- CONFIGURACIÓN ---
BASE_URL = "https://sara.uma.es/pls/apex/f?p=101:1"
PDF_BASE = "https://sara.uma.es"
OUTPUT_FILE = '/sdcard/Download/uma_math_data.json'
CURRENT_YEAR = "2025" 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Connection': 'keep-alive'
}

try:
    import pdfplumber
except ImportError:
    pass

def log(msg):
    print(msg)

def get_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    # Reintentos para estabilidad
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def safe_get(session, url):
    try:
        return session.get(url, timeout=30)
    except Exception as e:
        log(f"   [RED] Error: {e}")
        time.sleep(5)
        return None

def save_incremental(data):
    current = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                current = json.load(f)
        except: pass
    
    # Evitar duplicados (Aunque la lógica matemática ya los evita per se)
    existing_urls = {item['url_source'] for item in current}
    if data['url_source'] not in existing_urls:
        current.append(data)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(current, f, ensure_ascii=False, indent=4)

def clean_text_list(raw_text):
    if not raw_text: return []
    lines = [l.strip() for l in raw_text.split('\n') if len(l.strip()) > 3]
    cleaned = []
    for l in lines:
        if re.match(r'^\d+$', l): continue
        if "guía docente" in l.lower(): continue
        item = re.sub(r'^\s*(\d+[\.\)]|[-•·])\s*', '', l).strip()
        if item: cleaned.append(item)
    return cleaned

def extract_pdf_data(session, pdf_url):
    try:
        if 'pdfplumber' not in sys.modules: return None
        r = safe_get(session, pdf_url)
        if not r or r.status_code != 200: return None
        
        with pdfplumber.open(io.BytesIO(r.content)) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            
        patterns = {
            'objectives': r'(?:objetivos|competencias|resultados de aprendizaje)',
            'content': r'(?:contenidos|temario|programa de la asignatura|bloques temáticos)',
            'bibliography': r'(?:bibliografía|referencias|fuentes de información)',
            'stop': r'(?:evaluación|sistema de evaluación|metodología)'
        }
        t_lower = text.lower()
        indices = {k: (re.search(v, t_lower).start() if re.search(v, t_lower) else -1) for k, v in patterns.items()}
        
        extracted = {}
        # Extracción estándar (resumida)
        if indices['content'] != -1:
            start = indices['content']
            end = min([x for x in [indices['bibliography'], indices['stop'], len(text)] if x > start])
            extracted['course_content_outline'] = clean_text_list(text[start:end])
        if indices['objectives'] != -1:
            start = indices['objectives']
            end = min([x for x in [indices['content'], indices['bibliography'], indices['stop'], len(text)] if x > start])
            extracted['learning_objectives'] = clean_text_list(text[start:end])
        if indices['bibliography'] != -1:
            start = indices['bibliography']
            end = min([x for x in [indices['stop'], len(text)] if x > start])
            extracted['bibliography'] = {"references": clean_text_list(text[start:end])}
        return extracted
    except:
        return None

def process_degree_mathematically(session, prefix, center_name, degree_name):
    """
    Núcleo del Algoritmo Matemático.
    Itera C (Curso) y S (Asignatura) hasta encontrar fallos.
    """
    course = 1
    
    while True: # Bucle de CURSOS (1, 2, 3...)
        subject_idx = 1
        found_in_course = False
        
        while True: # Bucle de ASIGNATURAS (01, 02, 03...)
            # Construcción de ID: PREFIJO-C+SS (ej: 170141-5381-101)
            # Formato: {PREFIX}-{COURSE}{IDX:02d}
            generated_id = f"{prefix}-{course}{subject_idx:02d}"
            
            target_url = f"https://sara.uma.es/pls/apex/f?p=101:3:::::P3_ID:{generated_id}"
            
            # Petición
            r = safe_get(session, target_url)
            
            is_valid = False
            subject_name = ""
            
            if r and r.status_code == 200:
                # Comprobar si es una página de error de APEX o válida
                # Una página válida tiene el título de la asignatura visible
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Buscamos el título o el enlace al PDF para confirmar validez
                # En la ficha detalle, el nombre suele estar en un <h1> o <h2>
                # Buscamos el PDF "Guía docente" como prueba de vida definitiva
                pdf_link_tag = soup.find('a', string=re.compile(r"gu[ií]a docente", re.IGNORECASE))
                
                if pdf_link_tag:
                    is_valid = True
                    # Extraer nombre (normalmente en el título de la página o cerca)
                    # Fallback: Usar el título de la página
                    page_title = soup.find('title').get_text(strip=True)
                    # El título suele ser "Programación Docente - Nombre Asignatura"
                    subject_name = page_title.replace("Programación Docente", "").replace("-", "").strip()
            
            if is_valid:
                # === ÉXITO: LA ASIGNATURA EXISTE ===
                found_in_course = True
                log(f"      [OK] {generated_id} -> {subject_name}")
                
                record = {
                    'name': subject_name, 'center': center_name, 'degree': degree_name,
                    'academic_year': course, 'year': CURRENT_YEAR,
                    'url_source': target_url, 'status': 'NO_PDF'
                }
                
                # Descargar PDF
                if pdf_link_tag and 'pdfplumber' in sys.modules:
                    pdf_url = urljoin(PDF_BASE, pdf_link_tag['href'])
                    record['pdf_url'] = pdf_url
                    print(f"         [PDF] Descargando...", end="\r")
                    pdf_data = extract_pdf_data(session, pdf_url)
                    if pdf_data:
                        record.update(pdf_data)
                        record['status'] = 'SUCCESS'
                        print(f"         [PDF] OK            ")
                
                save_incremental(record)
                subject_idx += 1
                time.sleep(0.5) # Pausa técnica
                
            else:
                # === FALLO: LA ASIGNATURA NO EXISTE ===
                # log(f"      [FAIL] {generated_id}")
                
                if subject_idx == 1:
                    # Falló la primera del curso (ej: 401).
                    # CONCLUSIÓN: EL GRADO HA TERMINADO.
                    # log(f"   [FIN GRADO] No existe curso {course}.")
                    return # Salimos de la función, volvemos al siguiente grado
                
                else:
                    # Falló una intermedia (ej: existe 101...109, falla 110).
                    # CONCLUSIÓN: EL CURSO HA TERMINADO.
                    # log(f"   [FIN CURSO] Terminadas asignaturas de {course}º.")
                    break # Rompemos bucle de asignaturas, pasamos al siguiente curso
        
        # Incrementamos curso para la siguiente vuelta del bucle While True
        course += 1
        time.sleep(1)

def run_scraper():
    log("=== UMA MATHEMATICAL: Iteración de IDs ===\n")
    session = get_session()
    
    # 1. Obtener Centros y Grados (Metodología estándar para tener la lista)
    r = safe_get(session, f"{BASE_URL}:::::INICIO_LOV_TIPO_ESTUDIO:3")
    if not r: return
    soup = BeautifulSoup(r.text, 'html.parser')
    p_instance = soup.find('input', {'name': 'p_instance'}).get('value')
    
    select_centros = soup.find('select', {'id': 'INICIO_LOV_CENTROS'})
    centros = [o for o in select_centros.find_all('option') if o.get('value') != '-1']
    
    for i, centro in enumerate(centros):
        id_c = centro.get('value')
        nom_c = centro.get_text(strip=True)
        log(f"[{i+1}/{len(centros)}] {nom_c}")
        
        # Listar Grados
        url_grados = f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS:3,{CURRENT_YEAR},{id_c}"
        r_g = safe_get(session, url_grados)
        soup_g = BeautifulSoup(r_g.text, 'html.parser')
        select_grados = soup_g.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
        
        if not select_grados: continue
        grados = [o for o in select_grados.find_all('option') if o.get('value') != '-1']
        
        for grado in grados:
            id_g = grado.get('value')
            nom_g = grado.get_text(strip=True)
            log(f"   -> {nom_g}")
            
            # --- OBTENCIÓN DEL PREFIJO SEMILLA ---
            # Entramos a la lista de asignaturas (1º año) SOLO para coger un ID de ejemplo
            url_seed = (
                f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::"
                f"INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,"
                f"INICIO_LOV_TITULACIONES,INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:"
                f"3,{CURRENT_YEAR},{id_c},{id_g},1,1," # Forzamos curso 1 para asegurar semilla
            )
            r_seed = safe_get(session, url_seed)
            soup_seed = BeautifulSoup(r_seed.text, 'html.parser')
            
            # Buscamos cualquier enlace a asignatura
            seed_link = soup_seed.find('a', href=re.compile(r'P3_ID:'))
            
            if seed_link:
                # Extraer ID: ...P3_ID:170141-5381-101
                full_id = seed_link['href'].split('P3_ID:')[-1]
                # Cortamos los últimos 4 caracteres (-101) para obtener el PREFIJO
                # Ejemplo: 170141-5381-101 -> prefix = 170141-5381
                if full_id.count('-') >= 2:
                    prefix = "-".join(full_id.split('-')[:-1])
                    
                    # --- INICIAR ATAQUE MATEMÁTICO ---
                    process_degree_mathematically(session, prefix, nom_c, nom_g)
                else:
                    log("      [ERROR] Formato de ID desconocido en semilla.")
            else:
                log("      [ERROR] No se pudo obtener semilla (Grado vacío o error).")

if __name__ == "__main__":
    run_scraper()
