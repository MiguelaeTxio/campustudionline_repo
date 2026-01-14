import requests
from bs4 import BeautifulSoup
import os

# URL REAL CONFIRMADA
URL = "https://www.us.es/estudiar/que-estudiar/oferta-de-grados/grado-en-arqueologia-por-la-universidad-de-granada/2420001"
OUTPUT = "/sdcard/Download/subject_page_full_debug.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def deep_debug():
    print(f"--- Descargando Ficha Real: {URL} ---")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Guardamos el HTML formateado para lectura humana
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(f"DEBUG URL: {URL}\n")
            f.write("="*50 + "\n")
            # Extraemos enlaces interesantes antes del volcado total
            f.write("ENLACES POTENCIALES DETECTADOS:\n")
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                text = link.get_text(strip=True).lower()
                if ".pdf" in href or "proyecto" in text or "programa" in text:
                    f.write(f"  -> TEXTO: '{text}' | HREF: {href}\n")
            
            f.write("\n" + "="*50 + "\n")
            f.write("VOLCADO COMPLETO DEL BODY:\n")
            if soup.body:
                f.write(soup.body.prettify())
            else:
                f.write(soup.prettify())
            
        print(f"Inspección guardada en: {OUTPUT}")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    deep_debug()
