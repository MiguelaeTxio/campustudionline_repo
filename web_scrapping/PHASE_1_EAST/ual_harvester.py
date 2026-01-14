# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/ual_harvester.py
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re

"""
HARVESTER UAL - EXTRACCIÓN INTEGRAL
-----------------------------------
Flujo:
1. Mapea Ramas y Grados desde la página principal.
2. Itera por cada Grado extrayendo el Plan de Estudios (Asignaturas).
3. Genera ual_raw_data.json estructurado para importación.
"""

BASE_URL = "https://www.ual.es"
CATALOG_URL = "https://www.ual.es/estudios/grados"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_soup(url):
    try:
        print(f"Solicitando: {url}")
        time.sleep(random.uniform(1.0, 2.0))
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error en {url}: {e}")
        return None

def parse_study_plan(degree_id):
    url = f"{BASE_URL}/estudios/grados/presentacion/plandeestudios/{degree_id}"
    soup = get_soup(url)
    if not soup:
        return []

    subjects = []
    # Las asignaturas están agrupadas por bloques de curso/cuatrimestre
    blocks = soup.find_all('div', class_='row20')
    
    current_year = 0
    current_semester = 0

    for block in blocks:
        # Detectar Curso y Cuatrimestre en el H4
        h4 = block.find('h4')
        if h4:
            header_text = h4.get_text(strip=True)
            # Extraer año (ej: "1º Curso")
            year_match = re.search(r'(\d+)º', header_text)
            if year_match:
                current_year = int(year_match.group(1))
            
            # Extraer cuatrimestre o anualidad
            if "1º Cuatrimestre" in header_text:
                current_semester = 1
            elif "2º Cuatrimestre" in header_text:
                current_semester = 2
            elif "Anual" in header_text:
                current_semester = 0 # 0 representará anual en nuestro sistema

        # Buscar tablas de asignaturas en este bloque
        table = block.find('table')
        if not table:
            continue

        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                subjects.append({
                    "code": cols[0].get_text(strip=True),
                    "name": cols[1].find('a').get_text(strip=True) if cols[1].find('a') else cols[1].get_text(strip=True),
                    "ects": cols[2].get_text(strip=True),
                    "type": cols[3].get_text(strip=True),
                    "year": current_year,
                    "semester": current_semester
                })
    
    return subjects

def run_harvester():
    print("--- Iniciando Harvester UAL ---")
    soup = get_soup(CATALOG_URL)
    if not soup: return

    final_data = []
    # Buscar ramas (h2) y sus listas (ul)
    branches = soup.find_all('h2')
    
    for branch_node in branches:
        branch_name = branch_node.get_text(strip=True)
        print(f"\nProcesando Rama: {branch_name}")
        
        ul = branch_node.find_next_sibling('ul')
        if not ul: continue

        links = ul.find_all('a')
        for link in links:
            degree_name = link.get_text(strip=True)
            href = link.get('href', '')
            
            # Extraer ID del final de la URL
            match = re.search(r'/(\d+)$', href)
            if not match: continue
            degree_id = match.group(1)

            print(f"  > Extrayendo Grado: {degree_name} (ID: {degree_id})")
            
            subjects = parse_study_plan(degree_id)
            
            final_data.append({
                "university_name": "Universidad de Almería",
                "university_code": "UAL",
                "branch": branch_name,
                "degree_name": degree_name,
                "degree_code": degree_id,
                "subjects": subjects
            })

    with open('ual_raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n--- Proceso finalizado. {len(final_data)} grados guardados en ual_raw_data.json ---")

if __name__ == "__main__":
    run_harvester()
