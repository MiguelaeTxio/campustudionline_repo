import requests
from bs4 import BeautifulSoup
import json
import os

# CASO DE CONTROL: Grado en Arqueología
TARGET_URL = "https://www.us.es/estudiar/que-estudiar/oferta-de-grados/grado-en-arqueologia-por-la-universidad-de-granada"
OUTPUT_DEBUG = "us_probe_debug.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def probe_structure():
    print(f"--- Sonda de Detalle: {TARGET_URL} ---")
    
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Fallo de conexión: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Buscar tablas directamente (a veces están en el HTML principal)
    tables = soup.find_all('table')
    print(f"Tablas encontradas en la página principal: {len(tables)}")
    
    found_subjects = False
    
    for i, table in enumerate(tables):
        # Heurística: Buscar cabeceras típicas de asignaturas
        headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
        print(f"Tabla {i} Cabeceras: {headers}")
        
        if "asignatura" in headers or "créditos" in headers or "creditos" in headers:
            print(f"--> ¡CANDIDATA DETECTADA EN TABLA {i}!")
            found_subjects = True
            # Imprimir primera fila de datos
            rows = table.find_all('tr')
            if len(rows) > 1:
                cols = [td.get_text(strip=True) for td in rows[1].find_all('td')]
                print(f"    Ejemplo de fila: {cols}")

    # 2. Si no hay tablas, buscar enlaces a 'Planificación' o 'Asignaturas'
    if not found_subjects:
        print("\n--- Buscando enlaces de navegación interna ---")
        links = soup.find_all('a')
        for link in links:
            text = link.get_text(strip=True).lower()
            href = link.get('href', '')
            if "plan" in text or "asignatura" in text or "créditos" in text:
                print(f"Enlace potencial: '{text}' -> {href}")

    # Guardar HTML para análisis manual si falla
    with open(OUTPUT_DEBUG, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"\nDump HTML guardado en: {OUTPUT_DEBUG}")

if __name__ == "__main__":
    probe_structure()
