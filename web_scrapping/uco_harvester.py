import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin

def get_soup(url, session):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = session.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return BeautifulSoup(r.text, 'lxml')
    except: pass
    return None

def is_excluded(name):
    exclusions = ["doble", "pceo", "biling", "english", "itinerario conjunto", "ka131"]
    return any(x in name.lower() for x in exclusions)

def run_harvest(course_year="2025-26"):
    session = requests.Session()
    hubs = {
        "Ciencias": "https://www.uco.es/organiza/centros/ciencias/es/",
        "Derecho": "https://www.uco.es/derechoyccee/es/",
        "Filosofia": "https://www.uco.es/filosofiayletras/es/",
        "Educacion": "https://www.uco.es/educacion/es/",
        "Medicina": "https://www.uco.es/medicinayenfermeria/es/",
        "Veterinaria": "https://www.uco.es/veterinaria/es/"
    }
    master_data = {"university": "UCO", "course": course_year, "subjects": []}
    all_codes = set()

    for c_name, hub_url in hubs.items():
        soup_hub = get_soup(hub_url, session)
        if not soup_hub: continue
        degree_links = soup_hub.find_all('a', string=re.compile(r'Grado|Gr\.', re.I))
        if not degree_links: degree_links = soup_hub.find_all('a', href=re.compile(r'grado-|gr-'))
        
        urls_grados = set()
        for l in degree_links:
            name, href = l.get_text(strip=True), l.get('href')
            if href and not is_excluded(name) and len(name) > 5:
                urls_grados.add((urljoin(hub_url, href), name))

        for g_url, g_name in urls_grados:
            soup_landing = get_soup(g_url, session)
            if not soup_landing: continue
            codes_to_process = set(re.findall(r'\b([16]\d{5})\b', soup_landing.get_text()))
            
            p_link = None
            sidebar = soup_landing.find(['aside', 'div'], id='sidebar') or soup_landing.find('div', class_='menu-interes')
            if sidebar: p_link = sidebar.find('a', string=re.compile(r'Planificación', re.I))
            if not p_link: p_link = soup_landing.find('a', href=re.compile(r'planificacion', re.I))

            if p_link:
                res_plan = session.get(urljoin(g_url, p_link.get('href')), timeout=10)
                if res_plan.status_code == 200:
                    codes_to_process.update(re.findall(r'\b([16]\d{5})\b', res_plan.text))

            for c in codes_to_process:
                if c not in all_codes:
                    all_codes.add(c)
                    master_data["subjects"].append({
                        "code": c, "degree": g_name,
                        "pdf": f"http://www.uco.es/eguiado/guias/{course_year}/{c}es_{course_year}.pdf"
                    })
        time.sleep(1)

    with open("uco_master_map.json", "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run_harvest()
