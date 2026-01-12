import json
import os

# --- CONFIGURACIÓN ESTRICTA ANDROID ---
INPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
OUTPUT_FILE = "/sdcard/Download/ugr_languages_final.json"

def clean_v2():
    print("🧹 INICIANDO LIMPIEZA UGR V2 (IDENTIDAD COMPLETA)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No existe {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    final_dataset = []
    total_unique = 0
    total_redundant = 0

    for degree_entry in data:
        degree_name = degree_entry.get('degree_name')
        subjects = degree_entry.get('subjects', [])
        
        # Clave de integridad: Nombre completo + Año + URL de la Guía
        seen = set()
        unique_subjects = []
        
        for s in subjects:
            name = s['name'].strip()
            year = s.get('year', 1)
            url = s.get('guide_url', '').strip()
            
            # La huella dactilar de la asignatura
            fingerprint = f"{name}|{year}|{url}"
            
            if fingerprint not in seen:
                seen.add(fingerprint)
                unique_subjects.append({
                    "name": name,
                    "year": year,
                    "semester": s.get('semester'),
                    "type": s.get('type', 'OP'),
                    "guide_url": url
                })
            else:
                total_redundant += 1

        if unique_subjects:
            total_unique += len(unique_subjects)
            final_dataset.append({
                "university_code": "UGR",
                "university_name": "Institución Académica de Granada",
                "branch_name": "Artes y Humanidades",
                "degree_name": degree_name,
                "subjects": unique_subjects
            })
            print(f"   ✅ {degree_name}: {len(unique_subjects)} variantes preservadas.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_dataset, f, indent=4, ensure_ascii=False)

    print(f"\n✨ PROCESO FINALIZADO.")
    print(f"   📊 Variantes únicas totales: {total_unique}")
    print(f"   🗑️ Redundancia eliminada: {total_redundant}")
    print(f"   📄 Dataset listo en: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_v2()
