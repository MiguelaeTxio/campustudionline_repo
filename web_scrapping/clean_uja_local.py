import json
import re
import os

# --- RUTAS ABSOLUTAS ANDROID ---
INPUT_FILE = "/sdcard/Download/uja_refined.json"
OUTPUT_FILE = "/sdcard/Download/uja_final_data.json"

BLACKLIST_PHRASES = [
    "trabajo fin de grado", "trabajo fin de máster", "trabajo fin máster", "master thesis",
    "prácticas externas", "prácticas de empresa", "prácticas en empresa",
    "prácticas en instituciones", "prácticas docentes", "prácticas curriculares",
    "prácticum", "practicum"
]

def clean_data():
    print("🧹 LIMPIEZA UJA (ABSOLUTE PATHS)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ No existe {INPUT_FILE}. Ejecuta el refinador primero.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_degrees = []
    
    for degree_entry in data:
        valid_subjects = []
        d_name_raw = degree_entry.get('degree', degree_entry.get('degree_name', ''))
        degree_name = re.sub(r'\s*\(\d+[A-Z]+\)$', '', d_name_raw).strip()
        
        center = degree_entry.get('center', degree_entry.get('center_name', ''))
        branch = "Otras Ramas"
        if "POLITÉCNICA" in center or "Ingeniería" in degree_name: branch = "Ingeniería y Arquitectura"
        elif "SALUD" in center or "Enfermería" in degree_name: branch = "Ciencias de la Salud"
        elif "SOCIALES" in center or "Derecho" in degree_name or "ADE" in degree_name: branch = "Ciencias Sociales y Jurídicas"
        elif "HUMANIDADES" in center: branch = "Artes y Humanidades"
        elif "EXPERIMENTALES" in center: branch = "Ciencias"

        for subject in degree_entry.get('subjects', []):
            name = subject['name'].strip()
            name_lower = name.lower()
            is_banned = False
            for phrase in BLACKLIST_PHRASES:
                if phrase in name_lower:
                    is_banned = True
                    break
            if name_lower == "proyecto": is_banned = True

            if not is_banned:
                subject_clean = {
                    "code": subject.get('code', ''),
                    "name": name,
                    "year": subject.get('year', 1),
                    "semester": subject.get('semester'),
                    "type": subject.get('type', 'OB'),
                    "credits": 6.0,
                    "guide_url": subject.get('guide_url', '')
                }
                valid_subjects.append(subject_clean)

        if valid_subjects:
            cleaned_degrees.append({
                "university_code": "UJA",
                "university_name": "Institución Académica de Jaén",
                "center_name": center,
                "branch_name": branch,
                "degree_name": degree_name,
                "degree_code": degree_entry.get('degree_code', ''),
                "subjects": valid_subjects
            })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_degrees, f, indent=4, ensure_ascii=False)

    print(f"✅ LIMPIEZA COMPLETADA. Archivo: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_data()
