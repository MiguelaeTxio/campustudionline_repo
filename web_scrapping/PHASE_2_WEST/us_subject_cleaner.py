import json
import os

# CONFIGURACIÓN
INPUT_FILE = "/sdcard/Download/us_raw_subjects.json"
OUTPUT_FILE = "/sdcard/Download/us_clean_subjects.json"

def clean_data():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encuentra el archivo: {INPUT_FILE}")
        return

    print("--- Iniciando Limpieza de Datos ---")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    cleaned_data = {
        "university": raw_data.get("university", "US"),
        "timestamp": raw_data.get("timestamp", ""),
        "degrees_processed": 0,
        "data": []
    }

    stats = {
        "total_subjects": 0,
        "kept": 0,
        "deleted": 0,
        "reasons": {}
    }

    for degree in raw_data.get("data", []):
        new_degree = degree.copy()
        new_subjects = []
        
        for subject in degree.get("subjects", []):
            stats["total_subjects"] += 1
            name = subject.get("name", "").strip()
            name_lower = name.lower()
            
            should_delete = False
            reason = ""

            # REGLAS DE EXCLUSIÓN (Quirúrgicas)
            
            # 1. Por Contenido (Cualquier parte del nombre)
            if "fin de grado" in name_lower:
                should_delete = True
                reason = "TFG/PFG"
            elif "prácticas externas" in name_lower or "practicas externas" in name_lower:
                should_delete = True
                reason = "Prácticas Externas"
            elif "prácticas en empresas" in name_lower or "practicas en empresa" in name_lower:
                should_delete = True
                reason = "Prácticas Empresa"
                
            # 2. Por Inicio Exacto
            elif name_lower.startswith("prácticum") or name_lower.startswith("practicum"):
                should_delete = True
                reason = "Prácticum"
            elif name_lower.startswith("rotatorio"):
                should_delete = True
                reason = "Rotatorio"

            if should_delete:
                stats["deleted"] += 1
                stats["reasons"][reason] = stats["reasons"].get(reason, 0) + 1
            else:
                # Normalización de Créditos
                try:
                    cred_str = subject.get("credits", "0").replace(",", ".")
                    subject["credits"] = float(cred_str)
                except:
                    subject["credits"] = 0.0
                
                new_subjects.append(subject)
                stats["kept"] += 1

        new_degree["subjects"] = new_subjects
        new_degree["subjects_count"] = len(new_subjects)
        cleaned_data["data"].append(new_degree)

    cleaned_data["degrees_processed"] = len(cleaned_data["data"])

    # Guardar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

    print("\n=== RESUMEN DE LIMPIEZA ===")
    print(f"Total procesado: {stats['total_subjects']}")
    print(f"Conservadas:     {stats['kept']}")
    print(f"Eliminadas:      {stats['deleted']}")
    print("\nDesglose de eliminaciones:")
    for r, count in stats["reasons"].items():
        print(f"  - {r}: {count}")
    print(f"\nArchivo limpio generado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_data()
