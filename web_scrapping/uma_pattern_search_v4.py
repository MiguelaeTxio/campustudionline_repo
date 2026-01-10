import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import io
import re
import sys
import time
import os

# --- CONFIGURACIÓN ---
BASE_URL = "https://sara.uma.es/pls/apex/f?p=101:1"
PDF_BASE = "https://sara.uma.es"
OUTPUT_FILE = '/sdcard/Download/uma_pattern_data.json'
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
        if indices['content'] != -1:
            start = indices['content']
            candidates = [indices['bibliography'], indices['stop'], len(text)]
            end = min([x for x in candidates if x > start])
            extracted['course_content_outline'] = clean_text_list(text[start:end])
            
        if indices['objectives'] != -1:
            start = indices['objectives']
            candidates = [indices['content'], indices['bibliography'], indices['stop'], len(text)]
            end = min([x for x in candidates if x > start])
            extracted['learning_objectives'] = clean_text_list(text[start:end])
            
        if indices['bibliography'] != -1:
            start = indices['bibliography']
            candidates = [indices['stop'], len(text)]
            end = min([x for x in candidates if x > start])
            extracted['bibliography'] = {"references": clean_text_list(text[start:end])}
            
        return extracted
    except:
        return None

def find_link_by_suffix(soup, suffix):
    for a in soup.find_all('a', href=True):
        if a['href'].endswith(suffix) or f"{suffix}:" in a['href']: 
            return a
    return None

def run_scraper():
    log("=== UMA PATTERN SEARCH: Iteración 101, 102... ===")
    # === RESUME LOGIC ===
    existing_urls = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_urls = {item['url_source'] for item in json.load(f)}
            log(f"=== RESUMING: Found {len(existing_urls)} existing records ===")
        except: pass

    session = get_session()
    
    # 1. ENTRADA
    r = safe_get(session, f"{BASE_URL}:::::INICIO_LOV_TIPO_ESTUDIO:3")
    if not r: return
    soup = BeautifulSoup(r.text, 'html.parser')
    p_instance_input = soup.find('input', {'name': 'p_instance'})
    if not p_instance_input: return
    p_instance = p_instance_input.get('value')
    
    select_centros = soup.find('select', {'id': 'INICIO_LOV_CENTROS'})
    centros = [o for o in select_centros.find_all('option') if o.get('value') != '-1']
    
    for i, centro in enumerate(centros):
        try:
            id_c = centro.get('value')
            nom_c = centro.get_text(strip=True)
            log(f"\n[{i+1}/{len(centros)}] {nom_c}")
            
            # 2. TITULACIONES
            url_grados = f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS:3,{CURRENT_YEAR},{id_c}"
            r_g = safe_get(session, url_grados)
            if not r_g: continue
            soup_g = BeautifulSoup(r_g.text, 'html.parser')
            
            select_grados = soup_g.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
            if not select_grados: continue
            grados = [o for o in select_grados.find_all('option') if o.get('value') != '-1']
            
            for grado in grados:
                id_g = grado.get('value')
                nom_g = grado.get_text(strip=True)
                log(f"   -> {nom_g} (ID: {id_g})")
                
                # 3. CURSOS (1 a 6)
                for curso_num in range(1, 7):
                    # Cargamos la página del curso
                    url_listado = f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES,INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:3,{CURRENT_YEAR},{id_c},{id_g},1,-1,"
                    
                    r_a = safe_get(session, url_listado)
                    if not r_a: continue
                    soup_a = BeautifulSoup(r_a.text, 'html.parser')
                    
                    # === BUCLE DE ASIGNATURAS (101, 102...) ===
                    subject_idx = 1
                    found_subjects_in_course = 0
                    consecutive_misses = 0
                    MAX_MISSES = 10
                    
                    while True:
                        # Sufijo: -{id_grado}-{curso}{idx}
                        suffix = f"-{id_g}-{curso_num}{subject_idx:02d}"
                        
                        link = find_link_by_suffix(soup_a, suffix)
                        
                        if link:
                            nom_asig = link.get_text(strip=True)
                            full_href = link['href']
                            consecutive_misses = 0
                            log(f"      [OK] {suffix} -> {nom_asig}")
                            
                            url_detalle = urljoin(BASE_URL, full_href)

                            if url_detalle in existing_urls:
                                log(f"      [SKIP] {nom_asig}")
                                consecutive_misses = 0
                                found_subjects_in_course += 1
                                subject_idx += 1
                                continue

                            record = {
                                'name': nom_asig, 'center': nom_c, 'degree': nom_g,
                                'academic_year': curso_num, 'year': CURRENT_YEAR,
                                'url_source': url_detalle, 'status': 'NO_PDF'
                            }
                            
                            # PDF DOWNLOAD
                            if 'pdfplumber' in sys.modules:
                                r_d = safe_get(session, url_detalle)
                                if r_d:
                                    soup_d = BeautifulSoup(r_d.text, 'html.parser')
                                    pdf_link = soup_d.find('a', string=re.compile(r"gu[ií]a docente", re.IGNORECASE))
                                    if pdf_link:
                                        pdf_url = urljoin(PDF_BASE, pdf_link['href'])
                                        record['pdf_url'] = pdf_url
                                        print(f"         [PDF] Descargando...", end="\r")
                                        pdf_data = extract_pdf_data(session, pdf_url)
                                        if pdf_data:
                                            record.update(pdf_data)
                                            record['status'] = 'SUCCESS'
                                            print(f"         [PDF] OK            ")
                            
                            save_incremental(record)
                            found_subjects_in_course += 1
                            subject_idx += 1
                            time.sleep(0.5)
                        else:
                            # Tolerancia a huecos (ej: empieza en 402 y no 401)
                            consecutive_misses += 1
                            if consecutive_misses > MAX_MISSES:
                                break
                            subject_idx += 1
                            continue
                    
                    # Si no encontramos asignaturas en este curso, ¿es fin de carrera?
                    if found_subjects_in_course == 0:
                        if curso_num >= 4:
                            break
                            
                    time.sleep(1)

        except Exception as e:
            log(f"   [ERROR CENTRO] {e}")

if __name__ == "__main__":
    run_scraper()
