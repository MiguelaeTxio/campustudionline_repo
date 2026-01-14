import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import sys
import unicodedata

# --- CONFIGURACIÓN ---
BASE_URL = "https://sara.uma.es/pls/apex/"
START_URL = "https://sara.uma.es/pls/apex/f?p=101:1:::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD:3,2025"
OUTPUT_FILE = '/sdcard/Download/uma_full_data_clean.json' 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
}

# --- FILTROS DE EXCLUSIÓN ---
EXCLUDED_TERMS = [
    "trabajo fin de grado", "tfg",
    "prácticas externas", "practicas externas", 
    "prácticum", "practicum",
    "visitas", "visita técnica",
    "pruebas de campo",
    "reconocimiento de créditos", "reconocimiento académico",
    "actividades universitarias",
    "movilidad", "intercambio",
    "optatividad", 
    "créditos optativos"
]

def clean_text(text):
    if not text: return ""
    return unicodedata.normalize("NFKC", text).strip()

def is_valid_subject_name(name):
    name_lower = name.lower()
    if len(name) < 4: return False
    for term in EXCLUDED_TERMS:
        if term in name_lower:
            return False
    return True

def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print(f"Error requesting {url}: {e}")
        return None

def step_1_get_centers():
    print(f"\n[PHASE 1] Discovering Centers from: {START_URL}")
    soup = get_soup(START_URL)
    if not soup: return []
    
    select = soup.find('select', {'id': 'INICIO_LOV_CENTROS'})
    centers = []
    if select:
        for opt in select.find_all('option'):
            val = opt.get('value')
            name = clean_text(opt.get_text())
            if val and val not in ['-1', '-2', '']:
                centers.append({'id': val, 'name': name})
                
    print(f"-> Found {len(centers)} centers.")
    return centers

def step_2_get_degrees(center_id):
    discovery_url = f"https://sara.uma.es/pls/apex/f?p=101:1:::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES:3,2025,{center_id},-1"
    
    soup = get_soup(discovery_url)
    degrees = []
    if not soup: return []
    
    select = soup.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
    if select:
        for opt in select.find_all('option'):
            val = opt.get('value')
            name = clean_text(opt.get_text())
            if val and val != '-1':
                clean_name = name.replace('Graduado/a en ', '').replace('Graduado/a ', '')
                degrees.append({'id': val, 'name': clean_name, 'raw_name': name})
    
    return degrees

def step_3_get_subjects(center_id, degree_id, degree_name):
    list_url = f"https://sara.uma.es/pls/apex/f?p=101:1:::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES,INICIO_BUSCAR:3,2025,{center_id},{degree_id},"
    
    soup = get_soup(list_url)
    if not soup: return []
    
    subjects = []
    rows = soup.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if not cells: continue
        
        link = row.find('a', href=True)
        if not link: continue
        
        href = link['href']
        name = clean_text(link.get_text())
        
        if "javascript" in href: continue
        if not is_valid_subject_name(name): 
            continue
        
        year = None
        for cell in cells:
            txt = clean_text(cell.get_text())
            if txt.isdigit() and len(txt) == 1 and int(txt) <= 6:
                year = int(txt)
                break
        
        if not year: year = 0
            
        full_link = urljoin(BASE_URL, href)
        
        subjects.append({
            "university": "Universidad de Málaga",
            "center_id": center_id,
            "degree": degree_name,
            "degree_id": degree_id,
            "year": year,
            "name": name,
            "url_source": full_link,
            "pdf_url": None
        })
        
    return subjects

def main():
    print("==========================================")
    print("   UMA HARVESTER V1.2 (CLEAN DATA)   ")
    print("==========================================")
    
    all_data = []
    centers = step_1_get_centers()
    
    if not centers:
        print("[FATAL] No centers found.")
        return

    print(f"\nProcessing {len(centers)} centers...")
    
    for i, center in enumerate(centers):
        print(f"\n[{i+1}/{len(centers)}] CENTER: {center['name']}")
        degrees = step_2_get_degrees(center['id'])
        
        for deg in degrees:
            print(f"      Processing: {deg['name']}...", end='', flush=True)
            subjects = step_3_get_subjects(center['id'], deg['id'], deg['name'])
            print(f" {len(subjects)} valid subjects.")
            all_data.extend(subjects)
            
    print(f"\nSAVING DATA to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"DONE. Total valid records: {len(all_data)}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
