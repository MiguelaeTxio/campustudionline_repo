import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

# --- CONFIGURACIÓN ESTRICTA ANDROID ---
OUTPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
DEBUG_FILE = "/sdcard/Download/debug_ugr.html"
BASE_URL = "https://grados.ugr.es"

TARGET_DEGREES = {
    "Estudios Árabes e Islámicos": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-arabes-islamicos",
    "Estudios Franceses": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-franceses",
    "Estudios Ingleses": "https://grados.ugr.es/ramas/artes-humanidades/grado-estudios-ingleses",
    "Lenguas Modernas y sus Literaturas": "https://grados.ugr.es/ramas/artes-humanidades/grado-lenguas-modernas-sus-literaturas",
    "Filología Hispánica": "https://grados.ugr.es/ramas/artes-humanidades/grado-filologia-hispanica",
    "Filología Clásica": "https://grados.ugr.es/ramas/artes-humanidades/grado-filologia-clasica"
}

# Cabeceras completas para simular navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def get_subjects_v6(degree_name, url):
    print(f"   📖 Analizando: {degree_name}")
    subjects = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
        if r.status_code != 200: return []
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Guardar una muestra del primer grado para depuración si el anterior falló
        if not os.path.exists(DEBUG_FILE):
            with open(DEBUG_FILE, "w", encoding="utf-8") as df:
                df.write(soup.prettify())

        # ESTRATEGIA: Buscar todos los elementos que contengan texto de "Curso"
        # La UGR usa <h2> o <div> según la versión
        potential_headers = soup.find_all(re.compile(r'h[1-4]'), text=re.compile(r'curso', re.IGNORECASE))
        
        if not potential_headers:
            # Si no hay headers, probamos buscar por IDs contenido0, contenido1...
            potential_headers = [soup.find(id=f"contenido{i}") for i in range(5)]
            potential_headers = [h for h in potential_headers if h]

        for header in potential_headers:
            # Determinar Año
            h_text = header.get_text().upper()
            year = 1
            if "SEGUNDO" in h_text: year = 2
            elif "TERCER" in h_text: year = 3
            elif "CUARTO" in h_text: year = 4
            
            # Buscar tablas hasta el próximo header de curso
            curr = header.find_next_sibling()
            while curr:
                # Si encontramos otro header de curso, paramos
                if curr.name in ['h1', 'h2', 'h3'] and "CURSO" in curr.get_text().upper():
                    break
                
                # Buscar tablas en este bloque
                tables = curr.find_all('table') if curr.name != 'table' else [curr]
                for table in tables:
                    # Determinar Semestre
                    semester = 1
                    caption = table.find('caption')
                    if caption and "SEGUNDO" in caption.get_text().upper():
                        semester = 2
                    
                    # Parsear Filas
                    rows = table.find_all('tr')
                    for row in rows:
                        td_name = row.find('td', class_='asignatura') or row.find('td')
                        link_tag = td_name.find('a') if td_name else None
                        
                        if link_tag:
                            subj_name = link_tag.get_text(strip=True)
                            if not subj_name or len(subj_name) < 3: continue
                            
                            # Tipo
                            td_type = row.find('td', class_='tipo')
                            type_raw = td_type.get_text(strip=True).upper() if td_type else ""
                            stype = "OP"
                            if any(x in type_raw for x in ["TRONCAL", "BÁSICA", "BASICA"]): stype = "BA"
                            elif "OBLIGATORIA" in type_raw: stype = "OB"

                            # URL Guía
                            guide_link = row.find('a', href=re.compile(r'guia-docente'))
                            g_url = guide_link.get('href') if guide_link else ""
                            if g_url.startswith('/'): g_url = BASE_URL + g_url

                            subjects.append({
                                "name": subj_name,
                                "year": year,
                                "semester": semester,
                                "type": stype,
                                "guide_url": g_url
                            })
                curr = curr.find_next_sibling()

        return subjects
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return []

def main():
    print("🚀 HARVESTER UGR V6 (MÁXIMA RESILIENCIA)...")
    all_data = []

    for name, url in TARGET_DEGREES.items():
        subjects = get_subjects_v6(name, url)
        if subjects:
            all_data.append({
                "university": "Universidad de Granada",
                "degree_name": name,
                "subjects": subjects
            })
            print(f"      ✅ {len(subjects)} asignaturas capturadas con éxito.")
        else:
            print(f"      ⚠️ No se capturaron asignaturas en {name}.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ FIN V6. Archivo: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
