# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uja_harvester_v2.py
import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin

# --- CONFIGURACIÓN ---
BASE_DOMAIN = "https://uvirtual.ujaen.es"
START_URL = "https://uvirtual.ujaen.es/pub/es/informacionacademica/catalogofichasdocentesasignaturas/p/2025-26"
OUTPUT_FILE = "uja_raw_data.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def get_soup(url, context=""):
    """Realiza petición segura y devuelve Soup."""
    try:
        # Pequeño delay para no saturar
        time.sleep(0.5) 
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"❌ Error en {context}: {e}")
        return None

def extract_subjects_from_table(soup):
    """Extrae asignaturas de la tabla específica de la UJA."""
    subjects = []
    table = soup.find('table', id='listadofichasdocentesasignatura')
    
    if not table:
        return []

    # Iterar filas del cuerpo
    rows = table.find_all('tr')
    for row in rows:
        # Ignorar fila de filtros o cabeceras vacías
        if row.get('id') == 'trDeFilaDeFiltro' or row.find('th'):
            continue
            
        cols = row.find_all('td')
        if len(cols) < 5:
            continue

        # Estructura basada en tu HTML:
        # col[1]: Año (2025-26)
        # col[2]: Código (13712001)
        # col[4]: Enlace y Nombre
        
        code = cols[2].get_text(strip=True)
        link_tag = cols[4].find('a')
        
        if link_tag and code:
            name = link_tag.get_text(strip=True)
            href = link_tag.get('href')
            full_url = urljoin(BASE_DOMAIN, href)
            
            subjects.append({
                "code": code,
                "name": name,
                "guide_url": full_url
            })
            
    return subjects

def harvest():
    print("🚜 INICIANDO COSECHADORA UJA V2...")
    all_data = []
    
    # 1. Obtener Centros
    print(f"📍 Accediendo a índice: {START_URL}")
    soup_index = get_soup(START_URL, "Index")
    if not soup_index: return

    centro_select = soup_index.find('select', {'name': 'centro'})
    if not centro_select:
        print("❌ No se encontró selector de centros.")
        return

    centros = []
    for option in centro_select.find_all('option'):
        if option.get('value') and "Seleccione" not in option.get_text():
            centros.append({
                "name": option.get_text(strip=True),
                "url": urljoin(BASE_DOMAIN, option.get('value'))
            })

    print(f"🏫 Se encontraron {len(centros)} Centros.")

    # 2. Recorrer Centros
    for i, centro in enumerate(centros):
        print(f"\n[{i+1}/{len(centros)}] Procesando Centro: {centro['name']}")
        soup_centro = get_soup(centro['url'], "Centro")
        if not soup_centro: continue

        # 3. Obtener Planes (Grados/Másteres)
        plan_select = soup_centro.find('select', {'name': 'planEstudios'})
        if not plan_select:
            print("   ⚠️ Sin selector de planes.")
            continue

        planes = []
        for option in plan_select.find_all('option'):
            if option.get('value') and "Seleccione" not in option.get_text():
                # Extraer código de plan del texto (ej: "... (137A)")
                plan_name = option.get_text(strip=True)
                plan_code = ""
                if "(" in plan_name and plan_name.endswith(")"):
                    plan_code = plan_name.split("(")[-1].replace(")", "")

                planes.append({
                    "name": plan_name,
                    "code": plan_code,
                    "url": urljoin(BASE_DOMAIN, option.get('value'))
                })

        print(f"   📜 Encontrados {len(planes)} Planes de Estudio.")

        # 4. Recorrer Planes y Extraer Asignaturas
        for j, plan in enumerate(planes):
            print(f"      -> ({j+1}/{len(planes)}) Escaneando: {plan['code']} - {plan['name'][:40]}...")
            soup_plan = get_soup(plan['url'], "Plan")
            
            if soup_plan:
                subjects = extract_subjects_from_table(soup_plan)
                
                if subjects:
                    entry = {
                        "university": "Universidad de Jaén",
                        "center": centro['name'],
                        "degree": plan['name'],
                        "degree_code": plan['code'],
                        "subjects": subjects
                    }
                    all_data.append(entry)
                    print(f"         ✅ {len(subjects)} asignaturas extraídas.")
                else:
                    print("         ⚠️ Tabla de asignaturas vacía.")
            
            # Guardado parcial por seguridad
            if j % 5 == 0:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, indent=4, ensure_ascii=False)

    # Guardado Final
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n🎉 COSECHA COMPLETADA. Datos guardados en {OUTPUT_FILE}")
    print(f"📊 Total de titulaciones procesadas: {len(all_data)}")

if __name__ == "__main__":
    harvest()
