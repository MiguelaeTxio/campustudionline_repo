import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://sara.uma.es/pls/apex/"

# 1. URL de una asignatura real (Física I) obtenida en el test anterior
GUIDE_REL_URL = "f?p=101:3:::::P3_ID:171963-5158-101"

# 2. URL para intentar descubrir el catálogo del centro 315 (Industriales)
# Fijamos Tipo=3 (Grado), Curso=2025, Centro=315, pero Titulación=-1 (Vacío)
CATALOG_URL = "https://sara.uma.es/pls/apex/f?p=101:1:::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES:3,2025,315,-1"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def inspect_guide():
    print("--- 1. INSPECCIONANDO CONTENIDO DE GUÍA (Física I) ---")
    full_url = urljoin(BASE_URL, GUIDE_REL_URL)
    print(f"Target: {full_url}")
    
    try:
        r = requests.get(full_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        print(f"Page Title: {soup.title.string.strip() if soup.title else 'No Title'}")
        
        # A. Buscar enlaces a PDF explícitos
        print("\n[A] Buscando enlaces PDF...")
        pdfs = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            if '.pdf' in href.lower() or 'print' in href.lower() or 'imprimir' in text.lower():
                pdfs.append((text, href))
        
        if pdfs:
            for name, link in pdfs:
                print(f"   [PDF FOUND] {name} -> {link[:50]}...")
        else:
            print("   No PDFs found.")

        # B. Buscar contenido HTML estructurado (Tablas de datos)
        print("\n[B] Analizando estructura HTML...")
        tables = soup.find_all('table')
        print(f"   Tablas encontradas: {len(tables)}")
        
        # Buscar cabeceras típicas de guía docente
        keywords = ['Objetivos', 'Contenidos', 'Temario', 'Bibliografía', 'Evaluación']
        found_keywords = []
        text_content = soup.get_text()
        for k in keywords:
            if k in text_content:
                found_keywords.append(k)
        print(f"   Palabras clave detectadas en texto: {found_keywords}")

    except Exception as e:
        print(f"Error en Guía: {e}")

def discover_catalog():
    print("\n--- 2. TEST DE DESCUBRIMIENTO DE CATÁLOGO (Centro 315) ---")
    print(f"Target: {CATALOG_URL}")
    
    try:
        r = requests.get(CATALOG_URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Buscar el select de titulaciones que debería estar poblado
        select = soup.find('select', {'id': 'INICIO_LOV_TITULACIONES'})
        if select:
            options = select.find_all('option')
            valid = [o for o in options if o.get('value') != '-1']
            
            if valid:
                print(f"SUCCESS! Dropdown populated with {len(valid)} degrees.")
                print("Samples:")
                for o in valid[:5]:
                    print(f"   ID: {o['value']} | {o.get_text(strip=True)}")
            else:
                print("FAILURE. Dropdown exists but is empty (only default option).")
        else:
            print("FAILURE. Select element 'INICIO_LOV_TITULACIONES' not found.")
            
    except Exception as e:
        print(f"Error en Catálogo: {e}")

if __name__ == "__main__":
    inspect_guide()
    discover_catalog()
