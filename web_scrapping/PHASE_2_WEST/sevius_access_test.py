# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/PHASE_2_WEST/sevius_access_test.py
import requests
from bs4 import BeautifulSoup
import os

"""
Script de diagnóstico para verificar el acceso público a la Secretaría Virtual (SEVIUS4).
Extrará el contenido de la asignatura de control para identificar barreras de login.
"""

# URL de la asignatura de control en SEVIUS
TEST_URL = "https://sevius4.us.es/index.php?PyP=LISTA&codcentro=4&titulacion=242&asignatura=2420001"
OUTPUT_FILE = "/sdcard/Download/sevius_test_report.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def check_access():
    print(f"--- Probando acceso a SEVIUS: {TEST_URL} ---")
    
    try:
        response = requests.get(TEST_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"URL PROBADA: {TEST_URL}\n")
            f.write(f"STATUS CODE: {response.status_code}\n")
            f.write("-" * 50 + "\n")
            
            # Buscamos indicios de login
            page_text = response.text.lower()
            if "usuario" in page_text and "contraseña" in page_text:
                f.write("ESTADO: REQUIERE AUTENTICACIÓN (UVUS detectado)\n")
            elif "autenticación" in page_text or "identificación" in page_text:
                f.write("ESTADO: REQUIERE AUTENTICACIÓN\n")
            else:
                f.write("ESTADO: POSIBLE ACCESO PÚBLICO\n")
            
            f.write("-" * 50 + "\n")
            f.write("ENLACES ENCONTRADOS (Buscando .pdf o Programas):\n")
            links = soup.find_all('a', href=True)
            pdf_links = [l for l in links if ".pdf" in l['href'].lower()]
            
            if pdf_links:
                for pl in pdf_links:
                    f.write(f"  [PDF] {pl.get_text(strip=True)} -> {pl['href']}\n")
            else:
                f.write("  No se encontraron enlaces directos a PDF.\n")
                
            f.write("\n" + "="*50 + "\n")
            f.write("RESUMEN DEL HTML (Primeros 2000 caracteres):\n")
            f.write(response.text[:2000])
            
        print(f"Resultado guardado en: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"[ERROR] Fallo en la conexión: {e}")

if __name__ == "__main__":
    check_access()
