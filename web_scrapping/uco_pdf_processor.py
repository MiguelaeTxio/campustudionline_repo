import json
import os
import requests
import pdfplumber
import time
from io import BytesIO
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuración
INPUT_FILE = 'uco_final_data.json'
OUTPUT_FILE = 'uco_final_data_enriched.json'
DELAY_SECONDS = 1.5  # Pausa entre peticiones para evitar bloqueos
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_session():
    """Configura una sesión con reintentos automáticos."""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def extract_sections(text):
    """(Placeholder) Lógica de extracción futura."""
    return {
        "objectives": "",
        "content_outline": "",
        "bibliography": ""
    }

def main():
    print("--- INICIANDO PROCESAMIENTO ROBUSTO DE PDFs UCO ---")
    
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] No se encuentra {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Total asignaturas: {len(data)}")
    session = get_session()
    
    processed_count = 0
    
    for i, item in enumerate(data):
        # Si ya fue procesado correctamente en una ejecución anterior, saltar
        if item.get('parsing_status') == 'SUCCESS' and 'raw_text' in item:
            continue

        url = item.get('pdf_url')
        name = item.get('name', 'Desconocida')
        
        print(f"[{i+1}/{len(data)}] {name}...", end=" ", flush=True)
        
        if not url or not url.endswith('.pdf'):
            print("SKIP (URL inválida)")
            item['parsing_status'] = 'SKIPPED'
            continue
            
        try:
            # Pausa de cortesía
            time.sleep(DELAY_SECONDS)
            
            response = session.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                full_text = ""
                for page in pdf.pages:
                    extract = page.extract_text()
                    if extract:
                        full_text += extract + "\n"
                
                item['raw_text'] = full_text
                item['extracted_info'] = extract_sections(full_text)
                item['parsing_status'] = 'SUCCESS'
                # Limpiar error previo si existía
                if 'parsing_error' in item:
                    del item['parsing_error']
                print("OK")
                processed_count += 1
                
        except Exception as e:
            print(f"ERROR")
            item['parsing_status'] = 'ERROR'
            item['parsing_error'] = str(e)
            
        # Guardado incremental seguro cada 5 items
        if processed_count > 0 and processed_count % 5 == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    # Guardado final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"\n--- PROCESO FINALIZADO ---")
    print(f"Archivo generado: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
