import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

# --- CONFIGURACIÓN RUTA ABSOLUTA ANDROID ---
OUTPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
BASE_URL = "https://grados.ugr.es"
TARGET_DEGREES = [
    "arabe", "franceses", "ingleses", "modernas", "hispanicos", "clasica"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def extract_year(text):
    """Convierte 'Primer curso' en 1, etc."""
    text = text.upper()
    if "PRIMER" in text: return 1
    if "SEGUNDO" in text: return 2
    if "TERCER" in text: return 3
    if "CUARTO" in text: return 4
    return 1

def get_subjects_v2(degree_slug):
    url = f"{BASE_URL}/{degree_slug}/plan-de-estudios"
    print(f"   📖 Procesando plan: {url}")
    subjects = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200: return []
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # 1. Buscar bloques de curso (h2 id="contenidoX")
        course_headers = soup.find_all('h2', id=re.compile(r'contenido\d+'))
        
        for header in course_headers:
            year = extract_year(header.get_text())
            
            # Buscamos las tablas siguientes hasta el próximo h2
            sibling = header.find_next_sibling()
            while sibling and sibling.name != 'h2':
                # Las tablas están dentro de un div block-views...
                table = sibling.find('table', class_='tabla-semestre') if sibling.name != 'table' else sibling
                
                if table and table.name == 'table':
                    # Detectar Semestre del caption
                    semester = 1
                    caption = table.find('caption')
                    if caption and "SEGUNDO" in caption.get_text().upper():
                        semester = 2
                    
                    # Extraer asignaturas de la tabla
                    rows = table.find_all('tr')
                    for row in rows:
                        td_name = row.find('td', class_='asignatura')
                        if td_name and td_name.find('a'):
                            link_tag = td_name.find('a')
                            name = link_tag.get_text(strip=True)
                            
                            td_type = row.find('td', class_='tipo')
                            subj_type_raw = td_type.get_text(strip=True) if td_type else "Optativa"
                            
                            # Mapeo de tipos
                            stype = "OP"
                            if "TRONCAL" in subj_type_raw.upper() or "BÁSICA" in subj_type_raw.upper(): stype = "BA"
                            elif "OBLIGATORIA" in subj_type_raw.upper(): stype = "OB"

                            subjects.append({
                                "name": name,
                                "year": year,
                                "semester": semester,
                                "type": stype,
                                "url": link_tag.get('href')
                            })
                
                # Avanzar al siguiente hermano para seguir buscando tablas de este curso
                sibling = sibling.find_next_sibling()
                if not sibling: break

        return subjects
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def main():
    print("🚀 INICIANDO RECONSTRUCCIÓN UGR V2...")
    all_data = []

    for slug in TARGET_DEGREES:
        print(f"\n🎓 Grado: {slug}")
        subjects = get_subjects_v2(slug)
        if subjects:
            all_data.append({
                "university": "Universidad de Granada",
                "degree_slug": slug,
                "subjects": subjects
            })
            print(f"   ✅ {len(subjects)} asignaturas recuperadas.")
        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ FIN. Datos guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
