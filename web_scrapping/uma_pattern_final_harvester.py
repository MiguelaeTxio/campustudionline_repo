# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uma_pattern_final_harvester.py
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
OUTPUT_FILE = '/sdcard/Download/uma_pattern_final_data.json'
CURRENT_YEAR = "2025" 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Connection': 'keep-alive'
}

try:
    import pdfplumber
except ImportError:
    pass

def log(msg, end="\n"):
    print(msg, end=end)
    sys.stdout.flush()

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
        log(f"\n   [ERROR RED] {e}. Reintentando...")
        time.sleep(5)
        return None

def load_existing_data():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

def save_incremental(data, current_list):
    current_list.append(data)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_list, f, ensure_ascii=False, indent=4)

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
        # Lógica de segmentación por "anclas"
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
    except: return None

def find_link_by_suffix(soup, suffix):
    for a in soup.find_all('a', href=True):
        if a['href'].endswith(suffix) or f"{suffix}:" in a['href']: 
            return a
    return None

def run_scraper():
    log("=== UMA PATTERN FINAL HARVESTER (Modo Ciclo -1) ===")
    session = get_session()
    
    # 0. Cargar datos existentes para reanudación
    existing_data = load_existing_data()
    processed_urls = {item['url_source'] for item in existing_data}
    log(f"[INFO] Registros detectados en el JSON: {len(processed_urls)}")

    # 1. ENTRADA INICIAL
    r = safe_get(session, f"{BASE_URL}:::::INICIO_LOV_TIPO_ESTUDIO:3")
    if not r: return
    soup = BeautifulSoup(r.text, 'html.parser')
    p_instance = soup.find('input', {'name': 'p_instance'}).get('value')
    
    centros_select = soup.find('select', {'id': 'INICIO_LOV_CENTROS'})
    centros = [(o.get('value'), o.get_text(strip=True)) for o in centros_select.find_all('option') if o.get('value') != '-1']
    
    for i, (id_c, nom_c) in enumerate(centros):
        log(f"\n[{i+1}/{len(centros)}] CENTRO: {nom_c}")
        
        # 2. OBTENER TITULACIONES DEL CENTRO
        url_grados = f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS:3,{CURRENT_YEAR},{id_c}"
        r_g = safe_get(session, url_grados)
        if not r_g: continue
        soup_g = BeautifulSoup(r_g.text, 'html.parser')
        
        grados_select = soup_g.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
        if not grados_select: continue
        grados = [(o.get('value'), o.get_text(strip=True)) for o in grados_select.find_all('option') if o.get('value') != '-1']
        
        for id_g, nom_g in grados:
            log(f"   -> GRADO: {nom_g}")
            
            for curso_num in range(1, 7):
                url_listado = f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES,INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:3,{CURRENT_YEAR},{id_c},{id_g},-1,{curso_num},"
                
                r_a = safe_get(session, url_listado)
                if not r_a: continue
                soup_a = BeautifulSoup(r_a.text, 'html.parser')
                
                subject_idx = 1
                found_in_course = 0
                
                while True:
                    suffix = f"-{id_g}-{curso_num}{subject_idx:02d}"
                    link = find_link_by_suffix(soup_a, suffix)
                    
                    if link:
                        nom_asig = link.get_text(strip=True)
                        url_detalle = urljoin(BASE_URL, link['href'])
                        
                        if url_detalle in processed_urls:
                            log(f"      [SKIP] {nom_asig} ya existe.", end="\r")
                            found_in_course += 1
                            subject_idx += 1
                            continue

                        log(f"      [PROCESS] {nom_asig}...", end="\r")
                        record = {
                            'name': nom_asig, 'center': nom_c, 'degree': nom_g,
                            'academic_year': curso_num, 'year': CURRENT_YEAR,
                            'url_source': url_detalle, 'status': 'NO_PDF'
                        }
                        
                        # PDF
                        r_d = safe_get(session, url_detalle)
                        if r_d:
                            soup_d = BeautifulSoup(r_d.text, 'html.parser')
                            pdf_link = soup_d.find('a', string=re.compile(r"gu[ií]a docente", re.IGNORECASE))
                            if pdf_link:
                                pdf_url = urljoin(PDF_BASE, pdf_link['href'])
                                record['pdf_url'] = pdf_url
                                pdf_data = extract_pdf_data(session, pdf_url)
                                if pdf_data:
                                    record.update(pdf_data)
                                    record['status'] = 'SUCCESS'
                        
                        save_incremental(record, existing_data)
                        processed_urls.add(url_detalle)
                        found_in_course += 1
                        subject_idx += 1
                        log(f"      [OK] {nom_asig} ({record['status']})")
                        time.sleep(0.3)
                    else: break
                
                if found_in_course == 0 and curso_num >= 4: break
                time.sleep(0.5)

if __name__ == "__main__":
    run_scraper()
