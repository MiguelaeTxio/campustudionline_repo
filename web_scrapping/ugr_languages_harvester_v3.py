import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

# --- CONFIGURACIÓN RUTA ABSOLUTA ANDROID ---
OUTPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
BASE_URL = "https://grados.ugr.es"

# Diccionario con las URLs reales mapeadas del portal UGR
TARGET_DEGREES = {
    "Estudios Árabes e Islámicos": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-arabes-islamicos",
    "Estudios Franceses": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-franceses",
    "Estudios Ingleses": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-ingleses",
    "Lenguas Modernas y sus Literaturas": "https://grados.ugr.es/ramas/artes-humanidades/grado-lenguas-modernas-sus-literaturas",
    "Filología Hispánica": "https://grados.ugr.es/ramas/artes-humanidades/grado-filologia-hispanica",
    "Filología Clásica": "https://grados.ugr.es/ramas/artes-humanidades/grado-filologia-clasica"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def extract_year(text):
    text = text.upper()
    if "PRIMER" in text: return 1
    if "SEGUNDO" in text: return 2
    if "TERCER" in text: return 3
    if "CUARTO" in text: return 4
    return 1

def get_subjects_v3(name, url):
    print(f"   📖 Procesando: {name}")
    subjects = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"   ❌ Error HTTP {r.status_code}")
            return []
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Buscar bloques de curso (h2 id="contenidoX")
        course_headers = soup.find_all('h2', id=re.compile(r'contenido\d+'))
        
        if not course_headers:
            print("   ⚠️ No se detectaron encabezados de curso. Revisando estructura alternativa...")

        for header in course_headers:
            year = extract_year(header.get_text())
            
            # Navegar por los hermanos hasta el siguiente h2
            sibling = header.find_next_sibling()
            while sibling and sibling.name != 'h2':
                # Buscar tablas en el interior del hermano
                tables = sibling.find_all('table', class_='tabla-semestre')
                if not tables and sibling.name == 'table' and 'tabla-semestre' in sibling.get('class', []):
                    tables = [sibling]

                for table in tables:
                    # Detectar Semestre
                    semester = 1
                    caption = table.find('caption')
                    if caption and "SEGUNDO" in caption.get_text().upper():
                        semester = 2
                    
                    # Extraer asignaturas
                    rows = table.find_all('tr')
                    for row in rows:
                        td_name = row.find('td', class_='asignatura')
                        if td_name and td_name.find('a'):
                            link_tag = td_name.find('a')
                            subj_name = link_tag.get_text(strip=True)
                            
                            td_type = row.find('td', class_='tipo')
                            subj_type_raw = td_type.get_text(strip=True) if td_type else "Optativa"
                            
                            stype = "OP"
                            if "TRONCAL" in subj_type_raw.upper() or "BÁSICA" in subj_type_raw.upper(): stype = "BA"
                            elif "OBLIGATORIA" in subj_type_raw.upper(): stype = "OB"

                            subjects.append({
                                "name": subj_name,
                                "year": year,
                                "semester": semester,
                                "type": stype,
                                "url": link_tag.get('href')
                            })
                
                sibling = sibling.find_next_sibling()
                if not sibling: break

        return subjects
    except Exception as e:
        print(f"   ❌ Error crítico: {e}")
        return []

def main():
    print("🚀 INICIANDO RECONSTRUCCIÓN UGR V3 (URLs CORREGIDAS)...")
    all_data = []

    for name, url in TARGET_DEGREES.items():
        subjects = get_subjects_v3(name, url)
        if subjects:
            all_data.append({
                "university": "Universidad de Granada",
                "degree_name": name,
                "subjects": subjects
            })
            print(f"   ✅ {len(subjects)} asignaturas recuperadas.")
        else:
            print(f"   ❌ Fallo total en {name}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ FIN V3. Datos guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
