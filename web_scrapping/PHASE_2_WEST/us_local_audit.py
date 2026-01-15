# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/PHASE_2_WEST/us_local_audit.py
import json
import os

INPUT_FILE = "/sdcard/Download/us_final_data_enriched.json"

def run_audit():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encuentra el archivo enriquecido en: {INPUT_FILE}")
        return

    print("--- Analizando Calidad de los Datos de Sevilla ---")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data_root = json.load(f)

    total_degrees = data_root.get("degrees_processed", 0)
    data = data_root.get("data", [])

    stats = {
        "total_subjects": 0,
        "with_objectives": 0,
        "with_outline": 0,
        "completely_empty": 0,
        "degrees_with_issues": []
    }

    for degree in data:
        subjects = degree.get("subjects", [])
        degree_name = degree.get("degree_name")
        degree_subjects_count = len(subjects)
        degree_success_count = 0

        for sub in subjects:
            stats["total_subjects"] += 1
            has_obj = len(sub.get("learning_objectives", [])) > 0
            has_out = len(sub.get("course_content_outline", [])) > 0

            if has_obj: stats["with_objectives"] += 1
            if has_out: stats["with_outline"] += 1
            
            if has_obj or has_out:
                degree_success_count += 1
            else:
                stats["completely_empty"] += 1

        if degree_subjects_count > 0 and degree_success_count == 0:
            stats["degrees_with_issues"].append(degree_name)

    # CÁLCULOS
    p_obj = (stats["with_objectives"] / stats["total_subjects"] * 100) if stats["total_subjects"] > 0 else 0
    p_out = (stats["with_outline"] / stats["total_subjects"] * 100) if stats["total_subjects"] > 0 else 0

    print(f"\n=== REPORTE DE CALIDAD: SEVILLA ===")
    print(f"Grados Procesados:    {total_degrees}")
    print(f"Total Asignaturas:    {stats['total_subjects']}")
    print(f"-----------------------------------")
    print(f"Con Objetivos:        {stats['with_objectives']} ({p_obj:.1f}%)")
    print(f"Con Temario:          {stats['with_outline']} ({p_out:.1f}%)")
    print(f"Sin Contenido (PDF):  {stats['completely_empty']}")
    
    if stats["degrees_with_issues"]:
        print(f"\n⚠️ GRADOS CON 0% DE CONTENIDO ({len(stats['degrees_with_issues'])}):")
        for d in stats["degrees_with_issues"][:10]: # Mostrar primeros 10
            print(f"  - {d}")
        if len(stats["degrees_with_issues"]) > 10:
            print(f"  ... y {len(stats['degrees_with_issues']) - 10} más.")
    else:
        print("\n✅ Todos los grados tienen al menos una asignatura con contenido.")

if __name__ == "__main__":
    run_audit()
