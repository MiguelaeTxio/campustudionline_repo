# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/PHASE_2_WEST/us_gap_analysis.py
import json
import os

MASTER_FILE = "/sdcard/Download/us_degrees.json"
ENRICHED_FILE = "/sdcard/Download/us_final_data_enriched.json"
REPORT_FILE = "/sdcard/Download/us_missing_report.txt"

def analyze_gaps():
    if not os.path.exists(MASTER_FILE) or not os.path.exists(ENRICHED_FILE):
        print("[ERROR] Faltan archivos de entrada en el directorio de intercambio.")
        return

    print("--- Cruzando listados y detectando vacíos... ---")
    
    with open(MASTER_FILE, 'r', encoding='utf-8') as f:
        master = json.load(f)
    with open(ENRICHED_FILE, 'r', encoding='utf-8') as f:
        enriched = json.load(f)

    master_names = {d['name'] for d in master.get('items', [])}
    enriched_list = enriched.get('data', [])
    enriched_names = {d['degree_name'] for d in enriched_list}

    # 1. Grados que ni siquiera están en el archivo final
    missing_degrees = master_names - enriched_names

    report = []
    report.append("=== INFORME DE INVESTIGACIÓN DE VACÍOS (US) ===")
    report.append(f"Fecha de análisis: {enriched.get('timestamp', 'N/A')}")
    report.append("-" * 50)
    
    report.append(f"\n1. GRADOS TOTALMENTE AUSENTES EN EL RESULTADO ({len(missing_degrees)}):")
    if missing_degrees:
        for d in sorted(missing_degrees):
            report.append(f"   [!] {d}")
    else:
        report.append("   (Ninguno. Todos los grados tienen al menos una entrada)")

    report.append("\n" + "="*50)
    report.append("2. GRADOS CON ASIGNATURAS VACÍAS (SÓLO ESTRUCTURA, SIN CONTENIDO PDF):")
    
    total_empty_subjects = 0
    
    for deg in enriched_list:
        subjects = deg.get('subjects', [])
        # Identificar vacíos: sin objetivos Y sin temario
        empty_subjects = [s for s in subjects if not s.get('learning_objectives') and not s.get('course_content_outline')]
        
        if empty_subjects:
            total_empty_subjects += len(empty_subjects)
            success_rate = ((len(subjects) - len(empty_subjects)) / len(subjects)) * 100
            report.append(f"\n🔹 {deg['degree_name']}")
            report.append(f"   Cobertura: {success_rate:.1f}% ({len(empty_subjects)} de {len(subjects)} vacías)")
            for s in empty_subjects:
                report.append(f"     ↳ [{s['code']}] {s['name']}")

    report.append("\n" + "="*50)
    report.append(f"\nRESUMEN FINAL: {total_empty_subjects} asignaturas sin contenido detallado.")

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Investigación finalizada. Informe generado en: {REPORT_FILE}")

if __name__ == "__main__":
    analyze_gaps()
