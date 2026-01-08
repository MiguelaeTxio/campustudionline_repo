import requests
from bs4 import BeautifulSoup
import re
import json

BASE_URL = "https://sara.uma.es/pls/apex/f?p=101:1"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def navegar():
    print("--- INICIANDO PROTOCOLO ELCANO ---")
    session = requests.Session()
    session.headers.update(HEADERS)

    # 1. Obtener Sesión
    print("1. Obteniendo Session ID...")
    try:
        r = session.get(BASE_URL, timeout=15)
        # Buscar p_instance
        match = re.search(r'p_instance\s*=\s*"(\d+)"', r.text)
        if not match:
            # Intento alternativo input hidden
            soup = BeautifulSoup(r.text, 'html.parser')
            inp = soup.find('input', {'name': 'p_instance'})
            if inp:
                p_instance = inp.get('value')
            else:
                print("ERROR: No se pudo extraer p_instance.")
                return
        else:
            p_instance = match.group(1)
            
        print(f"   Session ID: {p_instance}")

        # 2. Petición AJAX "Elcano" (Parámetros en URL)
        # NOTA: En APEX, el request string para el plugin debe ir en la URL para que el router lo intercepte.
        
        # URL Construida manualmente con cuidado
        ajax_url = (
            f"https://sara.uma.es/pls/apex/wwv_flow.show"
            f"?p_flow_id=101"
            f"&p_flow_step_id=1"
            f"&p_instance={p_instance}"
            f"&p_request=PLUGIN%3Dapex.widget.selectlist"
        )
        
        # Datos del payload (lo que varía)
        payload = {
            'x01': 'INICIO_LOV_CENTROS', # El campo que queremos poblar
            'x02': '3'                   # El valor de 'Tipo Estudio' (Grado)
            # A veces se necesita enviar 'p_salt' si la página está protegida, 
            # pero probemos sin salt primero.
        }
        
        print(f"2. Enviando AJAX a URL construida...")
        print(f"   Target: {ajax_url}")
        
        r_ajax = session.post(ajax_url, data=payload, timeout=15)
        
        if r_ajax.status_code == 200:
            print("   Respuesta 200 OK.")
            # Comprobar contenido
            if "<option" in r_ajax.text:
                soup = BeautifulSoup(r_ajax.text, 'html.parser')
                opts = soup.find_all('option')
                validos = [o for o in opts if o.get('value') != '-1']
                print(f"   ¡ÉXITO TOTAL! Centros recuperados: {len(validos)}")
                
                if len(validos) > 0:
                    print(f"   Primer centro: {validos[0].get_text(strip=True)}")
                    
                    # Guardar JSON definitivo
                    data = {}
                    for o in validos:
                        val = o.get('value')
                        txt = o.get_text(strip=True)
                        data[val] = txt
                        
                    with open('/sdcard/Download/uma_mapa_centros.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                print("   FALLO: Seguimos recibiendo HTML completo (o vacío).")
                print("   Primeros 100 caracteres de la respuesta:")
                print(f"   {r_ajax.text[:100]}")
        else:
            print(f"   FALLO: Status {r_ajax.status_code}")

    except Exception as e:
        print(f"Excepción: {e}")

if __name__ == "__main__":
    navegar()
