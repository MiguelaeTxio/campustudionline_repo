# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uja_keyword_auditor.py
import json
import os
from collections import Counter

# Configuración
INPUT_FILE = "uja_raw_data.json"
KEYWORDS = [
    "trabajo", 
    "práctica", "practica", "pràctica", "practicum", 
    "proyecto", 
    "visita", 
    "traslado"
]

def audit():
    print("🔍 AUDITORÍA DE PALABRAS CLAVE - UJA")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ No se encuentra el archivo {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Almacén de hallazgos: {keyword: Counter(full_subject_name)}
    findings = {k: Counter() for k in KEYWORDS}
    
    total_subjects = 0
    
    for degree in data:
        for subject in degree.get('subjects', []):
            total_subjects += 1
            name_lower = subject['name'].lower()
            
            for keyword in KEYWORDS:
                if keyword in name_lower:
                    findings[keyword].update([subject['name']])

    # Reporte
    print(f"📊 Total Asignaturas Analizadas: {total_subjects}")
    print("-" * 40)
    
    for keyword in KEYWORDS:
        counts = findings[keyword]
        if counts:
            print(f"\n🔑 PALABRA CLAVE: '{keyword.upper()}' ({sum(counts.values())} coincidencias)")
            # Ordenar por frecuencia
            for name, count in counts.most_common():
                print(f"   [{count}] {name}")
        else:
             print(f"\n🔑 PALABRA CLAVE: '{keyword.upper()}' (0 coincidencias)")

if __name__ == "__main__":
    audit()
