import requests
import os

# Asignatura de prueba (Antropología Cultural)
URL = "https://www.us.es/estudiar/que-estudiar/oferta-de-grados/grado-en-arqueologia-por-la-universidad-de-granada/antropologia-cultural"
OUTPUT = "/sdcard/Download/subject_debug.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

def debug_html():
    print(f"--- Descargando HTML de: {URL} ---")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Archivo guardado en: {OUTPUT}")
        print(f"Tamaño: {len(response.text)} caracteres.")
        
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el HTML: {e}")

if __name__ == "__main__":
    debug_html()
