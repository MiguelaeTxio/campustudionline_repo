import requests
from bs4 import BeautifulSoup
import os

# Página del Grado (Confirmada que funciona)
URL = "https://www.us.es/estudiar/que-estudiar/oferta-de-grados/grado-en-arqueologia-por-la-universidad-de-granada"
OUTPUT = "/sdcard/Download/us_row_debug.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def inspect_rows():
    print(f"--- Inspeccionando tabla en: {URL} ---")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscamos la tabla que tiene las asignaturas
        tables = soup.find_all('table')
        
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(f"URL: {URL}\n")
            f.write("-" * 50 + "\n")
            
            for i, table in enumerate(tables):
                headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
                if "asignatura" in headers:
                    f.write(f"TABLA ENCONTRADA (Índice {i})\n")
                    # Tomamos las primeras 3 filas de datos
                    rows = table.find_all('tr')[:4] 
                    for j, row in enumerate(rows):
                        f.write(f"\nFILA {j}:\n")
                        f.write(row.prettify())
                        f.write("\n" + "="*30 + "\n")
            
        print(f"Inspección completada. Archivo guardado en: {OUTPUT}")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    inspect_rows()
