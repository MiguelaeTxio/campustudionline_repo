# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/ual_harvester_v1.py
import requests
import json
import time
import os
import sys

"""
UAL Data Harvester v1
---------------------
Target: Universidad de Almería Public JSON API
Objective: Retrieve full catalog of Degree (Grado) academic plans.
"""

# Configuration
BASE_URL = "https://campus.ual.es/webual/json/academica"
OUTPUT_FILE = "ual_raw_data.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.ual.es/",
    "Origin": "https://www.ual.es"
}

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [UAL-HARVESTER] {msg}")

def fetch_json(url, retries=3):
    """Fetches JSON from URL with retry logic."""
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                try:
                    return r.json()
                except json.JSONDecodeError:
                    log(f"Error: Invalid JSON response from {url}")
                    return None
            elif r.status_code == 404:
                return None # Resource not found
            else:
                log(f"Warning: HTTP {r.status_code} for {url} (Retry {i+1}/{retries})")
                time.sleep(1)
        except Exception as e:
            log(f"Error fetching {url}: {e} (Retry {i+1}/{retries})")
            time.sleep(1)
    return None

def main():
    log("--- Starting UAL Data Harvest ---")
    
    # 1. Get Degree Catalog
    degrees_url = f"{BASE_URL}/titulaciones/GRA/es"
    log(f"Fetching catalog: {degrees_url}")
    
    catalog_data = fetch_json(degrees_url)
    if not catalog_data or 'planes' not in catalog_data:
        log("FATAL: Could not retrieve degree catalog. Aborting.")
        return

    planes_raw = catalog_data['planes']
    active_planes = [p for p in planes_raw if p.get('cod_plan') or p.get('referencia')]
    
    log(f"Found {len(active_planes)} degree plans.")
    
    final_data = []
    
    # 2. Iterate and Fetch Details
    for idx, plan in enumerate(active_planes):
        plan_code = plan.get('referencia') or plan.get('cod_plan')
        plan_name = plan.get('nom_plan', 'Unknown Degree')
        
        log(f"Processing [{idx+1}/{len(active_planes)}]: {plan_name} (Code: {plan_code})")
        
        if not plan_code:
            continue

        # Fetch structural details
        details_url = f"{BASE_URL}/planestudios/{plan_code}/es"
        structure_data = fetch_json(details_url)
        
        degree_record = {
            'meta': plan,
            'structure': structure_data,
            'fetched_at': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if structure_data:
            subjects_count = 0
            if 'asignaturas' in structure_data:
                subjects_count = len(structure_data['asignaturas'])
            elif isinstance(structure_data, list):
                subjects_count = len(structure_data)
            log(f"  -> Success. Retrieved structure data ({subjects_count} items potentially).")
        else:
            log(f"  -> Warning: No structural data returned.")

        final_data.append(degree_record)
        time.sleep(0.2)

    # 3. Save to Disk
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        log(f"SUCCESS. Data saved to local file: {OUTPUT_FILE}")
        log(f"Total records: {len(final_data)}")
    except Exception as e:
        log(f"FATAL: Error saving file: {e}")

if __name__ == "__main__":
    main()
