import json
import unicodedata

INPUT_FILE = '/sdcard/Download/uma_pattern_data.json'
OUTPUT_FILE = '/sdcard/Download/uma_pattern_data_cleaned.json'

def normalize(text):
    """Normaliza texto para búsquedas robustas (minúsculas)."""
    return text.lower() if text else ""

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ No se encuentra el archivo {INPUT_FILE}")
        return

    cleaned_data = []
    stats = {
        'practicum': 0,
        'taller': 0,
        'proyecto_fin': 0,
        'practicas_externas': 0,
        'practicas_en': 0,
        'trabajo_fin': 0,
        'kept': 0,
        'total_deleted': 0
    }

    print(f"📉 Procesando {len(data)} registros...")

    for item in data:
        name_orig = item.get('name', '')
        name = normalize(name_orig)
        
        # --- REGLAS DE ELIMINACIÓN ---
        
        # 1. Practicum (Todas)
        if 'practicum' in name:
            stats['practicum'] += 1
            stats['total_deleted'] += 1
            continue
            
        # 2. Taller (Todas)
        if 'taller' in name:
            stats['taller'] += 1
            stats['total_deleted'] += 1
            continue

        # 3. Proyecto (Sólo 'Proyecto Fin')
        if 'proyecto fin' in name:
            stats['proyecto_fin'] += 1
            stats['total_deleted'] += 1
            continue

        # 4. Práctica (Sólo 'Prácticas Externas' y 'Prácticas en')
        # Normalizamos también acentos para asegurar match
        if 'prácticas externas' in name or 'practicas externas' in name:
            stats['practicas_externas'] += 1
            stats['total_deleted'] += 1
            continue
            
        if 'prácticas en' in name or 'practicas en' in name:
            stats['practicas_en'] += 1
            stats['total_deleted'] += 1
            continue

        # 5. Trabajo (Sólo 'Trabajo Fin')
        if 'trabajo fin' in name:
            stats['trabajo_fin'] += 1
            stats['total_deleted'] += 1
            continue

        # --- CONSERVACIÓN ---
        cleaned_data.append(item)
        stats['kept'] += 1

    # Guardar resultado
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print("\n" + "="*40)
    print("RESUMEN DE LIMPIEZA")
    print("="*40)
    print(f"❌ Practicum eliminados: {stats['practicum']}")
    print(f"❌ Taller eliminados: {stats['taller']}")
    print(f"❌ 'Proyecto Fin' eliminados: {stats['proyecto_fin']}")
    print(f"❌ 'Prácticas Externas' eliminados: {stats['practicas_externas']}")
    print(f"❌ 'Prácticas En' eliminados: {stats['practicas_en']}")
    print(f"❌ 'Trabajo Fin' eliminados: {stats['trabajo_fin']}")
    print("-" * 40)
    print(f"🗑️ TOTAL ELIMINADOS: {stats['total_deleted']}")
    print(f"✅ TOTAL CONSERVADOS: {len(cleaned_data)}")
    print("="*40)
    print(f"💾 Archivo limpio guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
