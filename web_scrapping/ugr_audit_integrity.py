import json
import os
from collections import Counter

# --- RUTA ABSOLUTA ANDROID ---
INPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"

def audit():
    print("🔬 AUDITORÍA DE INTEGRIDAD Y DUPLICADOS: UGR")
    print("=" * 60)
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No se encuentra {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        name = entry.get('degree_name')
        subjects = entry.get('subjects', [])
        total = len(subjects)
        
        # Identificador único: Nombre + URL de la guía
        seen = {}
        duplicates_count = 0
        
        for s in subjects:
            uid = f"{s['name']}|{s['guide_url']}"
            if uid in seen:
                seen[uid] += 1
                duplicates_count += 1
            else:
                seen[uid] = 1
        
        uniques = len(seen)
        
        print(f"\n🎓 {name}")
        print(f"   Total capturadas: {total}")
        print(f"   Asignaturas ÚNICAS: {uniques}")
        print(f"   Duplicados eliminables: {duplicates_count}")
        
        if uniques > 0:
            ratio = (duplicates_count / total) * 100
            print(f"   Tasa de redundancia: {ratio:.2f}%")

        # Mostrar las 5 más repetidas para entender el patrón
        if duplicates_count > 0:
            print("   🔎 Top 3 más repetidas:")
            most_common = sorted(seen.items(), key=lambda x: x[1], reverse=True)[:3]
            for item, count in most_common:
                s_name = item.split('|')[0]
                print(f"      - [{count} veces] {s_name}")

if __name__ == "__main__":
    audit()
