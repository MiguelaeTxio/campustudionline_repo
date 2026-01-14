import requests
from bs4 import BeautifulSoup
import json
import re
import io
import time
from pypdf import PdfReader
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URLS = {
    "Escenografía": "https://esadcordoba.com/inicio/oferta-formativa/escenografia/",
    "Interpretación": "https://esadcordoba.com/inicio/oferta-formativa/estudiar-interpretacion-en-andalucia/"
}
OUTPUT_FILE = "esad_final_data_v2.json"

def get_drive_direct_link(url):
    patterns = [r'drive\.google\.com/file/d/([^/]+)', r'drive\.google\.com/open\?id=([^/&]+)']
    for p in patterns:
        match = re.search(p, url)
        if match: return f"https://drive.google.com/uc?export=download&id={match.group(1)}"
    return url

def extract_text(content):
    try:
        reader = PdfReader(io.BytesIO(content))
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except: return ""

def clean(text):
    return re.sub(r'\s+', ' ', text).strip() if text else ""

def main():
    final_data = []
    
    with requests.Session() as s:
        s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'verify': 'False'
        })

        for degree_name, url in URLS.items():
            print(f"\n--- GRADO: {degree_name} ---")
            try:
                r = s.get(url, verify=False)
                soup = BeautifulSoup(r.content, 'html.parser')
                
                # Buscamos encabezados de curso y tablas
                elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'strong', 'p', 'tr'])
                
                current_year = 1
                degree_subjects = []
                processed_names = set()

                for el in elements:
                    text = el.get_text(separator=' ', strip=True).lower()
                    
                    # DETECTOR DE CAMBIO DE CURSO
                    if "primer curso" in text and len(text) < 60: current_year = 1
                    elif "segundo curso" in text and len(text) < 60: current_year = 2
                    elif "tercer curso" in text and len(text) < 60: current_year = 3
                    elif "cuarto curso" in text and len(text) < 60: current_year = 4
                    
                    # PROCESAR FILAS
                    if el.name == 'tr':
                        link = el.find('a', href=True)
                        cols = el.find_all('td')
                        
                        if link and cols and ("guía" in link.text.lower() or "descargar" in link.text.lower()):
                            subj_name = cols[0].get_text(strip=True)
                            subj_name = re.sub(r'\(.*?\)', '', subj_name).strip()
                            
                            if subj_name in processed_names: continue
                            processed_names.add(subj_name)

                            print(f"[{current_year}º] {subj_name}...")
                            
                            pdf_text = ""
                            try:
                                d_url = get_drive_direct_link(link['href'])
                                pdf_resp = s.get(d_url, verify=False, timeout=15)
                                if pdf_resp.status_code == 200:
                                    pdf_text = clean(extract_text(pdf_resp.content))
                            except: pass

                            # Estructura plana
                            final_data.append({
                                "degree": f"Grado en Enseñanzas Artísticas Superiores de {degree_name}",
                                "branch": "Artes y Humanidades",
                                "year": current_year,
                                "subjects": [{
                                    "name": subj_name,
                                    "learning_objectives": [],
                                    "course_content_outline": [pdf_text] if pdf_text else [],
                                    "bibliography": {}
                                }]
                            })

            except Exception as e: print(f"Error: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"\nArchivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
