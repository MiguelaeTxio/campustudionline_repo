# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uja_refiner_v3.py
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import concurrent.futures
import re

# --- CONFIGURACIÓN ---
INPUT_FILE = "uja_raw_data.json"
OUTPUT_FILE = "uja_refined.json"
MAX_WORKERS = 12 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def get_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

def parse_details_divs(session, url):
    """Parser específico para estructura de DIVs de la UJA."""
    data = {}
    try:
        response = session.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200: return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar todos los divs que actúan como etiquetas
        # Buscamos por texto porque las clases pueden variar, pero la estructura visual no.
        # El texto suele ser "Curso:", "Tipo:", etc.
        divs = soup.find_all('div')
        
        for div in divs:
            text = div.get_text(strip=True).upper()
            
            # Optimización: saltar divs largos
            if len(text) > 30: continue

            # 1. CURSO
            # Busca exactitud o el patrón "Curso:"
            if "CURSO:" in text: 
                val_div = div.find_next_sibling('div')
                if val_div:
                    val = val_div.get_text(strip=True)
                    digits = re.findall(r'\d+', val)
                    if digits:
                        data["year"] = int(digits[0])

            # 2. CUATRIMESTRE
            if "CUATRIMESTRE" in text:
                val_div = div.find_next_sibling('div')
                if val_div:
                    val = val_div.get_text(strip=True).upper()
                    if "PRIMER" in val: data["semester"] = 1
                    elif "SEGUNDO" in val: data["semester"] = 2
                    elif "ANUAL" in val: data["semester"] = None

            # 3. TIPO
            if "TIPO:" in text:
                val_div = div.find_next_sibling('div')
                if val_div:
                    val = val_div.get_text(strip=True).upper()
                    if "OBLIGATORIA" in val: data["type"] = "OB"
                    elif "BÁSICA" in val or "BASICA" in val: data["type"] = "BA"
                    elif "OPTATIVA" in val: data["type"] = "OP"
                    elif "TRONCAL" in val: data["type"] = "TR"

        return data if data else None

    except Exception:
        return None

def process_subject(args):
    subject, session = args
    url = subject.get('guide_url')
    
    # Si ya tiene año > 1, saltar (si ejecutamos varias veces)
    if subject.get('year', 1) > 1:
        return subject

    if not url: return subject
    
    details = parse_details_divs(session, url)
    if details:
        subject.update(details)
        if subject.get('year', 1) > 1:
            print(f"   ✅ {subject['name'][:25]}... -> Año {subject['year']}")
    
    return subject

def main():
    print("🚀 REFINERÍA UJA V3 (PARSER DIVs)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Falta {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    session = get_session()
    total = len(data)

    for i, degree in enumerate(data):
        subjects = degree.get('subjects', [])
        if not subjects: continue
        
        print(f"\n[{i+1}/{total}] {degree['degree_name']}")
        
        work_items = [(s, session) for s in subjects]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            refined = list(executor.map(process_subject, work_items))
        
        degree['subjects'] = refined
        
        if i % 3 == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"\n✨ FIN V3. Archivo: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
