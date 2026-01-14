import json
import os
import sys

# Rutas Android
BAD_FILE = '/sdcard/Download/uma_sextante_data.json'
FIXED_FILE = '/sdcard/Download/uma_sextante_fixed.json'

def repair():
    print(f"--- INICIO CIRUGÍA JSON ---")
    
    if not os.path.exists(BAD_FILE):
        print(f"Error: No encuentro {BAD_FILE}")
        return

    # 1. Leer como texto crudo
    with open(BAD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Tamaño original: {len(content)} caracteres")

    # 2. Buscar el último objeto válido
    # El archivo debe terminar en "}]". Si se cortó, buscamos la última "}" real.
    last_bracket = content.rfind('}')
    
    if last_bracket == -1:
        print("FATAL: No se encontró ningún objeto JSON válido (archivo vacío o muy corrupto).")
        return

    # 3. Amputar y cauterizar
    print("Recortando archivo hasta el último registro completo...")
    # Tomamos hasta la última llave y cerramos la lista
    fixed_content = content[:last_bracket+1] + "\n]"
    
    # 4. Verificar viabilidad
    try:
        data = json.loads(fixed_content)
        print(f"¡ÉXITO! Se han recuperado {len(data)} registros.")
        
        # 5. Guardar paciente
        with open(FIXED_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Archivo reparado guardado en: {FIXED_FILE}")
        
    except json.JSONDecodeError as e:
        print(f"La cirugía falló: {e}")
        print("El daño es más complejo de lo esperado.")

if __name__ == "__main__":
    repair()
