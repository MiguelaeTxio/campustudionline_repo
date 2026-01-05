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
OUTPUT_FILE = "esad_final_data_v3.json"

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
                
                # Buscamos todos los elementos en orden de aparición
                elements = soup.find_all(['h4', 'tr'])
                
                current_year = 1
                degree_subjects = []
                processed_names = set()

                for el in elements:
                    text = el.get_text(separator=' ', strip=True).lower()
                    
                    # DETECTOR DE AÑO (CORREGIDO PARA 1º, 2º, etc.)
                    if "1º curso" in text or "primer curso" in text: current_year = 1
                    elif "2º curso" in text or "segundo curso" in text: current_year = 2
                    elif "3º curso" in text or "tercer curso" in text: current_year = 3
                    elif "4º curso" in text or "cuarto curso" in text: current_year = 4
                    
                    # PROCESAMIENTO DE ASIGNATURAS
                    if el.name == 'tr':
                        link = el.find('a', href=True)
                        cols = el.find_all('td')
                        
                        if link and cols and ("guía" in link.text.lower() or "descargar" in link.text.lower()):
                            subj_name = cols[0].get_text(strip=True)
                            subj_name = re.sub(r'\(.*?\)', '', subj_name).strip()
                            
                            # Evitar duplicados (la web tiene tablas repetidas)
                            if subj_name in processed_names: continue
                            processed_names.add(subj_name)

                            print(f"[{current_year}º] {subj_name}...")
                            
                            # Descarga PDF
                            pdf_text = ""
                            try:
                                d_url = get_drive_direct_link(link['href'])
                                pdf_resp = s.get(d_url, verify=False, timeout=15)
                                if pdf_resp.status_code == 200:
                                    pdf_text = clean(extract_text(pdf_resp.content))
                            except: pass

                            degree_subjects.append({
                                "name": subj_name,
                                "year": current_year,
                                "outline": [pdf_text] if pdf_text else []
                            })

                # Estructurar JSON Final
                for subj in degree_subjects:
                    final_data.append({
                        "degree": f"Grado en Enseñanzas Artísticas Superiores de {degree_name}",
                        "branch": "Artes y Humanidades",
                        "year": subj['year'],
                        "subjects": [{
                            "name": subj['name'],
                            "learning_objectives": [],
                            "course_content_outline": subj['outline'],
                            "bibliography": {}
                        }]
                    })

            except Exception as e: print(f"Error: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"\nArchivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
