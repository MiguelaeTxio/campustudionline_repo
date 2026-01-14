# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uja_refiner.py
import json
import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
import time

# Configuración
INPUT_FILE = "uja_raw_data.json"
OUTPUT_FILE = "uja_refined.json"
MAX_WORKERS = 15  # Número de peticiones simultáneas (ajustado para Android)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def parse_subject_details(url):
    """Extrae Curso, Semestre y Tipo de la URL de detalle."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Estrategia: Buscar celdas por texto del encabezado
        data = {
            "year": 1,         # Default
            "semester": None,
            "type": "OB"       # Default
        }
        
        # Buscar todas las celdas de cabecera (th o td con clase label tal vez, o por texto directo)
        # En la captura se ven celdas normales. Buscamos por texto en td.
        
        # 1. CURSO
        curso_label = soup.find(lambda tag: tag.name == "td" and "Curso:" in tag.get_text())
        if not curso_label:
            # Intento alternativo: buscar en th
            curso_label = soup.find(lambda tag: tag.name == "th" and "Curso:" in tag.get_text())
            
        if curso_label:
            # El valor suele estar en el siguiente td
            curso_val_td = curso_label.find_next_sibling('td')
            if curso_val_td:
                try:
                    text = curso_val_td.get_text(strip=True)
                    # A veces pone "4" o "4º". Extraer digitos.
                    digits = ''.join(filter(str.isdigit, text))
                    if digits:
                        data["year"] = int(digits)
                except:
                    pass

        # 2. CUATRIMESTRE
        cuatri_label = soup.find(lambda tag: tag.name == "td" and "Cuatrimestre" in tag.get_text())
        if cuatri_label:
            cuatri_val_td = cuatri_label.find_next_sibling('td')
            if cuatri_val_td:
                text = cuatri_val_td.get_text(strip=True).upper()
                if "PRIMER" in text:
                    data["semester"] = 1
                elif "SEGUNDO" in text:
                    data["semester"] = 2
                elif "ANUAL" in text:
                    data["semester"] = None # O tratar como especial

        # 3. TIPO
        tipo_label = soup.find(lambda tag: tag.name == "td" and "Tipo:" in tag.get_text())
        if tipo_label:
            tipo_val_td = tipo_label.find_next_sibling('td')
            if tipo_val_td:
                text = tipo_val_td.get_text(strip=True).upper()
                if "BÁSICA" in text or "BASICA" in text:
                    data["type"] = "BA"
                elif "OBLIGATORIA" in text:
                    data["type"] = "OB"
                elif "OPTATIVA" in text:
                    data["type"] = "OP"
                elif "TRONCAL" in text:
                    data["type"] = "TR"

        return data

    except Exception as e:
        return None

def process_subject(subject):
    """Procesa una asignatura individual (para el ThreadPool)."""
    url = subject.get('guide_url')
    if not url:
        return subject
    
    details = parse_subject_details(url)
    if details:
        subject.update(details)
        # print(f"   ✅ {subject['code']} -> Año {details['year']}")
    else:
        # print(f"   ⚠️ Fallo en detalle: {subject['code']}")
        pass
        
    return subject

def refine():
    print("💎 INICIANDO REFINERÍA UJA (Multihilo)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Falta {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_degrees = len(data)
    total_subjects_count = sum(len(d['subjects']) for d in data)
    print(f"📦 Carga: {total_degrees} titulaciones, {total_subjects_count} asignaturas.")
    print(f"🚀 Motores: {MAX_WORKERS} hilos simultáneos.")

    start_time = time.time()
    processed_count = 0

    # Iterar titulaciones
    for i, degree in enumerate(data):
        subjects = degree.get('subjects', [])
        if not subjects: continue

        print(f"\n[{i+1}/{total_degrees}] Refinando: {degree['degree_code']}")
        
        # Procesamiento paralelo de las asignaturas de ESTA titulación
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Map devuelve los resultados en el orden original
            refined_subjects = list(executor.map(process_subject, subjects))
        
        degree['subjects'] = refined_subjects
        processed_count += len(refined_subjects)
        
        # Guardado parcial cada 5 titulaciones para no perder datos si se cancela
        if i % 5 == 0:
             with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    # Guardado Final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    elapsed = time.time() - start_time
    print(f"\n✨ REFINADO COMPLETO en {elapsed:.2f} segundos.")
    print(f"📄 Resultado: {OUTPUT_FILE}")

if __name__ == "__main__":
    refine()
