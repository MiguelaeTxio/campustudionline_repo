import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

# --- CONFIGURACIÓN ESTRICTA ANDROID ---
OUTPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
BASE_URL = "https://grados.ugr.es"

TARGET_DEGREES = {
    "Estudios Árabes e Islámicos": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-arabes-islamicos",
    "Estudios Franceses": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-franceses",
    "Estudios Ingleses": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-ingleses",
    "Lenguas Modernas y sus Literaturas": "https://grados.ugr.es/ramas/artes-humanidades/grado-lenguas-modernas-sus-literaturas",
    "Filología Hispánica": "https://grados.ugr.es/ramas/artes-humanidades/grado-filologia-hispanica",
    "Filología Clásica": "https://grados.ugr.es/ramas/artes-humanidades/grado-filologia-clasica"
}

# FORZAR USER-AGENT DE ESCRITORIO (Windows Chrome)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_subjects_v5(degree_name, url):
    print(f"   📖 Procesando (Desktop Mode): {degree_name}")
    subjects = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200: return []
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # 1. Localizar el índice (Solo existe en Desktop)
        index_div = soup.find('div', class_='indice-contenido')
        if not index_div:
            print("      ❌ Fallo: No se detectó la versión de escritorio. Abortando.")
            return []

        # 2. Mapear Años desde el índice
        links = index_div.find_all('a', class_='anchor-link')
        for link in links:
            target_id = link.get('href').replace('#', '')
            # Determinar año por el texto o posición
            year_text = link.get_text(strip=True).upper()
            year = 1
            if "SEGUNDO" in year_text: year = 2
            elif "TERCER" in year_text: year = 3
            elif "CUARTO" in year_text: year = 4

            # Encontrar el header del curso
            header = soup.find(id=target_id)
            if not header: continue

            # Buscar tablas hasta el siguiente curso o final
            curr = header.find_next_sibling()
            while curr:
                if curr.name == 'h2' and curr.get('id', '').startswith('contenido'):
                    break
                
                # Encontrar tablas de semestre
                tables = curr.find_all('table', class_='tabla-semestre') if curr.name != 'table' else [curr]
                for table in tables:
                    # Semestre
                    semester = 1
                    caption = table.find('caption')
                    if caption and "SEGUNDO" in caption.get_text().upper():
                        semester = 2
                    
                    # Filas de la tabla
                    rows = table.find_all('tr')
                    for row in rows:
                        td_name = row.find('td', class_='asignatura')
                        if td_name and td_name.find('a'):
                            link_tag = td_name.find('a')
                            name = link_tag.get_text(strip=True)
                            
                            td_type = row.find('td', class_='tipo')
                            type_raw = td_type.get_text(strip=True).upper() if td_type else ""
                            
                            stype = "OP"
                            if any(x in type_raw for x in ["TRONCAL", "BÁSICA", "BASICA"]): stype = "BA"
                            elif "OBLIGATORIA" in type_raw: stype = "OB"

                            guide_url = ""
                            guide_link = row.find('a', href=re.compile(r'guia-docente'))
                            if guide_link:
                                guide_url = guide_link.get('href')
                                if guide_url.startswith('/'): guide_url = BASE_URL + guide_url

                            subjects.append({
                                "name": name,
                                "year": year,
                                "semester": semester,
                                "type": stype,
                                "guide_url": guide_url
                            })
                curr = curr.find_next_sibling()

        return subjects
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return []

def main():
    print("🚜 HARVESTER UGR V5 (DESKTOP UA + TABLAS)...")
    all_data = []

    for name, url in TARGET_DEGREES.items():
        subjects = get_subjects_v5(name, url)
        if subjects:
            all_data.append({
                "university": "Universidad de Granada",
                "degree_name": name,
                "subjects": subjects
            })
            print(f"      ✅ {len(subjects)} asignaturas (con año/semestre) capturadas.")
        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ FIN V5. Archivo: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
