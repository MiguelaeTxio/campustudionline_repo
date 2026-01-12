import json
import os
from collections import Counter

# --- RUTA ABSOLUTA ANDROID ---
INPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"

def audit():
    print("🔍 AUDITORÍA DE CALIDAD UGR (V4 RAW)")
    print("=" * 60)
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No se encuentra {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        name = entry.get('degree_name')
        subjects = entry.get('subjects', [])
        
        print(f"\n🎓 {name}")
        print(f"   Total asignaturas: {len(subjects)}")
        
        if subjects:
            # Contar distribución de años y semestres
            year_dist = Counter([s.get('year') for s in subjects])
            sem_dist = Counter([s.get('semester') for s in subjects])
            
            print(f"   Distribución Años: {dict(year_dist)}")
            print(f"   Distribución Semestres: {dict(sem_dist)}")
            
            # Alerta de estancamiento
            if len(year_dist) == 1 and 1 in year_dist:
                print("   ⚠️ ALERTA: Todas las asignaturas están en AÑO 1.")
        else:
            print("   ⚠️ Sin datos.")

if __name__ == "__main__":
    audit()
