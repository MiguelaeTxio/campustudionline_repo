import requests
from bs4 import BeautifulSoup
import sys
import os

# --- CONFIGURACIÓN ---
BASE_URL = "https://sara.uma.es/pls/apex/f?p=101:1"
DEBUG_FILE = '/sdcard/Download/debug_uma.html'
CURRENT_YEAR = "2025" 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def log(msg):
    print(msg)

def run_debug():
    log("=== UMA SNAPSHOT DEBUG ===")
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # 1. ENTRADA
    log("1. Obteniendo Session ID...")
    r = session.get(f"{BASE_URL}:::::INICIO_LOV_TIPO_ESTUDIO:3")
    soup = BeautifulSoup(r.text, 'html.parser')
    p_instance = soup.find('input', {'name': 'p_instance'}).get('value')
    log(f"   Session ID: {p_instance}")
    
    # 2. CENTROS
    select_centros = soup.find('select', {'id': 'INICIO_LOV_CENTROS'})
    centros = [o for o in select_centros.find_all('option') if o.get('value') != '-1']
    
    if not centros:
        log("ERROR: No se encontraron centros.")
        return

    # COGEMOS SOLO EL PRIMERO PARA EL TEST
    centro = centros[0]
    id_c = centro.get('value')
    nom_c = centro.get_text(strip=True)
    log(f"2. Centro seleccionado: {nom_c} ({id_c})")
    
    # 3. TITULACIONES
    url_grados = f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS:3,{CURRENT_YEAR},{id_c}"
    r_g = session.get(url_grados)
    soup_g = BeautifulSoup(r_g.text, 'html.parser')
    select_grados = soup_g.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
    
    grados = [o for o in select_grados.find_all('option') if o.get('value') != '-1']
    if not grados:
        log("ERROR: No se encontraron grados.")
        return

    # COGEMOS SOLO EL PRIMERO PARA EL TEST
    grado = grados[0]
    id_g = grado.get('value')
    nom_g = grado.get_text(strip=True)
    log(f"3. Grado seleccionado: {nom_g} ({id_g})")
    
    # 4. CAPTURA DE PÁGINA DE ASIGNATURAS
    log("4. Solicitando página de asignaturas...")
    
    # URL idéntica a la que usaba victoria
    url_asig = (
        f"https://sara.uma.es/pls/apex/f?p=101:1:{p_instance}::::"
        f"INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,"
        f"INICIO_LOV_TITULACIONES,INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:"
        f"3,{CURRENT_YEAR},{id_c},{id_g},-1,-1,"
    )
    
    log(f"   URL Target: {url_asig}")
    r_a = session.get(url_asig)
    
    log(f"   Status Code: {r_a.status_code}")
    log(f"   Tamaño respuesta: {len(r_a.text)} bytes")
    
    # Análisis rápido
    soup_a = BeautifulSoup(r_a.text, 'html.parser')
    tabla = soup_a.find('table', class_='t-Report-report')
    if tabla:
        filas = tabla.find_all('tr')
        log(f"   [ANÁLISIS] Tabla encontrada con {len(filas)} filas.")
    else:
        log("   [ANÁLISIS] ¡TABLA NO ENCONTRADA! (Causa del bucle)")
        # Buscar mensajes de error comunes
        if "No se ha encontrado ningún dato" in r_a.text:
            log("   -> El servidor dice: 'No se ha encontrado ningún dato'")
    
    # 5. VOLCADO
    with open(DEBUG_FILE, 'w', encoding='utf-8') as f:
        f.write(r_a.text)
    
    log(f"\n[FIN] HTML guardado en: {DEBUG_FILE}")
    log("Por favor, revisa este archivo o ábrelo en un navegador para ver qué pasó.")

if __name__ == "__main__":
    run_debug()
