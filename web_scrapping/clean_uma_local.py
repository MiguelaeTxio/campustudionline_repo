import json
import re
import sys
import os
from collections import defaultdict

INPUT_FILE = '/sdcard/Download/uma_sextante_fixed.json'
OUTPUT_FILE = '/sdcard/Download/uma_clean_final.json'

# Lista negra de términos no académicos
BLACKLIST = [
    'trabajo fin', 'tfg', 'tfm', 'prácticas', 'practicum', 'prácticum',
    'visitas', 'laboratorio', 'trabajo de campo', 'rotatorio',
    'reconocimiento', 'movilidad', 'créditos', 'módulo', 'seminario'
]

def clean_degree_name(name):
    # Elimina "Plan 2010", "Plan 2023" y "Graduado/a en"
    clean = re.sub(r'\.?\s*Plan\s*\d{4}', '', name, flags=re.IGNORECASE)
    clean = clean.replace("Graduado/a en ", "").strip()
    return clean

def main():
    print("--- INICIANDO LIMPIEZA UMA ---")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: No existe {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"Registros Brutos: {len(raw_data)}")
    
    # DICCIONARIO PARA AGRUPAR Y DEDUPLICAR
    # Clave: (Nombre Grado Limpio, Nombre Asignatura)
    # Valor: Lista de registros encontrados
    grouped_subjects = defaultdict(list)
    
    stats = {'ruido': 0, 'sin_temario': 0}

    for item in raw_data:
        # 1. Filtro de Ruido (Blacklist)
        name = item.get('name', '').strip()
        if any(bad in name.lower() for bad in BLACKLIST):
            stats['ruido'] += 1
            continue
            
        # 2. Filtro de Contenido (Debe tener temario)
        outline = item.get('course_content_outline', [])
        if not outline:
            stats['sin_temario'] += 1
            continue

        # 3. Limpieza de Grado
        raw_degree = item.get('degree', '')
        clean_degree = clean_degree_name(raw_degree)
        item['degree'] = clean_degree # Actualizamos el registro
        
        # Agrupar
        key = (clean_degree, name)
        grouped_subjects[key].append(item)

    final_list = []
    
    # 4. RESOLUCIÓN DE DUPLICADOS (La Regla del Mínimo)
    for key, candidates in grouped_subjects.items():
        if len(candidates) == 1:
            final_list.append(candidates[0])
        else:
            # Si hay duplicados (mismo nombre exacto en mismo grado),
            # nos quedamos con el del AÑO MÁS BAJO.
            # Esto elimina los "fantasmas" de 4º, 5º, 6º que son copias de 1º.
            best_candidate = min(candidates, key=lambda x: x.get('academic_year', 99))
            final_list.append(best_candidate)

    # Guardar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
        
    print("\n--- RESULTADOS ---")
    print(f"Registros Válidos: {len(final_list)}")
    print(f"Eliminados por Ruido: {stats['ruido']}")
    print(f"Eliminados sin Temario: {stats['sin_temario']}")
    print(f"Duplicados Fantasma Eliminados: {len(raw_data) - len(final_list) - stats['ruido'] - stats['sin_temario']}")
    print(f"Archivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
