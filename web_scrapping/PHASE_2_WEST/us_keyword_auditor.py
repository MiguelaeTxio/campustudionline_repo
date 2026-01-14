import json
import os
from collections import defaultdict

INPUT_FILE = "/sdcard/Download/us_raw_subjects.json"

# Palabras clave sospechosas a auditar
KEYWORDS = [
    "Trabajo", "Práctica", "Practica", "Prácticum", "Practicum", 
    "Externas", "Rotatorio", "Proyecto", "TFG", "Fin de Grado"
]

def audit():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encuentra: {INPUT_FILE}")
        return

    print("--- Cargando datos... ---")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Estructura para contadores y ejemplos
    # { "Trabajo": { "starts": {"count": 0, "examples": set()}, "contains": ... } }
    stats = {k: {"starts": [], "ends": [], "contains": []} for k in KEYWORDS}
    
    total_subjects = 0
    
    for degree in data.get("data", []):
        for subject in degree.get("subjects", []):
            name = subject.get("name", "")
            total_subjects += 1
            
            for k in KEYWORDS:
                if k.lower() in name.lower():
                    # Clasificación por posición
                    if name.lower().startswith(k.lower()):
                        stats[k]["starts"].append(name)
                    elif name.lower().endswith(k.lower()):
                        stats[k]["ends"].append(name)
                    else:
                        stats[k]["contains"].append(name)

    print(f"\n=== REPORTE DE AUDITORÍA ({total_subjects} asignaturas analizadas) ===")
    
    for k in KEYWORDS:
        s = stats[k]
        total_k = len(s["starts"]) + len(s["ends"]) + len(s["contains"])
        
        if total_k == 0:
            continue
            
        print(f"\n🔸 PALABRA CLAVE: '{k}' (Total: {total_k})")
        
        if s["starts"]:
            print(f"   ↳ Empieza con '{k}' ({len(s['starts'])}):")
            # Mostrar hasta 3 ejemplos únicos
            examples = list(set(s["starts"]))[:3]
            print(f"      Ej: {', '.join(examples)}")
            
        if s["ends"]:
            print(f"   ↳ Termina en '{k}' ({len(s['ends'])}):")
            examples = list(set(s["ends"]))[:3]
            print(f"      Ej: {', '.join(examples)}")
            
        if s["contains"]:
            print(f"   ↳ Contiene '{k}' ({len(s['contains'])}):")
            examples = list(set(s["contains"]))[:5]
            print(f"      Ej: {', '.join(examples)}")

if __name__ == "__main__":
    audit()
