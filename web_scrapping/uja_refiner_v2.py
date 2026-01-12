# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uja_refiner_v2.py
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import concurrent.futures
import time
import re

# Configuración
INPUT_FILE = "uja_raw_data.json"
OUTPUT_FILE = "uja_refined.json"
MAX_WORKERS = 10 # Bajamos un poco para estabilidad
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

# Configuración de Sesión con Reintentos
def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def parse_subject_details(session, url):
    """Extrae Curso, Semestre y Tipo de forma robusta."""
    try:
        response = session.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {}
        
        # Función auxiliar para limpiar texto
        def clean(t): return t.get_text(strip=True).upper() if t else ""

        # Buscar celdas (td o th) que contengan las palabras clave
        cells = soup.find_all(['td', 'th'])
        
        for cell in cells:
            text = clean(cell)
            
            # 1. CURSO
            if "CURSO" in text and len(text) < 20: # Evitar falsos positivos largos
                sibling = cell.find_next_sibling('td')
                if sibling:
                    val = clean(sibling)
                    # Extraer el primer dígito encontrado
                    digits = re.findall(r'\d+', val)
                    if digits:
                        data["year"] = int(digits[0])

            # 2. CUATRIMESTRE
            if "CUATRIMESTRE" in text:
                sibling = cell.find_next_sibling('td')
                if sibling:
                    val = clean(sibling)
                    if "PRIMER" in val: data["semester"] = 1
                    elif "SEGUNDO" in val: data["semester"] = 2
                    elif "ANUAL" in val: data["semester"] = None

            # 3. TIPO
            if "TIPO" in text and len(text) < 15:
                sibling = cell.find_next_sibling('td')
                if sibling:
                    val = clean(sibling)
                    if "OBLIGATORIA" in val: data["type"] = "OB"
                    elif "BÁSICA" in val or "BASICA" in val: data["type"] = "BA"
                    elif "OPTATIVA" in val: data["type"] = "OP"
                    elif "TRONCAL" in val: data["type"] = "TR"

        return data if data else None

    except Exception as e:
        # print(f"Error parseando {url}: {e}")
        return None

def process_subject(args):
    """Wrapper para procesar asignatura."""
    subject, session = args
    url = subject.get('guide_url')
    
    # Si ya tiene año > 1, asumimos que está bien (optimización para re-runs)
    if subject.get('year', 1) > 1:
        return subject

    if not url:
        return subject
    
    details = parse_subject_details(session, url)
    if details:
        subject.update(details)
        # Debug para verificar que funciona
        if subject.get('year', 1) > 1:
            print(f"   ✅ {subject['name'][:20]}... -> Año {subject['year']}")
    
    return subject

def refine():
    print("💎 INICIANDO REFINERÍA UJA V2 (ROBUSTA)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Falta {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Preparar sesión global no es thread-safe del todo, mejor una por hilo o local
    # Usaremos una estrategia de crear sesión dentro del worker si fuera proceso, 
    # pero con hilos requests.Session es thread-safe.
    session = get_session()

    total_degrees = len(data)
    
    # Aplanar lista para procesar
    # Pero necesitamos mantener estructura. 
    # Procesaremos grado a grado para guardar parciales.
    
    for i, degree in enumerate(data):
        subjects = degree.get('subjects', [])
        if not subjects: continue

        print(f"\n[{i+1}/{total_degrees}] Refinando: {degree['degree_name']}")
        
        # Crear tuplas (subject, session) para pasar al map
        work_items = [(s, session) for s in subjects]
        
        refined_subjects = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            refined_subjects = list(executor.map(process_subject, work_items))
        
        degree['subjects'] = refined_subjects
        
        # Guardado parcial frecuente
        if i % 2 == 0:
             with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    # Guardado Final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n✨ REFINADO V2 COMPLETO.")
    print(f"📄 Resultado: {OUTPUT_FILE}")

if __name__ == "__main__":
    refine()
