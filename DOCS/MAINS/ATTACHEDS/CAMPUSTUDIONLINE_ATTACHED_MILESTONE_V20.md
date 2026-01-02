# Anexo del Hito 20: Ingesta UCO - Fase de Consolidación

## 1. Estado de la Situación (LEY SUPREMA)
- **Archivos Persistidos:** Se encuentran en `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/web_scrapping/` un total de **39 fragmentos JSON** (`uco_map_part01.json` a `uco_map_part44.json` con los saltos correspondientes).
- **Integridad:** Los archivos han sido limpiados de TFGs, Prácticas y asignaturas genéricas. Los años académicos están normalizados a enteros.
- **Scripts:** Solo existe `uco_harvester_v19.py`. **NO EXISTEN** scripts de ensamblaje ni procesadores de PDF en el servidor.

## 2. Inventario de Fragmentos JSON
- Bloque 01-09: Salud y Agroalimentaria.
- Bloque 12-17: Ciencias y ADE.
- Bloque 20-31: Letras, Derecho y Educación.
- Bloque 32-38: Ciencias, Ingeniería y Turismo.
- Bloque 40-44: Ciencias, Ingeniería y Trabajo.

## 3. Hoja de Ruta para la Siguiente Sesión (PROHIBIDO INVENTAR)

### Tarea 1: Creación del Ensamblador
- Desarrollar un script `uco_assembler.py` para fusionar los 39 archivos en un único `uco_final_data.json`.
- Validar la estructura de array JSON en cada parte antes de la unión.

### Tarea 2: Extracción de Contenido (PDF Parsing)
- Desarrollar y descargar al local (Android/Termux) el script `uco_pdf_processor.py`.
- Ejecutar en local usando la librería `pdfplumber` para extraer Objetivos, Temarios y Bibliografía de las 1655+ URLs capturadas.
- Generar `uco_final_data_enriched.json` en local y subirlo al servidor.

### Tarea 3: Ingesta en el ORM de Django
- Crear un Management Command para poblar la base de datos a partir del JSON enriquecido.
- Implementar la lógica de `ContentHashFamily` para centralizar asignaturas duplicadas entre diferentes grados.
