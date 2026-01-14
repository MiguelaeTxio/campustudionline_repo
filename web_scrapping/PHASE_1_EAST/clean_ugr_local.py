import json
import os

# --- CONFIGURACIÓN RUTAS ABSOLUTAS ---
INPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
OUTPUT_FILE = "/sdcard/Download/ugr_languages_final.json"

def clean():
    print("🧹 INICIANDO LIMPIEZA QUIRÚRGICA UGR...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No existe {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_data = []
    total_removed = 0

    for entry in data:
        degree_name = entry.get('degree_name')
        subjects = entry.get('subjects', [])
        
        seen_subjects = set()
        unique_subjects = []
        
        for s in subjects:
            # Clave de unicidad: Nombre + URL (normalizados)
            uid = f"{s['name'].strip()}|{s['guide_url'].strip()}"
            
            if uid not in seen_subjects:
                seen_subjects.add(uid)
                # Normalización de campos para el importador
                unique_subjects.append({
                    "name": s['name'].strip(),
                    "year": s.get('year', 1),
                    "semester": s.get('semester'),
                    "type": s.get('type', 'OP'),
                    "guide_url": s['guide_url']
                })
            else:
                total_removed += 1

        if unique_subjects:
            cleaned_data.append({
                "university_code": "UGR",
                "university_name": "Institución Académica de Granada",
                "branch_name": "Artes y Humanidades",
                "degree_name": degree_name,
                "subjects": unique_subjects
            })
            print(f"   ✅ {degree_name}: {len(unique_subjects)} asignaturas únicas.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

    print(f"\n✨ LIMPIEZA FINALIZADA.")
    print(f"   🗑️ Duplicados eliminados: {total_removed}")
    print(f"   📄 Dataset final generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean()
