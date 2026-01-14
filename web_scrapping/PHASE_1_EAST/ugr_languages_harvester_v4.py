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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def get_subjects_v4(degree_name, url):
    print(f"   📖 Analizando: {degree_name}")
    subjects = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200: return []
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # 1. Encontrar el índice de contenidos para identificar los IDs de los cursos
        index_div = soup.find('div', class_='indice-contenido')
        if not index_div:
            print("      ⚠️ No se encontró índice. Buscando tablas directamente...")
            # Fallback: intentar pillar todas las tablas
            tables = soup.find_all('table', class_='tabla-semestre')
            for table in tables:
                subjects.extend(parse_table(table, 1, 1)) # Default 1/1
            return subjects

        # 2. Mapear IDs de curso del índice
        course_links = index_div.find_all('a', class_='anchor-link')
        for link in course_links:
            target_id = link.get('href').replace('#', '')
            course_text = link.get_text(strip=True)
            
            # Determinar año numérico
            year = 1
            if "SEGUNDO" in course_text.upper(): year = 2
            elif "TERCER" in course_text.upper(): year = 3
            elif "CUARTO" in course_text.upper(): year = 4

            # Encontrar el elemento que tiene ese ID
            section_header = soup.find(id=target_id)
            if not section_header: continue

            # Navegar por los hermanos hasta el siguiente h2 o final
            curr = section_header.find_next_sibling()
            while curr:
                # Si llegamos a otro h2 con ID de curso, paramos este curso
                if curr.name == 'h2' and curr.get('id', '').startswith('contenido'):
                    break
                
                # Buscar tablas dentro de este contenedor
                tables = curr.find_all('table', class_='tabla-semestre') if curr.name != 'table' else [curr]
                for table in tables:
                    # Determinar semestre
                    semester = 1
                    caption = table.find('caption')
                    if caption and "SEGUNDO" in caption.get_text().upper():
                        semester = 2
                    
                    # Extraer asignaturas de la tabla
                    subjects.extend(parse_table(table, year, semester))
                
                curr = curr.find_next_sibling()

        return subjects
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return []

def parse_table(table, year, semester):
    subjs = []
    rows = table.find_all('tr')
    for row in rows:
        td_name = row.find('td', class_='asignatura')
        if td_name and td_name.find('a'):
            link_tag = td_name.find('a')
            name = link_tag.get_text(strip=True)
            
            td_type = row.find('td', class_='tipo')
            type_raw = td_type.get_text(strip=True).upper() if td_type else ""
            
            stype = "OP"
            if "TRONCAL" in type_raw or "BÁSICA" in type_raw or "BASICA" in type_raw: stype = "BA"
            elif "OBLIGATORIA" in type_raw: stype = "OB"

            # Buscar link de la guía docente
            guide_url = ""
            guide_link = row.find('a', href=re.compile(r'guia-docente'))
            if guide_link:
                guide_url = guide_link.get('href')
                if guide_url.startswith('/'): guide_url = BASE_URL + guide_url

            subjs.append({
                "name": name,
                "year": year,
                "semester": semester,
                "type": stype,
                "guide_url": guide_url
            })
    return subjs

def main():
    print("🚀 INICIANDO RECONSTRUCCIÓN UGR V4 (ESTRATEGIA ÍNDICE)...")
    all_data = []

    for name, url in TARGET_DEGREES.items():
        subjects = get_subjects_v4(name, url)
        if subjects:
            all_data.append({
                "university": "Universidad de Granada",
                "degree_name": name,
                "subjects": subjects
            })
            print(f"      ✅ {len(subjects)} asignaturas capturadas.")
        else:
            print(f"      ❌ Fallo total en {name}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ FIN V4. Datos: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
