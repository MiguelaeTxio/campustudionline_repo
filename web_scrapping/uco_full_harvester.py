# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uco_full_harvester.py
import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os

def get_code(href):
    # Extrae el código de 6 dígitos de la asignatura de la URL de la guía
    match = re.search(r'idAsignatura=(\d{6,})', href)
    if match:
        return match.group(1)
    # Intento secundario: buscar bloque de 6 dígitos al final
    digits = re.findall(r'\d+', href)
    for d in digits:
        if len(d) == 6: return d
    return None

def scrape_uco():
    urls = [
        {"c": "Veterinaria", "d": "Veterinaria", "u": "https://www.uco.es/organiza/centros/veterinaria/es/planificacion-de-la-ensenanza"},
        {"c": "Veterinaria", "d": "CyTA", "u": "https://www.uco.es/organiza/centros/veterinaria/es/planificacion-ensenanza-cyta"},
        {"c": "Veterinaria", "d": "Nutrición", "u": "https://www.uco.es/organiza/centros/veterinaria/es/planificacion-nutricion"},
        {"c": "ETSIAM", "d": "Agroalimentaria", "u": "https://www.uco.es/etsiam/es/planificacion-guias-agroalimentaria"},
        {"c": "ETSIAM", "d": "Forestal", "u": "https://www.uco.es/etsiam/es/planificacion-guias-forestal"},
        {"c": "ETSIAM", "d": "Enología", "u": "https://www.uco.es/etsiam/es/planificacion-guias-enologia"},
        {"c": "Medicina", "d": "Enfermería", "u": "https://www.uco.es/organiza/centros/medicinayenfermeria/es/planificacion-de-la-ensenanza-enf"},
        {"c": "Medicina", "d": "Fisioterapia", "u": "https://www.uco.es/organiza/centros/medicinayenfermeria/es/planificacion-ensenanza-fis"},
        {"c": "Medicina", "d": "Medicina", "u": "https://www.uco.es/medicinayenfermeria/es/planificacion-ensenanza-med"},
        {"c": "Ciencias", "d": "Biología", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-de-la-ensenanza"},
        {"c": "Ciencias", "d": "Bioquímica", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-bioquimica"},
        {"c": "Ciencias", "d": "Biotecnología", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-biotecnologia"},
        {"c": "Ciencias", "d": "Ambientales", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-ambientales"},
        {"c": "Ciencias", "d": "Física", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-fisica"},
        {"c": "Ciencias", "d": "Química", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-quimica"},
        {"c": "Ciencias", "d": "Matemáticas", "u": "https://www.uco.es/organiza/centros/ciencias/es/planificacion-ensenanza-matematicas-filosofia"},
        {"c": "Filosofía", "d": "Cine", "u": "https://www.uco.es/filosofiayletras/es/grados/gr-cine-y-cultura#planificacion"},
        {"c": "Filosofía", "d": "Historia", "u": "https://www.uco.es/filosofiayletras/es/grados/gr-historia#planificacion"},
        {"c": "Derecho", "d": "Derecho", "u": "https://www.uco.es/organiza/centros/derecho/es/planificacion-de-la-ensenanza-derecho.html"},
        {"c": "EPSC", "d": "Ingenierías", "u": "https://www.uco.es/eps/es/programas-de-asignaturas"},
        {"c": "Trabajo", "d": "Relaciones Laborales", "u": "https://www.uco.es/trabajo/es/grelacioneslaborales-planificacion"},
        {"c": "Belmez", "d": "Ing. Civil", "u": "https://www.uco.es/organiza/centros/EPSBelmez/es/planificacion-ensenanza-ing-civil"}
    ]

    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for item in urls:
        print(f"--> Analizando {item['d']}...")
        try:
            res = requests.get(item['u'], headers=headers, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            degree_node = {"center": item['c'], "degree": item['d'], "subjects": []}
            
            panels = soup.select('.panel-default')
            for panel in panels:
                title_el = panel.select_one('.panel-title')
                if not title_el: continue
                title_text = title_el.get_text(strip=True)
                
                # Detectar año real
                year_match = re.search(r'(\d)[ºo]', title_text)
                current_year = int(year_match.group(1)) if year_match else 1
                if "Primero" in title_text: current_year = 1
                elif "Segundo" in title_text: current_year = 2
                elif "Tercero" in title_text: current_year = 3
                elif "Cuarto" in title_text: current_year = 4

                table = panel.select_one('table')
                if not table: continue
                
                for row in table.select('tr'):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 2: continue
                    
                    # El nombre suele ser la primera celda que no sea solo un número
                    name = cells[0].get_text(strip=True)
                    if not name or name.isdigit() or len(name) < 4 or name in ["1º", "2º", "3º", "4º"]:
                        name = cells[1].get_text(strip=True) if len(cells) > 1 else ""

                    if any(ex in name.upper() for ex in ["TFG", "TRABAJO FIN", "PRACTICUM", "PRÁCTICAS"]): continue
                    if name.upper() in ["ASIGNATURA", "NOMBRE", "CURSO"]: continue

                    # Buscar enlace de la guía (el que contiene el código real)
                    guide_link = row.find('a', href=re.compile(r'idAsignatura='))
                    if not guide_link:
                        # Reintento buscando enlaces que contengan "25-26" o "24-25"
                        guide_link = row.find('a', string=re.compile(r'25-26|24-25'))

                    if guide_link and guide_link.has_attr('href'):
                        sub_code = get_code(guide_link['href'])
                        if sub_code:
                            # Detectar semestre por posición o texto
                            row_html = str(row).upper()
                            semester = 1 if ("1º" in row_html or "PRIMER" in row_html) else 2
                            
                            degree_node["subjects"].append({
                                "year": current_year,
                                "name": name,
                                "code": sub_code,
                                "semester": semester
                            })

            results.append(degree_node)
            print(f"   [OK] {len(degree_node['subjects'])} asignaturas encontradas.")
            time.sleep(0.3)
        except Exception as e:
            print(f"   [ERROR] en {item['d']}: {e}")

    out = "/sdcard/Download/uco_master_ingest.json" if os.path.exists("/sdcard") else "uco_master_ingest.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"\nTAREA COMPLETADA. JSON real en: {out}")

if __name__ == "__main__":
    scrape_uco()
