import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random

# --- CONFIGURACIÓN LOCAL (ANDROID) ---
INPUT_FILE = "/sdcard/Download/us_degrees.json"
OUTPUT_FILE = "/sdcard/Download/us_raw_subjects.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def load_degrees():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encuentra el archivo de entrada: {INPUT_FILE}")
        return []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("items", [])

def extract_subjects_from_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"  [ERROR CONEXIÓN] {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    subjects = []
    tables = soup.find_all('table')

    target_table = None
    
    # 1. Identificar la tabla correcta por sus cabeceras
    for table in tables:
        headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
        # Patrón confirmado en sonda: ['curso', 'código asig.', 'asignatura', 'créditos', 'tipo']
        if "asignatura" in headers and "curso" in headers:
            target_table = table
            break
    
    if not target_table:
        print("  [WARN] No se encontró la tabla de asignaturas.")
        return []

    # 2. Extraer filas
    # Asumimos estructura estándar basada en la sonda:
    # 0: Curso, 1: Código, 2: Asignatura, 3: Créditos, 4: Tipo
    rows = target_table.find_all('tr')
    for row in rows[1:]: # Saltar cabecera
        cols = row.find_all('td')
        if len(cols) >= 5:
            try:
                subject_data = {
                    "course": cols[0].get_text(strip=True),
                    "code": cols[1].get_text(strip=True),
                    "name": cols[2].get_text(strip=True),
                    "credits": cols[3].get_text(strip=True),
                    "type": cols[4].get_text(strip=True),
                    "link": "" 
                }
                
                # Intentar capturar enlace a la ficha de la asignatura si existe en el nombre
                link_tag = cols[2].find('a')
                if link_tag and 'href' in link_tag.attrs:
                    href = link_tag['href']
                    if href.startswith("/"):
                        subject_data["link"] = f"https://www.us.es{href}"
                    else:
                        subject_data["link"] = href

                subjects.append(subject_data)
            except Exception as e:
                continue

    return subjects

def harvest():
    degrees = load_degrees()
    print(f"--- Iniciando Harvester Intermedio: {len(degrees)} Grados ---")
    
    all_data = []
    
    for i, degree in enumerate(degrees):
        print(f"[{i+1}/{len(degrees)}] Procesando: {degree['name']}")
        
        subjects = extract_subjects_from_url(degree['url'])
        
        entry = {
            "degree_name": degree['name'],
            "degree_url": degree['url'],
            "subjects_count": len(subjects),
            "subjects": subjects
        }
        all_data.append(entry)
        
        print(f"  -> {len(subjects)} asignaturas extraídas.")
        
        # Guardado incremental por seguridad
        if (i + 1) % 5 == 0:
            save_json(all_data)
            print("  [INFO] Guardado parcial realizado.")
        
        # Pausa anti-bloqueo
        time.sleep(random.uniform(1.0, 2.5))

    save_json(all_data)
    print(f"\n--- Proceso Finalizado. Datos en: {OUTPUT_FILE} ---")

def save_json(data):
    output = {
        "university": "Universidad de Sevilla (US)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "degrees_processed": len(data),
        "data": data
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    harvest()
