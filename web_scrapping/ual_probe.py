import requests
from bs4 import BeautifulSoup
import os
import sys
import json
from urllib.parse import urljoin

"""
SCRIPT DE SONDEO - UNIVERSIDAD DE ALMERÍA (UAL)
Objetivo: Descargar HTML crudo del catálogo y una muestra de grado para análisis estructural.
Ejecución: Local (Termux/PC).
"""

# Configuración Inicial (Sujeta a verificación manual)
# URL principal de grados de la UAL
BASE_URL = "https://www.ual.es/estudios/grados"
OUTPUT_DIR = "ual_probe_data"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[OK] Directorio creado: {OUTPUT_DIR}")

def save_html(filename, content):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] HTML guardado: {filepath}")
    return filepath

def probe_catalog():
    print(f"[*] Conectando a {BASE_URL}...")
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        save_html("01_catalogo_index.html", response.text)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Búsqueda heurística de enlaces a grados
        # Buscamos enlaces que contengan 'grados' o 'estudios' y parezcan fichas
        links = soup.find_all('a', href=True)
        candidates = []
        
        print("[*] Analizando enlaces candidatos...")
        for link in links:
            href = link['href']
            text = link.get_text(strip=True)
            
            # Filtros heurísticos (ajustar tras primera ejecución si falla)
            # La UAL suele usar rutas como /estudios/grados/presentacion/XXXX
            if 'grados' in href and len(text) > 5:
                full_url = urljoin(BASE_URL, href)
                candidates.append({
                    'text': text,
                    'url': full_url
                })
        
        # Eliminar duplicados por URL
        unique_candidates = {c['url']: c for c in candidates}.values()
        print(f"[INFO] Detectados {len(unique_candidates)} posibles enlaces a grados.")
        
        # Guardar lista de candidatos para inspección
        with open(os.path.join(OUTPUT_DIR, "candidates.json"), "w", encoding="utf-8") as f:
            json.dump(list(unique_candidates), f, indent=4, ensure_ascii=False)
            
        return list(unique_candidates)

    except Exception as e:
        print(f"[ERROR] Fallo en sonda de catálogo: {e}")
        return []

def probe_degree_detail(url, name):
    print(f"[*] Sondeando detalle de grado: {name}")
    print(f"    URL: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        save_html("02_detalle_grado_ejemplo.html", response.text)
        
        # Intento de buscar pestaña o enlace al PLAN DE ESTUDIOS
        soup = BeautifulSoup(response.text, 'html.parser')
        plan_links = soup.find_all('a', string=lambda t: t and "Plan de" in t)
        
        if plan_links:
            print(f"[INFO] Detectados {len(plan_links)} enlaces a 'Plan de Estudios'.")
            for i, link in enumerate(plan_links):
                href = link['href']
                plan_url = urljoin(url, href)
                print(f"    -> Descargando Plan de Estudios {i+1}: {plan_url}")
                try:
                    r_plan = requests.get(plan_url, headers=HEADERS, timeout=15)
                    save_html(f"03_plan_estudios_{i+1}.html", r_plan.text)
                except Exception as ex:
                    print(f"    [WARN] No se pudo descargar el plan {i+1}: {ex}")
        else:
            print("[WARN] No se detectó enlace explícito a 'Plan de Estudios' en la home del grado.")
            
    except Exception as e:
        print(f"[ERROR] Fallo en sonda de detalle: {e}")

def main():
    ensure_dir()
    candidates = probe_catalog()
    
    if candidates:
        # Elegimos el candidato que parezca más estándar (evitar dobles grados si es posible para empezar)
        target = candidates[0]
        for c in candidates:
            # Preferir un grado simple de informática o similar si aparece para estandarizar
            if "informática" in c['text'].lower() or "computer" in c['text'].lower():
                target = c
                break
        
        probe_degree_detail(target['url'], target['text'])
    else:
        print("[FATAL] No se pudieron extraer candidatos para profundizar. Revisar 01_catalogo_index.html")

if __name__ == "__main__":
    main()
