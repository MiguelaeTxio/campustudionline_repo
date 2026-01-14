import requests
from bs4 import BeautifulSoup

# URL Directa proporcionada (Ingeniería Industrial - ID 5158)
TARGET_URL = "https://sara.uma.es/pls/apex/f?p=101:1:::::INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES,INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:3,2025,315,5158,-1,-1,"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def test_direct_access():
    print(f"--- UMA DIRECT LINK TEST ---")
    print(f"Targeting Degree ID: 5158 (via URL param)")
    
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar la tabla de asignaturas
        # Estrategia: Buscar enlaces que contengan 'GUIA' o estructura típica de asignaturas
        print("\n[ANALYSIS] Scanning for subjects...")
        
        subjects_found = 0
        
        # En APEX, las tablas de resultados suelen tener clases como 'u-Report-table' o estar dentro de regiones
        # Buscamos filas de tabla <tr>
        rows = soup.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if not cells: continue
            
            # Heurística UMA:
            # Normalmente: Código | Nombre (con enlace) | Curso | ...
            # Buscamos un enlace en alguna celda
            
            for cell in cells:
                link = cell.find('a', href=True)
                if link:
                    text = link.get_text(strip=True)
                    href = link.get('href')
                    
                    # Filtros básicos para descartar basura
                    if len(text) > 5 and not "javascript" in href:
                        print(f"   [SUBJECT?] {text} -> {href[:40]}...")
                        subjects_found += 1
                        # Solo imprimimos una vez por fila para no duplicar
                        break 
        
        if subjects_found > 0:
            print(f"\nSUCCESS! Found {subjects_found} potential subjects.")
        else:
            print("\nFAILURE. Page loaded but no subjects found. (Session expired or bad params?)")
            # Debug: imprimir título por si nos redirigió
            print(f"Page Title: {soup.title.string.strip() if soup.title else 'No Title'}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_direct_access()
