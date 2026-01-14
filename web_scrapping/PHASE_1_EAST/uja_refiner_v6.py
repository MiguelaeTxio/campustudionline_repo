import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import concurrent.futures
import re

# --- RUTAS ABSOLUTAS ---
INPUT_FILE = "/sdcard/Download/uja_raw_data.json"
OUTPUT_FILE = "/sdcard/Download/uja_refined.json"
MAX_WORKERS = 10 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def get_session():
    session = requests.Session()
    retry = Retry(total=8, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

def parse_details_v6(session, url):
    data = {}
    try:
        response = session.get(url, headers=HEADERS, timeout=20)
        if response.status_code != 200: return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # ESTRATEGIA 1: BÚSQUEDA POR CLASES
        labels = soup.find_all('div', class_='fdoca_celda_descripcion_concepto')
        
        for label in labels:
            key = label.get_text(strip=True).upper()
            value_div = label.find_next_sibling('div', class_='fdoca_celda_valor_concepto')
            if not value_div: continue
            val = value_div.get_text(strip=True).upper()

            if "CURSO" in key:
                digits = re.findall(r'\d+', val)
                if digits: 
                    y = int(digits[0])
                    # SANITY CHECK: Filtro anti-basura (Ej: Año 120)
                    if 1 <= y <= 6:
                        data["year"] = y
            
            elif "CUATRIMESTRE" in key:
                if "PRIMER" in val: data["semester"] = 1
                elif "SEGUNDO" in val: data["semester"] = 2
                elif "ANUAL" in val: data["semester"] = None
            
            elif "TIPO" in key:
                if "OBLIGATORIA" in val: data["type"] = "OB"
                elif "BÁSICA" in val: data["type"] = "BA"
                elif "OPTATIVA" in val: data["type"] = "OP"
                elif "TRONCAL" in val: data["type"] = "TR"

        # ESTRATEGIA 2: FALLBACK
        if "year" not in data:
            divs = soup.find_all('div')
            for div in divs:
                if "CURSO:" in div.get_text(strip=True).upper():
                    nxt = div.find_next_sibling('div')
                    if nxt:
                        d = re.findall(r'\d+', nxt.get_text())
                        if d: 
                            y = int(d[0])
                            if 1 <= y <= 6: data["year"] = y

        return data if data else None

    except Exception:
        return None

def process_subject(args):
    subject, session = args
    url = subject.get('guide_url')
    
    # IMPORTANTE: No saltamos si year > 1 para corregir los 120 erróneos de la pasada anterior
    # if subject.get('year', 1) > 1: return subject 

    if not url: return subject
    
    details = parse_details_v6(session, url)
    if details:
        subject.update(details)
        y = subject.get('year', 1)
        if y > 1:
            print(f"   ✅ {subject['name'][:25]}... -> Año {y}")
    
    return subject

def main():
    print("🚀 REFINERÍA UJA V6 (CON SANITY CHECK)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Falta {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    session = get_session()
    
    for i, degree in enumerate(data):
        subjects = degree.get('subjects', [])
        if not subjects: continue
        
        d_name = degree.get('degree', degree.get('degree_name', 'TITULACION'))
        print(f"\n[{i+1}/{len(data)}] {d_name}")
        
        work_items = [(s, session) for s in subjects]
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            refined = list(executor.map(process_subject, work_items))
        degree['subjects'] = refined
        
        if i % 3 == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"\n✨ FIN V6. Archivo: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
