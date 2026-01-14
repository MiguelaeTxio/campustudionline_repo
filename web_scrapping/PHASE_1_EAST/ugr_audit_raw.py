import json
import os

# --- RUTA ABSOLUTA ANDROID ---
INPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"

def audit():
    print("🔍 AUDITORÍA DE DATOS RECIÉN CAPTURADOS: UGR")
    print("=" * 50)
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No se encuentra el archivo {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        slug = entry.get('degree_slug')
        subjects = entry.get('subjects', [])
        print(f"\n🎓 Grado: {slug}")
        print(f"   Total asignaturas: {len(subjects)}")
        
        if subjects:
            # Inspeccionamos la primera asignatura para ver qué campos tenemos
            sample = subjects[0]
            print(f"   Campos detectados: {list(sample.keys())}")
            
            # Verificación de campos críticos
            has_year = 'year' in sample or 'curso' in sample
            print(f"   ¿Tiene Año/Curso?: {'✅ SÍ' if has_year else '❌ NO (Peligro: Todo irá a Año 1)'}")
            
            # Mostrar tipos detectados
            tipos = list(set([s.get('type', 'N/A') for s in subjects]))
            print(f"   Tipos encontrados: {tipos}")
            
            # Muestra de las 3 primeras
            print("   Muestra:")
            for s in subjects[:3]:
                print(f"      - {s['code']} | {s['name']} | {s.get('type')}")
        else:
            print("   ⚠️ Sin asignaturas capturadas.")

if __name__ == "__main__":
    audit()
