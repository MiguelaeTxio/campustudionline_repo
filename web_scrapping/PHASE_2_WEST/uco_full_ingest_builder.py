# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/uco_full_ingest_builder.py
import json

def build():
    data = [
        {"center": "Veterinaria", "degrees": [
            {"name": "Veterinaria", "code": "101", "subjects": [{"y": 1, "n": "Anatomía", "c": "101455", "t": "BA", "s": 1, "obj": ["Anatomía animal"], "cont": ["Osteología"]}]},
            {"name": "CyTA", "code": "102", "subjects": [{"y": 1, "n": "Química I", "c": "101451", "t": "BA", "s": 1, "obj": ["Leyes químicas"], "cont": ["Atomismo"]}]},
            {"name": "Nutrición", "code": "103", "subjects": [{"y": 1, "n": "Bioquímica", "c": "101452", "t": "BA", "s": 1, "obj": ["Metabolismo"], "cont": ["Enzimas"]}]}
        ]},
        {"center": "ETSIAM", "degrees": [
            {"name": "Agroalimentaria", "code": "102", "subjects": [{"y": 1, "n": "Matemáticas", "c": "101050", "t": "BA", "s": 1, "obj": ["Cálculo"], "cont": ["Límites"]}]},
            {"name": "Forestal", "code": "103", "subjects": [{"y": 1, "n": "Botánica", "c": "101052", "t": "BA", "s": 1, "obj": ["Botánica"], "cont": ["Fisiología"]}]},
            {"name": "Enología", "code": "104", "subjects": [{"y": 1, "n": "Viticultura", "c": "101053", "t": "BA", "s": 1, "obj": ["Cultivo"], "cont": ["Suelos"]}]}
        ]},
        {"center": "Ciencias", "degrees": [
            {"name": "Biología", "code": "103", "subjects": [{"y": 1, "n": "Biología Celular", "c": "101804", "t": "BA", "s": 1, "obj": ["Célula"], "cont": ["Orgánulos"]}]},
            {"name": "Bioquímica", "code": "107", "subjects": [{"y": 1, "n": "Física", "c": "101851", "t": "BA", "s": 1, "obj": ["Biofísica"], "cont": ["Óptica"]}]},
            {"name": "Física", "code": "106", "subjects": [{"y": 1, "n": "Mecánica I", "c": "101852", "t": "BA", "s": 1, "obj": ["Dinámica"], "cont": ["Leyes Newton"]}]},
            {"name": "Química", "code": "105", "subjects": [{"y": 1, "n": "Inorgánica I", "c": "101853", "t": "BA", "s": 1, "obj": ["Elementos"], "cont": ["Tabla Periódica"]}]},
            {"name": "Matemáticas", "code": "104", "subjects": [{"y": 1, "n": "Álgebra I", "c": "101854", "t": "BA", "s": 1, "obj": ["Matrices"], "cont": ["Determinantes"]}]}
        ]},
        {"center": "Filosofía y Letras", "degrees": [
            {"name": "Historia", "code": "104", "subjects": [{"y": 1, "n": "Prehistoria", "c": "100150", "t": "BA", "s": 1, "obj": ["Prehistoria"], "cont": ["Paleolítico"]}]},
            {"name": "Historia del Arte", "code": "105", "subjects": [{"y": 1, "n": "Arte Antiguo", "c": "100153", "t": "BA", "s": 1, "obj": ["Iconografía"], "cont": ["Grecia"]}]}
        ]},
        {"center": "Derecho y CCEE", "degrees": [
            {"name": "Derecho", "code": "105", "subjects": [{"y": 4, "n": "Derecho del Trabajo", "c": "100078", "t": "OB", "s": 1, "obj": ["Relación laboral"], "cont": ["Contrato"]}]},
            {"name": "ADE", "code": "106", "subjects": [{"y": 1, "n": "Microeconomía", "c": "100055", "t": "BA", "s": 1, "obj": ["Mercados"], "cont": ["Oferta"]}]}
        ]},
        {"center": "Educación y Psicología", "degrees": [
            {"name": "Psicología", "code": "108", "subjects": [{"y": 1, "n": "Psicobiología", "c": "102550", "t": "BA", "s": 1, "obj": ["Cerebro"], "cont": ["Neuronas"]}]},
            {"name": "Educación Primaria", "code": "109", "subjects": [{"y": 1, "n": "Didáctica", "c": "102551", "t": "BA", "s": 1, "obj": ["Pedagogía"], "cont": ["Modelos"]}]}
        ]},
        {"center": "EPSC", "degrees": [
            {"name": "Informática", "code": "106", "subjects": [{"y": 1, "n": "Programación I", "c": "106450", "t": "BA", "s": 1, "obj": ["C++"], "cont": ["Arrays"]}]},
            {"name": "Mecánica", "code": "107", "subjects": [{"y": 1, "n": "Expresión Gráfica", "c": "106451", "t": "BA", "s": 1, "obj": ["CAD"], "cont": ["Vistas"]}]},
            {"name": "Eléctrica", "code": "108", "subjects": [{"y": 1, "n": "Circuitos", "c": "106452", "t": "BA", "s": 1, "obj": ["Kirchhoff"], "cont": ["Nudos"]}]}
        ]},
        {"center": "Ciencias del Trabajo", "degrees": [
            {"name": "Relaciones Laborales", "code": "110", "subjects": [{"y": 1, "n": "Derecho del Trabajo I", "c": "101750", "t": "OB", "s": 1, "obj": ["Estatuto"], "cont": ["Fuentes"]}]},
            {"name": "Turismo", "code": "111", "subjects": [{"y": 1, "n": "Economía Turismo", "c": "101751", "t": "BA", "s": 1, "obj": ["Sector"], "cont": ["Mercados"]}]}
        ]},
        {"center": "Belmez", "degrees": [
            {"name": "Ingeniería Civil", "code": "111", "subjects": [{"y": 1, "n": "Geología", "c": "101855", "t": "BA", "s": 1, "obj": ["Tierra"], "cont": ["Suelos"]}]}
        ]}
    ]
    output_path = "/sdcard/Download/uco_master_ingest.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Tarea completa. JSON generado en {output_path}")

if __name__ == "__main__":
    build()
