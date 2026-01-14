import requests
from bs4 import BeautifulSoup
import json
import time
import unicodedata
import sys
import os
from urllib.parse import urljoin

# --- CONFIGURACIÓN ---
OUTPUT_FILE = 'uco_master_map.json'

# --- DATOS DE ENTRADA (Mismos que V19.2) ---
DATA_SOURCE = [
    {"degree": "Grado en Veterinaria", "candidates": ["https://www.uco.es/organiza/centros/veterinaria/es/planificacion-de-la-ensenanza"]},
    {"degree": "Grado en Ciencia y Tecnología de los Alimentos", "candidates": ["https://www.uco.es/organiza/centros/veterinaria/es/planificacion-ensenanza-cyta"]},
    {"degree": "Grado en Nutrición Humana y Dietética", "candidates": ["https://www.uco.es/organiza/centros/veterinaria/es/planificacion-nutricion"]},
    {"degree": "Grado en Ingeniería Agroalimentaria y del Medio Rural", "candidates": ["https://www.uco.es/etsiam/es/planificacion-guias-agroalimentaria"]},
    {"degree": "Grado en Ingeniería Forestal", "candidates": ["https://www.uco.es/etsiam/es/planificacion-guias-forestal"]},
    {"degree": "Grado en Enología", "candidates": ["https://www.uco.es/etsiam/es/planificacion-guias-enologia"]},
    {"degree": "Grado en Enfermería", "candidates": ["https://www.uco.es/organiza/centros/medicinayenfermeria/es/planificacion-de-la-ensenanza-enf"]},
    {"degree": "Grado en Fisioterapia", "candidates": ["https://www.uco.es/organiza/centros/medicinayenfermeria/es/planificacion-ensenanza-fis"]},
    {"degree": "Grado en Medicina", "candidates": ["https://www.uco.es/medicinayenfermeria/es/planificacion-ensenanza-med"]},
    {"degree": "Grado en Biología", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-de-la-ensenanza"]},
    {"degree": "Grado en Bioquímica", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-bioquimica"]},
    {"degree": "Grado en Biotecnología", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-biotecnologia"]},
    {"degree": "Grado en Ciencias Ambientales", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-ambientales"]},
    {"degree": "Grado en Física", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-fisica"]},
    {"degree": "Grado en Química", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-quimica"]},
    {"degree": "Grado en Matemáticas y Filosofía", "candidates": ["https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-matematicas-filosofia"]},
    {"degree": "Grado en Cine y Cultura", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-cine-y-cultura#planificacion"]},
    {"degree": "Grado en Cine y Cultura (No Presencial)", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-cine-y-cultura-no-presencial#planificacion"]},
    {"degree": "Grado en Estudios Ingleses", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-estudios-ingleses#planificacion"]},
    {"degree": "Grado en Filología Hispánica", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-filologia-hispanica#planificacion"]},
    {"degree": "Grado en Gestión Cultural", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-gestion-cultural#planificacion"]},
    {"degree": "Grado en Historia", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-historia#planificacion"]},
    {"degree": "Grado en Historia del Arte", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-historia-del-arte#planificacion"]},
    {"degree": "Grado en Traducción e Interpretación", "candidates": ["https://www.uco.es/filosofiayletras/es/grados/gr-traduccion-e-interpretacion#planificacion"]},
    {"degree": "Grado en Derecho", "candidates": ["https://www.uco.es/organiza/centros/derecho/es/planificacion-de-la-ensenanza-derecho.html"]},
    {"degree": "Grado en Administración y Dirección de Empresas (ADE)", "candidates": ["https://www.uco.es/organiza/centros/derecho/es/planificacion-de-la-ensenanza-ade.html"]},
    {"degree": "Grado en Educación Infantil", "candidates": ["https://www.uco.es/educacion/es/infantil-planificacion-de-la-ensenanza"]},
    {"degree": "Grado en Educación Primaria", "candidates": ["https://www.uco.es/educacion/es/primaria-planificacion-de-la-ensenanza"]},
    {"degree": "Grado en Educación Social", "candidates": ["https://www.uco.es/educacion/es/social-planificacion-de-las-ensenanzas"]},
    {"degree": "Grado en Psicología", "candidates": ["https://www.uco.es/educacion/es/gpsicologia-planificacion-ps-planifica"]},
    {"degree": "Grado en Ingeniería Eléctrica", "candidates": ["https://www.uco.es/eps/es/programas-de-asignaturas"]},
    {"degree": "Grado en Ingeniería Electrónica Industrial", "candidates": ["https://www.uco.es/eps/es/programas-de-asignaturas"]},
    {"degree": "Grado en Ingeniería Mecánica", "candidates": ["https://www.uco.es/eps/es/programas-de-asignaturas"]},
    {"degree": "Grado en Ingeniería Informática", "candidates": ["https://www.uco.es/eps/es/programas-de-asignaturas"]},
    {"degree": "Grado en Relaciones Laborales y Recursos Humanos", "candidates": ["https://www.uco.es/trabajo/es/grelacioneslaborales-planificacion"]},
    {"degree": "Grado en Turismo", "candidates": ["https://www.uco.es/trabajo/es/gturismo-planificacion"]},
    {"degree": "Grado en Ingeniería Civil", "candidates": ["https://www.uco.es/organiza/centros/EPSBelmez/es/planificacion-ensenanza-ing-civil"]},
    {"degree": "Grado en Ingeniería de la Energía y Recursos Minerales", "candidates": ["https://www.uco.es/organiza/centros/EPSBelmez/es/planificacion-ensenanza-ing-energia-recursos-minerales"]},
]

# --- MAPEO DE AÑOS ---
YEAR_MAPPING = {
    'primer': 1, 'primero': 1, '1': 1, '1º': 1,
    'segundo': 2, '2': 2, '2º': 2,
    'tercer': 3, 'tercero': 3, '3': 3, '3º': 3,
    'cuarto': 4, '4': 4, '4º': 4,
    'quinto': 5, '5': 5, '5º': 5,
    'sexto': 6, '6': 6, '6º': 6
}

# --- FILTROS ---
EXCLUDED_TERMS = [
    'trabajo fin de grado', 'tfg',
    'prácticas externas', 'practicas externas',
    'optatividad', 'reconocimiento', 'créditos',
    'tmb', 'transversal',
    '(bilingüe)', 'grupo bilingüe', 'english group', 'itinerario'
]

PROTECTED_TERMS = [
    'trabajo social', 'derecho del trabajo', 'seguridad social'
]

def clean_text(text):
    if not text: return ""
    text = unicodedata.normalize("NFKC", text)
    return text.strip()

def is_valid_subject(name):
    name_lower = name.lower()
    for protected in PROTECTED_TERMS:
        if protected in name_lower: return True
    for excluded in EXCLUDED_TERMS:
        if excluded in name_lower: return False
    if len(name) < 4: return False
    # Filtro extra: Si el nombre contiene palabras clave de temporalidad, probablemente es un error
    if "cuatrimestre" in name_lower or "trimestre" in name_lower or "anual" in name_lower:
        # Solo si no es una asignatura "Anual" legítima (raro como nombre único)
        if len(name) < 20: # "1er cuatrimestre" es corto
            return False
    return True

def parse_year(panel_title):
    text = clean_text(panel_title).lower()
    for key, value in YEAR_MAPPING.items():
        if key in text: return value
    return None

def extract_from_url(degree_name, url):
    print(f"    Intentando: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"      [X] Fallo: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    subjects = []
    
    potential_containers = soup.find_all(['div', 'h3', 'h4', 'a'], string=True)
    year_nodes = []
    for node in potential_containers:
        text = node.get_text(strip=True)
        if len(text) < 60 and parse_year(text):
             if node.name in ['h3', 'h4'] or 'panel-title' in str(node.get('class', [])) or 'accordion' in str(node.get('class', [])):
                 year_nodes.append(node)
             elif node.name == 'a' and ('collapse' in str(node.get('data-toggle', '')) or 'collapse' in str(node.get('href', ''))):
                 year_nodes.append(node)

    processed_years = set()
    for node in year_nodes:
        year_text = node.get_text(strip=True)
        year = parse_year(year_text)
        if not year or year in processed_years: continue
            
        table = None
        parent_panel = node.find_parent(class_='panel')
        if parent_panel:
            target_body = parent_panel.find(class_='panel-body')
            if target_body: table = target_body.find('table')
        if not table: table = node.find_next('table')
        if not table: continue
            
        processed_years.add(year)
        rows = table.find_all('tr')
        count_for_year = 0
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if not cells: continue
            
            final_name = ""
            final_url = None
            
            # --- NUEVA ESTRATEGIA: Buscar el enlace (Anchor) ---
            # El nombre de la asignatura SIEMPRE es el texto del enlace a la guía.
            
            links = row.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                text = clean_text(link.get_text())
                
                # Descartar enlaces vacíos o javascript
                if not text or len(text) < 3: continue
                if 'javascript' in href or href.startswith('#'): continue
                if '@' in href or 'mailto:' in href: continue # Ignorar emails
                
                # Si pasa el filtro de asignatura válida, es nuestro candidato
                if is_valid_subject(text):
                    final_name = text
                    final_url = urljoin(url, href)
                    break # Encontramos el principal, salimos de la celda
            
            # Fallback: Si no hay enlace válido, usar lógica antigua (texto largo)
            # pero con filtro estricto de no "cuatrimestre"
            if not final_name:
                max_len = 0
                for cell in cells:
                    cell_text = clean_text(cell.get_text())
                    if len(cell_text) > max_len:
                        if is_valid_subject(cell_text):
                            max_len = len(cell_text)
                            final_name = cell_text

            if final_name and is_valid_subject(final_name):
                # Limpieza final
                final_name = final_name.replace('\n', ' ').strip()
                
                subjects.append({
                    "university": "Universidad de Córdoba",
                    "degree": degree_name,
                    "year": year,
                    "name": final_name,
                    "pdf_url": final_url,
                    "url_source": url
                })
                count_for_year += 1
                
        print(f"      Año {year}: {count_for_year} asignaturas.")

    if not subjects:
        print("      [!] URL válida pero 0 asignaturas.")
        return None
        
    return subjects

def main():
    print("==========================================")
    print("   UCO HARVESTER V19.4 - NAME FIX")
    print("==========================================")
    
    master_list = []
    
    for i, entry in enumerate(DATA_SOURCE):
        degree = entry.get('degree')
        print(f"[{i+1}/{len(DATA_SOURCE)}] {degree} - RE-GENERANDO...")
        candidates = entry.get('candidates', [])
        success = False
        
        for url in candidates:
            results = extract_from_url(degree, url)
            if results:
                master_list.extend(results)
                success = True
                break
            time.sleep(1)
            
        if not success:
            print(f"   [!!!] FALLO TOTAL PARA: {degree}")

    print(f"\nGenerando {OUTPUT_FILE} (V4 Nombres Correctos)...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(master_list, f, ensure_ascii=False, indent=4)
        print(f"SUCCESS. Total asignaturas: {len(master_list)}")
    except Exception as e:
        print(f"Error escribiendo archivo: {e}")

if __name__ == "__main__":
    main()
