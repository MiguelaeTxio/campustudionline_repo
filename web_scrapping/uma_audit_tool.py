import json
import re
from collections import defaultdict

INPUT_FILE = '/sdcard/Download/uma_pattern_data.json'
KEYWORDS = [
    'trabajo', 'visita', 'práctica', 'practicum', 'traslado', 
    'créditos', 'reconocimiento', 'taller', 'seminario', 
    'jornada', 'proyecto', 'laboratorio', 'clínica', 'rotatorio'
]

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ No se encuentra el archivo {INPUT_FILE}")
        return

    hits = defaultdict(set)
    total_subjects = len(data)
    
    print(f"🔍 Analizando {total_subjects} registros...")
    
    for item in data:
        original_name = item.get('name', '')
        name_lower = original_name.lower()
        
        for kw in KEYWORDS:
            # Búsqueda simple (case-insensitive)
            if kw in name_lower:
                hits[kw].add(original_name)

    print("\n" + "="*60)
    print("RESUMEN DE COINCIDENCIAS POR PALABRA CLAVE")
    print("="*60)

    for kw in sorted(KEYWORDS):
        matches = hits.get(kw, set())
        if matches:
            print(f"\n🔶 PALABRA CLAVE: '{kw.upper()}' ({len(matches)} variaciones únicas)")
            print("-" * 40)
            # Mostramos las primeras 20 variantes para no saturar, pero ordenadas
            for subj in sorted(list(matches))[:50]:
                print(f"  • {subj}")
            
            if len(matches) > 50:
                print(f"  ... y {len(matches) - 50} más.")
        else:
            # Opcional: mostrar si no hay hits
            pass

    print("\n" + "="*60)
    print("FIN DE LA AUDITORÍA")

if __name__ == "__main__":
    main()
