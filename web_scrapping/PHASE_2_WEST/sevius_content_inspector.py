# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/PHASE_2_WEST/sevius_content_inspector.py
import requests
from bs4 import BeautifulSoup
import os

# URL de la asignatura de control en SEVIUS
URL = "https://sevius4.us.es/index.php?PyP=LISTA&codcentro=4&titulacion=242&asignatura=2420001"
OUTPUT = "/sdcard/Download/sevius_html_dump.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def inspect_content():
    print(f"--- Inspeccionando SEVIUS en: {URL} ---")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(f"DEBUG SEVIUS URL: {URL}\n")
            f.write("="*50 + "\n")
            
            # Intentamos localizar el contenedor principal de datos
            # Normalmente es un div con id 'contenido' o similar en SEVIUS
            main_content = soup.find('div', id='contenido') or soup.find('section') or soup.body
            
            if main_content:
                f.write("VOLCADO DEL CONTENIDO DETECTADO:\n")
                f.write(main_content.prettify())
            else:
                f.write("No se detectó un contenedor claro. Volcando body completo.\n")
                f.write(soup.body.prettify())
                
        print(f"Inspección guardada en: {OUTPUT}")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    inspect_content()
