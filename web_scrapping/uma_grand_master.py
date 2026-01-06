import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import json
import time
import io
import re
import os

try:
    import pdfplumber
except ImportError:
    import sys
    print("[FATAL] 'pdfplumber' no instalado.")
    sys.exit(1)

BASE_URL = "https://sara.uma.es/pls/apex/"
PDF_BASE = "https://sara.uma.es"
OUTPUT_FILE = '/sdcard/Download/uma_universal_harvest.json'

def clean_text_list(raw_text):
    if not raw_text: return []
    lines = [l.strip() for l in raw_text.split('\n') if len(l.strip()) > 5]
    cleaned = []
    for l in lines:
        if re.match(r'^\d+$', l): continue
        if "guía docente" in l.lower(): continue
        item = re.sub(r'^\s*(\d+[\.\)]|[-•·])\s*', '', l).strip()
        if item: cleaned.append(item)
    return cleaned

def process_pdf_content(raw_text):
    if not raw_text: return None
    t = raw_text.lower()
    patterns = {
        'objectives': r'(?:objetivos|competencias|resultados de aprendizaje)',
        'content': r'(?:contenidos|temario|programa de la asignatura|bloques temáticos)',
        'bibliography': r'(?:bibliografía|referencias|fuentes de información)',
        'stop': r'(?:evaluación|sistema de evaluación|metodología)'
    }
    idx = {k: re.search(v, t).start() if re.search(v, t) else -1 for k, v in patterns.items()}
    found = sorted([(k, v) for k, v in idx.items() if v != -1 and k != 'stop'], key=lambda x: x[1])
    
    res = {'learning_objectives': [], 'course_content_outline': [], 'bibliography': {"references": []}}
    for i, (name, start) in enumerate(found):
        end = found[i+1][1] if i < len(found)-1 else (idx['stop'] if idx['stop'] > start else len(raw_text))
        fragment = raw_text[start:end].split('\n', 1)[-1] if '\n' in raw_text[start:end] else ""
        if name == 'objectives': res['learning_objectives'] = clean_text_list(fragment)
        elif name == 'content': res['course_content_outline'] = clean_text_list(fragment)
        elif name == 'bibliography': res['bibliography'] = {"references": clean_text_list(fragment)}
    return res

def recolectar_uma(session, center_id, degree_id, year, center_name, degree_name):
    url_listado = (
        f"{BASE_URL}f?p=101:1:::::"
        f"INICIO_LOV_TIPO_ESTUDIO,INICIO_LOV_CURSO_ACAD,"
        f"INICIO_LOV_CENTROS,INICIO_LOV_TITULACIONES,"
        f"INICIO_LOV_CICLOS,INICIO_LOV_CURSOS,INICIO_BUSCAR:"
        f"3,2025,{center_id},{degree_id},1,{year}"
    )
    
    try:
        r = session.get(url_listado, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all('a', href=re.compile(r'f\?p=101:3:.*P3_ID:'))
        
        vistos = set()
        for l in links:
            qs = parse_qs(urlparse(l['href']).query)
            if "P3_ID" not in qs: continue
            asig_id = qs["P3_ID"][0]
            if asig_id in vistos: continue
            vistos.add(asig_id)

            nombre_asig = "Desconocida"
            fila = l.find_parent('tr')
            if fila:
                celdas = fila.find_all('td')
                if len(celdas) > 1: nombre_asig = celdas[1].get_text(strip=True)

            url_detalle = urljoin(BASE_URL, l['href'])
            rd = session.get(url_detalle, timeout=15)
            soup_d = BeautifulSoup(rd.text, "html.parser")
            link_pdf = soup_d.find("a", string=lambda t: t and "Consultar la guía docente" in t)
            
            if link_pdf:
                pdf_url = urljoin(PDF_BASE, link_pdf['href'])
                try:
                    rp = session.get(pdf_url, timeout=15)
                    with pdfplumber.open(io.BytesIO(rp.content)) as pdf:
                        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                        data = process_pdf_content(text)
                        
                        record = {
                            'center_name': center_name, 'degree_name': degree_name,
                            'name': nombre_asig, 'year': year, 'url_source': url_detalle,
                            'pdf_url': pdf_url, 'status': 'READY'
                        }
                        if data: record.update(data)
                        
                        current_db = []
                        if os.path.exists(OUTPUT_FILE):
                            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f: current_db = json.load(f)
                        current_db.append(record)
                        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f: json.dump(current_db, f, ensure_ascii=False, indent=4)
                        print(".", end="", flush=True)
                except: pass
    except: pass

def obtener_centros(session):
    r = session.get(f"{BASE_URL}f?p=101:1", timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    select = soup.find("select", {"name": "INICIO_LOV_CENTROS"})
    return {o.get("value"): o.get_text(strip=True) for o in select.find_all("option") if o.get("value") and o.get("value").isdigit()}

def obtener_titulaciones(session, center_id):
    url = (f"{BASE_URL}wwv_flow.show?p_flow_id=101&p_flow_step_id=1"
           f"&p_instance=0&request=PLUGIN=apex.widget.selectlist&x01=INICIO_LOV_TITULACIONES&x02={center_id}")
    r = session.get(url, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    return {o.get("value"): o.get_text(strip=True) for o in soup.find_all("option") if o.get("value") and o.get("value").isdigit()}

def main():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    centros = obtener_centros(session)
    for c_id, c_name in centros.items():
        print(f"\n[ORQ] Centro: {c_name}")
        grados = obtener_titulaciones(session, c_id)
        for d_id, d_name in grados.items():
            print(f"  [ORQ] Grado: {d_name}")
            for curso in (1, 2, 3, 4):
                print(f"    [ORQ] Curso {curso}: ", end="", flush=True)
                recolectar_uma(session, c_id, d_id, curso, c_name, d_name)
                print(" OK")

if __name__ == "__main__":
    main()
