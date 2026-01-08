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
# USAMOS EL ARCHIVO REPARADO COMO BASE Y DESTINO
OUTPUT_FILE = '/sdcard/Download/uma_sextante_fixed.json'
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

def load_existing_data():
    """Carga los datos previos para evitar duplicados."""
    if not os.path.exists(OUTPUT_FILE):
        return [], set()
    
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Creamos un set de claves únicas (URL + Curso)
        keys = {f"{item['url_source']}_{item['academic_year']}" for item in data}
        return data, keys
    except Exception as e:
        log(f"Error cargando archivo existente: {e}")
        return [], set()

def save_batch(full_data):
    """Guarda el archivo completo."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log(f"Error guardando: {e}")

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

def run_scraper():
    log("=== UMA SEXTANTE: REANUDACIÓN INTELIGENTE ===")
    
    # 1. Cargar estado previo
    all_data, existing_keys = load_existing_data()
    log(f"Registros previos cargados: {len(all_data)}")
    
    session = get_session()
    
    # 2. Entrada inicial
    r = safe_get(session, f"{BASE_URL}:::::INICIO_LOV_TIPO_ESTUDIO:3")
    if not r: return
    soup = BeautifulSoup(r.text, 'html.parser')
    p_instance_input = soup.find('input', {'name': 'p_instance'})
    if not p_instance_input: return
    p_instance = p_instance_input.get('value')
    
    select_centros = soup.find('select', {'id': 'INICIO_LOV_CENTROS'})
    centros = [o for o in select_centros.find_all('option') if o.get('value') != '-1']
    
    counter_since_save = 0
    
    for i, centro in enumerate(centros):
        try:
            id_c = centro.get('value')
            nom_c = centro.get_text(strip=True)
            log(f"\n[{i+1}/{len(centros)}] CENTRO: {nom_c}")
            
            # Navegación a grados
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
                # log(f"   -> {nom_g}") # Reducir ruido en log si ya está hecho
                
                for curso_num in range(1, 7):
                    url_asig = (
                        f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::"
                        f"INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,"
                        f"INICIO_LOV_TITULACIONES,INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:"
                        f"3,{CURRENT_YEAR},{id_c},{id_g},-1,{curso_num},"
                    )
                    
                    # Pequeña optimización: no hacemos GET si ya tenemos muchas de este grado/curso
                    # (Difícil de saber a priori, así que hacemos GET y filtramos rápido)
                    
                    r_a = safe_get(session, url_asig)
                    if not r_a: continue
                    soup_a = BeautifulSoup(r_a.text, 'html.parser')
                    
                    links = soup_a.find_all('a', href=re.compile(r'f\?p=101:3'))
                    processed_urls_in_page = set()
                    found_in_year = 0
                    
                    for link in links:
                        nom_asig = link.get_text(strip=True)
                        if not nom_asig or "programación" in nom_asig.lower() or "guía docente" in nom_asig.lower():
                            continue
                        
                        href = link['href']
                        url_detalle = urljoin(BASE_URL, href)
                        
                        if url_detalle in processed_urls_in_page: continue
                        processed_urls_in_page.add(url_detalle)
                        
                        # === LÓGICA DE SALTO (RESUME) ===
                        current_key = f"{url_detalle}_{curso_num}"
                        if current_key in existing_keys:
                            # Ya la tenemos, saltar silenciosamente o con un punto
                            # print(".", end="", flush=True) 
                            found_in_year += 1
                            continue
                        
                        # Si llegamos aquí, ES NUEVA
                        log(f"      [NUEVA] [{curso_num}º] {nom_asig}")
                        
                        record = {
                            'name': nom_asig, 'center': nom_c, 'degree': nom_g,
                            'academic_year': curso_num, 'year': CURRENT_YEAR,
                            'url_source': url_detalle, 'status': 'NO_PDF'
                        }
                        
                        if 'pdfplumber' in sys.modules:
                            r_d = safe_get(session, url_detalle)
                            if r_d:
                                soup_d = BeautifulSoup(r_d.text, 'html.parser')
                                pdf_link = soup_d.find('a', string=re.compile(r"gu[ií]a docente", re.IGNORECASE))
                                if pdf_link:
                                    pdf_url = urljoin(PDF_BASE, pdf_link['href'])
                                    record['pdf_url'] = pdf_url
                                    print("         [PDF] Descargando...", end="\r")
                                    pdf_data = extract_pdf_data(session, pdf_url)
                                    if pdf_data:
                                        record.update(pdf_data)
                                        record['status'] = 'SUCCESS'
                                        print("         [PDF] OK            ")
                        
                        all_data.append(record)
                        existing_keys.add(current_key)
                        
                        # Guardamos cada 5 nuevas para no machacar disco
                        counter_since_save += 1
                        if counter_since_save >= 5:
                            save_batch(all_data)
                            counter_since_save = 0
                            
                        found_in_year += 1
                        time.sleep(0.5)
                    
                    if found_in_year == 0 and curso_num >= 5:
                        break
            
            # Guardado de seguridad al cambiar de centro
            save_batch(all_data)

        except Exception as e:
            log(f"   [ERROR CENTRO] {e}")
            save_batch(all_data) # Guardar por si acaso

    # Guardado final
    save_batch(all_data)
    log("=== FINALIZADO COMPLETO ===")

if __name__ == "__main__":
    run_scraper()
