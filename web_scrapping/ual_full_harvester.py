import requests
import json
import time
import os
import urllib3
import re

# Configuración
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL_GRADOS = "https://campus.ual.es/ual/api/estudios/planes/titulaciones/GRA/es"
URL_ASIGNATURAS_BASE = "https://campus.ual.es/webual/json/academica/bAsignaturasJSON.jsp"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.ual.es/"
}

# Mapeo de Tipos de Asignatura al Modelo Django
TYPE_MAP = {
    "Básica": "BA",
    "Obligatoria": "OB",
    "Optativa": "OP",
    "Troncal": "TR",
    "Trabajo Fin De Grado": "OB", # Tratamos TFG como obligatoria especial o definimos OT
    "Prácticas Externas": "OB"
}

def clean_year(year_str):
    """Convierte '1º' a 1"""
    match = re.search(r'\d+', str(year_str))
    return int(match.group()) if match else 1

def clean_semester(sem_str):
    """Convierte '1Q' a 1, '2Q' a 2, 'A' a None"""
    if "1Q" in sem_str: return 1
    if "2Q" in sem_str: return 2
    return None # Anual

def fetch_json(url, params=None):
    try:
        resp = requests.get(url, params=params, headers=HEADERS, verify=False, timeout=20)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"    [Error] {e}")
    return None

def run_full_harvest():
    print("--- UAL FULL HARVESTER STARTED ---")
    
    # 1. Obtener Grados
    print("[1/3] Descargando lista maestra de Grados...")
    grados_data = fetch_json(URL_GRADOS)
    
    if not grados_data or 'planes' not in grados_data:
        print("CRITICAL: No se pudo obtener la lista de grados.")
        return

    # Estructura final
    university_data = {
        "code": "UAL",
        "name": "Universidad de Almería",
        "branches": {} 
    }

    planes = grados_data['planes']
    total_planes = len(planes)
    print(f"      -> {total_planes} grados encontrados.")

    # 2. Procesar Grados y Ramas
    for idx, plan in enumerate(planes):
        branch_name = plan['nom_rama']
        degree_id = plan['cod_plan']
        degree_name = plan['nom_plan']
        
        print(f"[2/3] ({idx+1}/{total_planes}) Procesando: {degree_name[:40]}...")

        # Inicializar rama si no existe
        if branch_name not in university_data['branches']:
            university_data['branches'][branch_name] = []

        # Estructura del Grado
        degree_obj = {
            "code": degree_id,
            "name": degree_name,
            "subjects": []
        }

        # 3. Obtener Asignaturas del Grado
        subjects_payload = fetch_json(URL_ASIGNATURAS_BASE, {"idTit": degree_id, "idioma": "es"})
        
        if subjects_payload and 'asignaturas' in subjects_payload:
            # La estructura es asignaturas -> lista de cursos -> lista de asignaturas
            for curso_wrapper in subjects_payload['asignaturas']:
                # A veces viene como lista de un solo objeto 'curso'
                if isinstance(curso_wrapper, dict) and 'curso' in curso_wrapper:
                    # El wrapper interno que contiene el nombre del curso y el array real
                    inner_courses = curso_wrapper['curso'] 
                    if isinstance(inner_courses, list):
                        for c_info in inner_courses:
                            year_int = clean_year(c_info.get('curso', '1'))
                            semester_int = clean_semester(c_info.get('cuatrimestre', 'A'))
                            
                            # Lista real de asignaturas
                            for subj in c_info.get('asignaturas', []):
                                # Filtro: Solo asignaturas vigentes/ofertadas
                                if subj.get('ofertada') == 'S' or subj.get('estado_ass') == 'V':
                                    s_type = TYPE_MAP.get(subj.get('nom_caracter'), "OT")
                                    
                                    degree_obj['subjects'].append({
                                        "code": subj['cod_ass'],
                                        "name": subj['nom_ass'],
                                        "ects": subj.get('cred_ects', 0),
                                        "year": year_int,
                                        "semester": semester_int,
                                        "type": s_type,
                                        "raw_type": subj.get('nom_caracter')
                                    })
        
        university_data['branches'][branch_name].append(degree_obj)
        time.sleep(0.5) # Cortesía

    # 4. Guardar Resultado Final
    print("[3/3] Guardando datos estructurados...")
    final_file = "ual_final_data.json"
    with open(final_file, "w", encoding="utf-8") as f:
        json.dump(university_data, f, ensure_ascii=False, indent=2)
    
    print(f"--- SUCCESS ---")
    print(f"Data saved to: {os.path.abspath(final_file)}")

if __name__ == "__main__":
    run_full_harvest()
