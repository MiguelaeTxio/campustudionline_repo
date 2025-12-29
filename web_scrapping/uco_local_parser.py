import json
import re
import os
import glob
from bs4 import BeautifulSoup

# ==========================================
# CONFIGURACIÓN Y MATRIZ DE EXCLUSIÓN
# ==========================================
INPUT_DIR = os.path.join("web_scrapping", "html_dump")
OUTPUT_FILE = "uco_master_map.json"
LOG_FILE = "uco_excluded_log.json"

EXCLUDED_TERMS = [
    "practicum", "prácticas", "externas", "tfg", "tfm", "trabajo fin", 
    "seminario", "intercambio", "clínica", "rotatorio", "mantenimiento", 
    "laboratorio", "reconocimiento", "antiguo", "extinto", "extinción", 
    "anterior", "licenciatura", "demo"
]
SAFE_WORDS = ["trabajo social", "derecho del trabajo"]

RAMAS_MAP = {
    "Artes y Humanidades": ["filosofía", "letras", "cine", "traducción", "historia", "arte"],
    "Ciencias": ["ciencias", "biología", "química", "física", "bioquímica", "biotecnología", "ambientales"],
    "Ciencias de la Salud": ["medicina", "enfermería", "veterinaria", "fisioterapia", "nutrición"],
    "Ciencias Sociales y Jurídicas": ["derecho", "ade", "educación", "infantil", "primaria", "psicología", "trabajo", "turismo", "relaciones laborales"],
    "Ingeniería y Arquitectura": ["politécnica", "ingeniería", "agronómica", "montes", "enología", "informática", "eléctrica", "civil"]
}

class UCOParserV9:
    def __init__(self):
        self.results = []
        self.excluded_log = []

    def get_rama(self, text):
        text = text.lower()
        for rama, keywords in RAMAS_MAP.items():
            if any(k in text for k in keywords):
                return rama
        return "Ciencias Sociales y Jurídicas" # Default por volumen en UCO

    def is_excluded(self, name):
        name_lower = name.lower().strip()
        if any(safe in name_lower for safe in SAFE_WORDS): return False
        return any(exc in name_lower for exc in EXCLUDED_TERMS)

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def extract_year(self, text):
        text = text.lower()
        if "1" in text or "primero" in text or "primer" in text: return 1
        if "2" in text or "segundo" in text: return 2
        if "3" in text or "tercero" in text or "tercer" in text: return 3
        if "4" in text or "cuarto" in text: return 4
        if "5" in text or "quinto" in text: return 5
        if "6" in text or "sexto" in text: return 6
        return None

    def parse_file(self, file_path):
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Identificar Grado
        title_tag = soup.find(['h2', 'h1', 'title'])
        degree_name = self.clean_text(title_tag.get_text()) if title_tag else filename
        degree_name = degree_name.split('-')[0].strip()
        
        # Ignorar si es el índice general
        if "Listado de Grados" in degree_name: return

        print(f"📦 Procesando Grado: {degree_name}")
        rama = self.get_rama(degree_name + " " + filename)
        
        degree_data = {
            "degree": degree_name,
            "rama": rama,
            "subjects": []
        }

        # Lógica de Acordeones (Arquetipos A, B, D, E, F, G)
        panels = soup.find_all('div', class_='panel')
        
        # Caso especial: Educación (Arquetipo B) - Filtrar solo bloque 2025/26
        target_container = soup.find('div', id='2025-2026')
        if target_container:
            panels = target_container.find_all('div', class_='panel')

        for panel in panels:
            header = panel.find(class_='panel-title')
            if not header: continue
            
            year = self.extract_year(header.get_text())
            if not year: continue # Ignorar secciones que no sean de cursos (ej: "Info")

            table = panel.find('table')
            if not table: continue

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) < 2: continue
                
                # Buscar nombre: suele ser la celda con más texto o con un link que no sea PDF
                texts = [self.clean_text(c.get_text()) for c in cols]
                
                # Heurística: la asignatura no suele ser puramente numérica y tiene longitud > 5
                subject_name = None
                for t in texts:
                    if len(t) > 5 and not t.isdigit() and "guía" not in t.lower() and "ects" not in t.lower():
                        subject_name = t
                        break
                
                if not subject_name or self.is_excluded(subject_name):
                    if subject_name:
                        self.excluded_log.append({"degree": degree_name, "subject": subject_name})
                    continue

                # Evitar duplicados en el mismo grado
                if not any(s['name'] == subject_name for s in degree_data["subjects"]):
                    degree_data["subjects"].append({
                        "name": subject_name,
                        "year": year
                    })

        if degree_data["subjects"]:
            self.results.append(degree_data)
            print(f"   ✅ {len(degree_data['subjects'])} asignaturas.")

    def run(self):
        if not os.path.exists(INPUT_DIR):
            print(f"❌ Error: No existe {INPUT_DIR}")
            return
            
        files = glob.glob(os.path.join(INPUT_DIR, "*.html"))
        for f in files:
            self.parse_file(f)

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.excluded_log, f, ensure_ascii=False, indent=2)

        print(f"\n🚀 Parser finalizado. Mapa maestro generado en {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = UCOParserV9()
    parser.run()
