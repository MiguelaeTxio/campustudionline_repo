import requests
from bs4 import BeautifulSoup

# URL Semilla
START_URL = "https://sara.uma.es/pls/apex/f?p=101:1"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Origin': 'https://sara.uma.es',
}

def audit_interaction_self_post():
    print(f"--- UMA AUDIT TOOL v3.2 (Self-Post Strategy) ---")
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        # PASO 1: Obtener estado inicial y URL con Sesión
        print("1. Fetching initial page...")
        r_get = session.get(START_URL, timeout=20)
        r_get.raise_for_status()
        
        # Esta es la URL "buena" con el ID de sesión (f?p=101:1:SESSION_ID:...)
        current_url = r_get.url
        print(f"   [INFO] Session URL detected: {current_url}")
        
        soup = BeautifulSoup(r_get.content, 'html.parser')
        form = soup.find('form')
        if not form:
            print("CRITICAL: No form found.")
            return

        # Recolectar inputs ocultos (Esencial para mantener el estado APEX)
        payload = {}
        for input_tag in form.find_all('input'):
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            if name:
                payload[name] = value
        
        # PASO 2: Configurar payload (Centro: Informática - 306)
        print("2. Configuring payload (Self-Post)...")
        
        payload['INICIO_LOV_TIPO_ESTUDIO'] = '3'
        payload['INICIO_LOV_CENTROS'] = '306'
        payload['INICIO_LOV_TITULACIONES'] = '-1'
        payload['INICIO_LOV_CURSO_ACAD'] = '2025'
        
        # El disparador clave
        payload['p_request'] = 'INICIO_LOV_CENTROS'
        
        # PASO 3: Enviar POST a la MISMA URL de sesión
        print(f"3. Sending POST to: {current_url}")
        session.headers.update({'Referer': current_url})
        
        r_post = session.post(current_url, data=payload)
        r_post.raise_for_status()
        
        # PASO 4: Verificar resultados
        soup_post = BeautifulSoup(r_post.content, 'html.parser')
        titulaciones_select = soup_post.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
        
        if titulaciones_select:
            options = titulaciones_select.find_all('option')
            valid_options = [opt for opt in options if opt.get('value') != '-1']
            
            print(f"\n[RESULT] Success! Found {len(valid_options)} degrees.")
            for opt in valid_options:
                print(f"   - [{opt.get('value')}] {opt.get_text(strip=True)}")
                
            # Si funciona, mostramos también los hidden inputs clave para entender la sesión
            print(f"\n[DEBUG] Session Instance (p_instance): {payload.get('p_instance', 'NOT FOUND')}")
        else:
            print("FAILURE: 'INICIO_LOV_TITULACIONES' not found or empty.")
            # Debug: buscar errores visibles
            err = soup_post.find(class_='t15Notification')
            if err: print(f"   [APEX Error]: {err.get_text(strip=True)}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    audit_interaction_self_post()
