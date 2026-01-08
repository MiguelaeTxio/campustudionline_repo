import json
import os

# Colores para la consola
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

FILE = '/sdcard/Download/uma_sextante_fixed.json'

def audit():
    print("--- AUDITORÍA DE INTEGRIDAD: BUSCANDO ASIGNATURA '101' ---")
    
    if not os.path.exists(FILE):
        print(f"Error: No encuentro el archivo {FILE}")
        return

    try:
        with open(FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error leyendo JSON: {e}")
        return

    # 1. Agrupar asignaturas por Grado
    degrees = {}
    for item in data:
        deg = item.get('degree', 'Desconocido')
        if deg not in degrees:
            degrees[deg] = []
        degrees[deg].append(item)

    print(f"Analizando {len(degrees)} grados encontrados...\n")

    count_ok = 0
    count_fail = 0

    # 2. Buscar la asignatura 101 en cada grado
    for deg_name, subjects in sorted(degrees.items()):
        found_101 = None
        
        for s in subjects:
            url = s.get('url_source', '')
            # Buscamos el patrón estricto del ID terminando en -101
            # Ej: ...P3_ID:171963-5158-101
            if url.strip().endswith('-101'):
                found_101 = s['name']
                break
        
        if found_101:
            # Si existe, mostramos OK (opcionalmente acortamos el nombre del grado para legibilidad)
            print(f"{GREEN}[OK]{RESET} {deg_name[:50]}... -> Asig: {found_101}")
            count_ok += 1
        else:
            # Si NO existe, ROJO
            print(f"{RED}[FALTA 101] {deg_name}{RESET}")
            count_fail += 1

    print(f"\n--- RESUMEN ---")
    print(f"Grados Correctos (Tienen la 101): {count_ok}")
    print(f"Grados Rotos (Les falta la 101): {count_fail}")

if __name__ == '__main__':
    audit()
