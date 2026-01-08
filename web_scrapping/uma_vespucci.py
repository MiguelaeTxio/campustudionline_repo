import requests
from bs4 import BeautifulSoup
import re
import json

# URL de entrada
BASE_URL = "https://sara.uma.es/pls/apex/f?p=101:1"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def navegar():
    print("--- INICIANDO PROTOCOLO VESPUCIO ---")
    session = requests.Session()
    session.headers.update(HEADERS)

    # 1. Obtener Sesión (GET)
    print("1. Solicitando página de inicio para obtener Session ID...")
    try:
        r = session.get(BASE_URL, timeout=15)
        if r.status_code != 200:
            print(f"ERROR CRÍTICO: La página devolvió {r.status_code}")
            return
        
        # 2. Extraer p_instance (Session ID)
        # Buscamos: <input type="hidden" name="p_instance" value="4523452345..." />
        soup = BeautifulSoup(r.text, 'html.parser')
        input_instance = soup.find('input', {'name': 'p_instance'})
        
        if not input_instance:
            print("ERROR: No se encontró el campo oculto 'p_instance'.")
            # Intento de fallback con regex por si acaso
            match = re.search(r'p_instance\s*=\s*"(\d+)"', r.text)
            if match:
                p_instance = match.group(1)
            else:
                return
        else:
            p_instance = input_instance.get('value')

        print(f"¡ÉXITO! Session ID capturado: {p_instance}")

        # 3. Lanzar Petición AJAX Autenticada
        # La URL de AJAX en APEX suele ser la del "Flow" con parámetros específicos
        # Vamos a probar la ruta de plugin estándar pero CON la instancia válida
        
        ajax_url = f"https://sara.uma.es/pls/apex/wwv_flow.show?p_flow_id=101&p_flow_step_id=1&p_instance={p_instance}"
        
        payload = {
            'p_request': 'PLUGIN=apex.widget.selectlist',
            'p_instance': p_instance,
            'x01': 'INICIO_LOV_CENTROS', # Campo a rellenar
            'x02': '3'                   # Valor del padre (Grado)
        }
        
        print(f"2. Solicitando Centros vía AJAX (Contexto Grado)...")
        r_ajax = session.post(ajax_url, data=payload, timeout=15)
        
        print(f"Status AJAX: {r_ajax.status_code}")
        
        if r_ajax.status_code == 200:
            # APEX suele devolver HTML con <option>
            if "<option" in r_ajax.text:
                soup_ajax = BeautifulSoup(r_ajax.text, 'html.parser')
                opts = soup_ajax.find_all('option')
                validos = [o for o in opts if o.get('value') and o.get('value') != '-1']
                
                print(f"¡VICTORIA! Recuperados {len(validos)} centros.")
                if validos:
                    print(f"Ejemplo: {validos[0].get_text(strip=True)} (ID: {validos[0]['value']})")
                    
                    # Guardar JSON
                    data = {o['value']: o.get_text(strip=True) for o in validos}
                    with open('/sdcard/Download/uma_centros_map.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print("Mapa guardado en /sdcard/Download/uma_centros_map.json")
            else:
                print("La respuesta 200 no parece contener opciones.")
                print(r_ajax.text[:200])
        else:
            print("Fallo en la petición AJAX.")

    except Exception as e:
        print(f"Excepción: {e}")

if __name__ == "__main__":
    navegar()
