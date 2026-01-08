import requests
from bs4 import BeautifulSoup
import json

# --- CONFIGURACIÓN MAGALLANES ---
# URL estándar para llamadas AJAX en APEX
AJAX_URL = "https://sara.uma.es/pls/apex/wwv_flow.show"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest' # Importante para que el servidor sepa que es AJAX
}

def probar_obtencion_centros():
    print("--- INICIANDO SONDEO AJAX (MAGALLANES) ---")
    
    # Hipótesis: x01 es el nombre del campo destino, x02 es el valor del padre (Tipo Estudio = 3 Grado)
    params = {
        'p_flow_id': '101',
        'p_flow_step_id': '1',
        'p_instance': '0',
        'request': 'PLUGIN=apex.widget.selectlist',
        'x01': 'INICIO_LOV_CENTROS', # Queremos rellenar esto
        'x02': '3'                   # Dado que hemos seleccionado 'Grado'
    }
    
    print(f"Enviando solicitud AJAX simulada para 'Grado' (x02=3)...")
    try:
        r = requests.post(AJAX_URL, headers=HEADERS, data=params, timeout=15)
        print(f"Status Code: {r.status_code}")
        
        if r.status_code == 200:
            print("Respuesta recibida. Analizando...")
            # La respuesta suele ser un HTML parcial con <option> o un JSON
            # Probemos parsear como HTML primero (APEX clásico)
            soup = BeautifulSoup(r.text, 'html.parser')
            options = soup.find_all('option')
            
            if options:
                print(f"¡ÉXITO! Se han recuperado {len(options)} centros.")
                validos = [o for o in options if o.get('value') != '-1']
                print(f"Centros válidos: {len(validos)}")
                
                # Mostrar muestra
                print("\n--- MUESTRA DE DATOS ---")
                for o in validos[:5]:
                    print(f"ID: {o.get('value')} | Nombre: {o.get_text(strip=True)}")
                
                # Guardar mapa para uso futuro
                mapa_centros = {o.get('value'): o.get_text(strip=True) for o in validos}
                with open('/sdcard/Download/uma_centros_map.json', 'w', encoding='utf-8') as f:
                    json.dump(mapa_centros, f, indent=4, ensure_ascii=False)
                print("\nMapa de centros guardado en '/sdcard/Download/uma_centros_map.json'")
                
            else:
                print("FALLO: La respuesta 200 no contiene etiquetas <option>.")
                print("Contenido raw (primeros 500 chars):")
                print(r.text[:500])
        else:
            print(f"FALLO: El servidor rechazó la solicitud ({r.status_code})")
            
    except Exception as e:
        print(f"ERROR DE CONEXIÓN: {e}")

if __name__ == "__main__":
    probar_obtencion_centros()
