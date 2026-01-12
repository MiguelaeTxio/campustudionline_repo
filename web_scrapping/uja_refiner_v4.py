import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import concurrent.futures
import re

# --- RUTAS ABSOLUTAS ANDROID (NO TOCAR) ---
INPUT_FILE = "/sdcard/Download/uja_raw_data.json"
OUTPUT_FILE = "/sdcard/Download/uja_refined.json"
MAX_WORKERS = 10 
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
    data = {}
    try:
        response = session.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200: return None
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div')
        for div in divs:
            text = div.get_text(strip=True).upper()
            if len(text) > 30: continue
            if "CURSO:" in text: 
                val_div = div.find_next_sibling('div')
                if val_div:
                    digits = re.findall(r'\d+', val_div.get_text(strip=True))
                    if digits: data["year"] = int(digits[0])
            if "CUATRIMESTRE" in text:
                val_div = div.find_next_sibling('div')
                if val_div:
                    val = val_div.get_text(strip=True).upper()
                    if "PRIMER" in val: data["semester"] = 1
                    elif "SEGUNDO" in val: data["semester"] = 2
                    elif "ANUAL" in val: data["semester"] = None
            if "TIPO" in text:
                val_div = div.find_next_sibling('div')
                if val_div:
                    val = val_div.get_text(strip=True).upper()
                    if "OBLIGATORIA" in val: data["type"] = "OB"
                    elif "BÁSICA" in val or "BASICA" in val: data["type"] = "BA"
                    elif "OPTATIVA" in val: data["type"] = "OP"
                    elif "TRONCAL" in val: data["type"] = "TR"
        return data if data else None
    except: return None

def process_subject(args):
    subject, session = args
    url = subject.get('guide_url')
    # Si ya tiene año > 1, saltar
    if subject.get('year', 1) > 1: return subject
    if not url: return subject
    details = parse_details_divs(session, url)
    if details:
        subject.update(details)
        if subject.get('year', 1) > 1:
            print(f"   ✅ {subject['name'][:25]}... -> Año {subject['year']}")
    return subject

def main():
    print("🚀 REFINERÍA UJA V4 (ABSOLUTE PATHS)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ CRÍTICO: No se encuentra {INPUT_FILE}")
        print("Asegúrate de que 'uja_raw_data.json' está en /sdcard/Download/")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    session = get_session()
    
    for i, degree in enumerate(data):
        subjects = degree.get('subjects', [])
        if not subjects: continue
        
        # CORRECCIÓN DE CLAVE SEGURA
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
        
    print(f"\n✨ FIN V4. Archivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
