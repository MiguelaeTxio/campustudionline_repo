import json
import os
import sys

def process():
    # El nuevo mapa correcto
    infile = "uco_master_map.json"
    # El archivo con los datos procesados (contenido PDF) pero nombres mal
    backup_file = "uco_data_backup.json" 
    # El archivo de salida final corregido
    outfile = "uco_data_final.json"
    
    if not os.path.exists(infile):
        print("ERROR: Falta uco_master_map.json")
        return

    # Cargar mapa maestro nuevo (Nombres OK)
    with open(infile, 'r', encoding='utf-8') as f:
        master_data = json.load(f)
        subjects_master = master_data.get('subjects', [])

    # Cargar datos viejos (Contenido OK)
    content_cache = {}
    if os.path.exists(backup_file):
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                old_list = json.load(f)
                for item in old_list:
                    # Indexar por código
                    content_cache[item['code']] = item
            print(f"-> Caché de contenido cargada: {len(content_cache)} registros.")
        except Exception as e:
            print(f"-> Error cargando backup: {e}")
    else:
        print("-> AVISO: No se encontró uco_data_backup.json. Se procesará sin caché (descarga completa).")

    final_list = []
    total = len(subjects_master)
    merged_count = 0
    
    print(f"Iniciando fusión de datos para {total} asignaturas...")

    for idx, sub_master in enumerate(subjects_master):
        code = sub_master.get('code')
        
        # Estrategia de Fusión:
        # Tomamos el objeto del MASTER (que tiene el Nombre y Rama correctos)
        # Y le inyectamos el CONTENIDO del BACKUP si existe.
        
        if code in content_cache:
            cached_sub = content_cache[code]
            if cached_sub.get('content_status') == 'OK':
                sub_master['learning_objectives'] = cached_sub.get('learning_objectives', [])
                sub_master['course_content_outline'] = cached_sub.get('course_content_outline', [])
                sub_master['bibliography'] = cached_sub.get('bibliography', {})
                sub_master['content_status'] = 'OK'
                merged_count += 1
            else:
                # Si falló antes, mantenemos el estado de error
                sub_master['content_status'] = cached_sub.get('content_status', 'PENDING')
        else:
             sub_master['content_status'] = 'PENDING' # No estaba en el backup
        
        final_list.append(sub_master)
        
        # Feedback visual
        pct = (idx + 1) / total * 100
        sys.stdout.write(f"\r[{idx+1}/{total}] {pct:.1f}% - Fusionado: {sub_master.get('name')[:30]}")
        sys.stdout.flush()

    # Guardado final
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"\n\n¡Fusión completada! Registros recuperados: {merged_count}/{total}. Guardado en {outfile}")
    print("Nota: Si hay registros 'PENDING', significa que no estaban en el backup y requerirían descarga manual.")

if __name__ == "__main__":
    process()
