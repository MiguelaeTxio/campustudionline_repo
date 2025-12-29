import json
import time
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ==========================================
# CONFIGURACIÓN REAL (URL VERIFICADA)
# ==========================================
START_URL = "https://www.uco.es/grados/listado-general-por-centro"
OUTPUT_FILE = "uco_master_map.json"
EXCLUDED_TERMS = ["practicum", "prácticas", "externas", "tfg", "tfm", "trabajo fin", "seminario", "intercambio", "clínica", "rotatorio", "mantenimiento", "laboratorio", "reconocimiento"]
SAFE_WORDS = ["trabajo social", "derecho del trabajo"]

class UCOHarvesterV18:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.results = []

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def get_planning_url(self, grade_name, center_id):
        """Construye la URL de planificación usando los planos de las muestras"""
        cid = center_id.lower()
        gn = grade_name.lower()
        
        if "veterinaria" in cid:
            return "https://www.uco.es/organiza/centros/veterinaria/es/planificacion-de-la-ensenanza"
        if "medicina" in cid:
            return "https://www.uco.es/medicinayenfermeria/es/planificacion-ensenanza-med"
        if "derecho" in cid:
            return "https://www.uco.es/derechoyccee/es/planificacion-de-la-ensenanza-derecho.html"
        if "fce" in cid: # Educación
            return "https://www.uco.es/educacion/es/infantil-planificacion-de-la-ensenanza"
        if "etsiam" in cid:
            # Reconstruir slug para ETSIAM
            slug = gn.replace("grado en ", "").replace("ingeniería ", "").split(" ")[0]
            return f"https://www.uco.es/etsiam/es/planificacion-guias-{slug}"
        if "ciencias" in cid:
            return "https://www.uco.es/ciencias/es/planificacion-de-la-ensenanza"
        if "trabajo" in cid:
            return "https://www.uco.es/trabajo/es/grelacioneslaborales-planificacion"
        
        return None

    def run(self):
        print(f"🕷️  Iniciando Cosecha en la URL CORRECTA: {START_URL}")
        self.driver.get(START_URL)
        time.sleep(3)
        
        soup_index = BeautifulSoup(self.driver.page_source, 'html.parser')
        panels = soup_index.find_all('div', class_='panel')
        
        grades_list = []
        for p in panels:
            title = p.find(class_='panel-title')
            content = p.find('div', class_='panel-collapse')
            if not title or not content: continue
            
            center_id = content['id']
            links = content.find_all('a', href=True)
            for a in links:
                if "grado" in a.get_text().lower():
                    grades_list.append({
                        "name": self.clean_text(a.get_text()),
                        "center_id": center_id
                    })

        print(f"🎯 Detectados {len(grades_list)} grados potenciales.")

        for grade in grades_list:
            target_url = self.get_planning_url(grade['name'], grade['center_id'])
            if not target_url: continue

            print(f"🚀 Navegando a: {grade['name']} -> {target_url}")
            try:
                self.driver.get(target_url)
                time.sleep(2)

                # Abrir pestañas si existen (ETSIAM, etc.)
                try:
                    tabs = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'docentes') or contains(@href, 'planificacion')]")
                    for t in tabs: 
                        if t.is_displayed(): t.click(); time.sleep(0.5)
                except: pass

                soup_grade = BeautifulSoup(self.driver.page_source, 'html.parser')
                # Bloque 2025/26 prioritario
                container = soup_grade.find('div', id='2025-2026') or soup_grade.find('div', id='demo2') or soup_grade
                
                subj_in_grade = []
                panels_grade = container.find_all('div', class_='panel')
                for pg in panels_grade:
                    header = pg.find(class_='panel-title')
                    if not header: continue
                    h_text = header.get_text().lower()
                    
                    # Identificar Año del acordeón
                    year = 1
                    if "1" in h_text or "primer" in h_text: year = 1
                    elif "2" in h_text or "segundo" in h_text: year = 2
                    elif "3" in h_text or "tercer" in h_text: year = 3
                    elif "4" in h_text or "cuarto" in h_text: year = 4
                    elif "5" in h_text or "quinto" in h_text: year = 5
                    elif "6" in h_text or "sexto" in h_text: year = 6
                    else: continue

                    table = pg.find('table')
                    if not table: continue
                    
                    for row in table.find_all('tr'):
                        cells = [self.clean_text(c.get_text()) for c in row.find_all(['td', 'th'])]
                        if len(cells) < 2: continue
                        name_subject = max(cells, key=len)
                        
                        if any(safe in name_subject.lower() for safe in SAFE_WORDS):
                            pass
                        elif any(exc in name_subject.lower() for exc in EXCLUDED_TERMS) or len(name_subject) < 5:
                            continue

                        if not any(s['name'] == name_subject for s in subj_in_grade):
                            subj_in_grade.append({"name": name_subject, "year": year})
                
                if subj_in_grade:
                    self.results.append({"degree": grade['name'], "subjects": subj_in_grade})
                    print(f"   ✅ {len(subj_in_grade)} asignaturas.")

            except Exception as e:
                print(f"   ❌ Error procesando {grade['name']}: {e}")

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        self.driver.quit()
        print(f"\n🎉 EXTRACCIÓN COMPLETA. JSON generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    UCOHarvesterV18().run()
