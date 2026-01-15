# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/PHASE_2_WEST/us_final_refiner.py
import json
import os
import time

INPUT_FILE = "/sdcard/Download/us_final_data_enriched.json"
OUTPUT_FILE = "/sdcard/Download/us_dataset_FINAL.json"

def refine():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encuentra: {INPUT_FILE}")
        return

    print("--- Refinando Dataset Final: Sevilla ---")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data_root = json.load(f)

    final_data = {
        "university": "Institución Académica de Sevilla",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_degrees": 0,
        "total_subjects": 0,
        "data": []
    }

    stats = {"removed_empty": 0, "removed_practices": 0, "kept": 0}

    for degree in data_root.get("data", []):
        new_subjects = []
        for sub in degree.get("subjects", []):
            name_lower = sub.get("name", "").lower()
            has_content = len(sub.get("learning_objectives", [])) > 0 or len(sub.get("course_content_outline", [])) > 0
            
            # 1. Filtro de Contenido (Eliminar vacíos)
            if not has_content:
                stats["removed_empty"] += 1
                continue
            
            # 2. Filtro de Prácticas Residuales
            if "prácticas de empresa" in name_lower or "prácticas en empresa" in name_lower or "practicas de empresa" in name_lower:
                stats["removed_practices"] += 1
                continue

            # Asignatura válida
            new_subjects.append(sub)
            stats["kept"] += 1

        if new_subjects:
            degree["subjects"] = new_subjects
            degree["subjects_count"] = len(new_subjects)
            final_data["data"].append(degree)

    final_data["total_degrees"] = len(final_data["data"])
    final_data["total_subjects"] = stats["kept"]

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print("\n=== RESUMEN DE REFINAMIENTO FINAL ===")
    print(f"Asignaturas conservadas: {stats['kept']}")
    print(f"Eliminadas por vacío:    {stats['removed_empty']} (UGR/UJA/UPO/Otros)")
    print(f"Eliminadas (Prácticas):  {stats['removed_practices']}")
    print(f"Archivo FINAL generado:  {OUTPUT_FILE}")

if __name__ == "__main__":
    refine()
