import requests
from bs4 import BeautifulSoup
import json
import time
import os

# --- CONFIGURACIÓN RUTA ABSOLUTA ANDROID ---
OUTPUT_FILE = "/sdcard/Download/ugr_languages_raw.json"
BASE_URL = "https://grados.ugr.es"
# Lista de slugs de grados a recuperar (los que contienen el catálogo de lenguas)
TARGET_DEGREES = [
    "arabe", "franceses", "ingleses", "modernas", "hispanicos", "clasica"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

def get_subjects(degree_slug):
    url = f"{BASE_URL}/{degree_slug}/plan-de-estudios"
    print(f"   📖 Extrayendo plan: {url}")
    subjects = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # La UGR organiza las asignaturas en tablas dentro de paneles
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Estructura típica UGR: Código | Nombre | Créditos | Tipo
                    code = cols[0].get_text(strip=True)
                    name = cols[1].get_text(strip=True)
                    # El tipo suele estar en la 4ª columna o mediante iconos/clases
                    # Intentamos extraer texto de la columna de tipo si existe
                    subj_type = cols[3].get_text(strip=True) if len(cols) > 3 else "Optativa"
                    
                    if code.isdigit():
                        subjects.append({
                            "code": code,
                            "name": name,
                            "type": subj_type
                        })
        return subjects
    except Exception as e:
        print(f"   ❌ Error en {degree_slug}: {e}")
        return []

def main():
    print("🚜 INICIANDO HARVESTER DE LENGUAS UGR...")
    all_data = []

    for slug in TARGET_DEGREES:
        print(f"\n🎓 Procesando Grado: {slug}")
        subjects = get_subjects(slug)
        if subjects:
            all_data.append({
                "university": "Universidad de Granada",
                "degree_slug": slug,
                "subjects": subjects
            })
            print(f"   ✅ {len(subjects)} asignaturas encontradas.")
        time.sleep(1) # Cortesía con el servidor

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ PROCESO COMPLETADO. Datos en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
