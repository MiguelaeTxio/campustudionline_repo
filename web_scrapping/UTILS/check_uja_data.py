import json

# Busca asignaturas de Fisioterapia para ver sus años
with open('/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/data/uja_final_data.json', 'r') as f:
    data = json.load(f)

print("🔍 INSPECCIÓN DE DATOS: GRADO EN FISIOTERAPIA")
found = False
for degree in data:
    if "Fisioterapia" in degree['degree_name']:
        found = True
        print(f"Titulación: {degree['degree_name']}")
        print(f"Total Asignaturas: {len(degree['subjects'])}")
        
        # Conteo de años
        years = {}
        for s in degree['subjects']:
            y = s.get('year', 'Unknown')
            years[y] = years.get(y, 0) + 1
            
        print("Distribución de años en el JSON:")
        for y, count in years.items():
            print(f"  - Año {y}: {count} asignaturas")
            
        # Muestra 3 ejemplos
        print("\nEjemplos:")
        for s in degree['subjects'][:3]:
            print(f"  - {s['name']} -> Año {s.get('year')}")
        break

if not found:
    print("❌ No se encontró el Grado en Fisioterapia en el JSON.")
