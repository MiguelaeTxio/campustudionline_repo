import json
import os
from collections import Counter

INPUT_FILE = "/sdcard/Download/uja_refined.json"

def audit():
    print("🔍 AUDITORÍA DE CALIDAD UJA (LOCAL)")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ No encuentro {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    stuck_degrees = []
    good_degrees = []

    print(f"📊 Total Titulaciones: {len(data)}")
    print("-" * 40)

    for degree in data:
        # Recuperamos nombre (gestionando ambas claves por seguridad)
        d_name = degree.get('degree', degree.get('degree_name', 'Unknown'))
        subjects = degree.get('subjects', [])
        
        if not subjects: continue

        # Contamos distribución de años
        years = [s.get('year', 1) for s in subjects]
        year_counts = Counter(years)
        
        # Criterio: Si el 100% de las asignaturas son de Año 1, algo falló (o es un máster de 1 año)
        total_subjs = len(subjects)
        year_1_count = year_counts.get(1, 0)
        
        is_stuck = (year_1_count == total_subjs) and (total_subjs > 0)
        
        if is_stuck:
            stuck_degrees.append(f"{d_name} ({total_subjs} asig.)")
        else:
            good_degrees.append(f"{d_name}: {dict(year_counts)}")

    # RESULTADOS
    print(f"\n✅ TITULACIONES CORRECTAS (Con variedad de años): {len(good_degrees)}")
    # Mostrar solo las primeras 5 para no saturar
    # for d in good_degrees[:5]: print(f"   - {d}")

    print(f"\n⚠️ TITULACIONES 'ATASCADAS' EN AÑO 1: {len(stuck_degrees)}")
    for d in stuck_degrees:
        print(f"   ❌ {d}")

    print("-" * 40)
    print("CONCLUSIÓN:")
    if len(stuck_degrees) > 20:
        print("⛔ EL DATASET TIENE MUCHOS FALLOS. NO SUBIR.")
    else:
        print("✅ EL DATASET PARECE RAZONABLE (Revisar los fallos puntuales).")

if __name__ == "__main__":
    audit()
