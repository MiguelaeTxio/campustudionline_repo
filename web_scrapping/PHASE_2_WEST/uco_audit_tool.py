import json
from collections import Counter, defaultdict

def audit():
    try:
        with open('uco_audit_report.json', 'r') as f: audit = json.load(f)
        with open('uco_master_map.json', 'r') as f: master = json.load(f)
        lookup = {s['code']: (s['degree'], s.get('name', 'N/A')) for s in master['subjects']}
        counts = Counter(item['status'] for item in audit)
        print("\n--- RESUMEN ---")
        for s, c in counts.items(): print(f"{s}: {c}")
        print("\n--- DETALLE NOMINAL ---")
        for item in audit:
            deg, name = lookup.get(item['code'], ("?", "?"))
            print(f"[{item['status']}] {item['code']} | {deg[:20]} | {name}")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    audit()
