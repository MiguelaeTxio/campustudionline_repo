import json
import glob
import os
import sys

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, 'uco_final_data.json')

def main():
    print("--- INICIANDO ENSAMBLAJE DE FRAGMENTOS UCO ---")
    
    # Buscar archivos part*.json
    pattern = os.path.join(BASE_DIR, 'uco_map_part*.json')
    json_files = sorted(glob.glob(pattern))
    
    if not json_files:
        print("[ERROR] No se encontraron archivos 'uco_map_part*.json'.")
        sys.exit(1)
        
    print(f"Archivos encontrados: {len(json_files)}")
    
    master_data = []
    total_files_ok = 0
    total_files_error = 0
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                # Validación básica de estructura del primer elemento
                if data and not all(key in data[0] for key in ['university', 'degree', 'year', 'name']):
                    print(f"[WARN] {filename}: Estructura de campos sospechosa en el primer elemento.")
                
                count = len(data)
                master_data.extend(data)
                print(f"[OK] {filename}: +{count} registros.")
                total_files_ok += 1
            else:
                print(f"[ERROR] {filename}: El contenido no es una lista JSON.")
                total_files_error += 1
                
        except json.JSONDecodeError as e:
            print(f"[ERROR] {filename}: JSON Corrupto - {e}")
            total_files_error += 1
        except Exception as e:
            print(f"[ERROR] {filename}: Error inesperado - {e}")
            total_files_error += 1

    # Resultados finales
    print("\n--- RESUMEN DE EJECUCIÓN ---")
    print(f"Archivos procesados correctamente: {total_files_ok}")
    print(f"Archivos con errores: {total_files_error}")
    print(f"Total de asignaturas recolectadas: {len(master_data)}")
    
    # Guardar archivo unificado
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(master_data, f, ensure_ascii=False, indent=4)
        print(f"\n[ÉXITO] Archivo unificado generado: {OUTPUT_FILE}")
    except Exception as e:
        print(f"\n[FATAL] No se pudo guardar el archivo final: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
