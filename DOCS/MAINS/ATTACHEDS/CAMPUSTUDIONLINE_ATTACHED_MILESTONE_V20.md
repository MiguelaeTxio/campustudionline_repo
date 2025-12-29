# Anexo del Hito 20: Refinamiento del Proceso de Scraping e Ingesta UCO

## 1. Visión y Estado
Consolidar la ingesta de 1.540 asignaturas de la UCO (2025/26). La sesión actual ha demostrado la inviabilidad de Selenium en entorno Android/Termux debido a colapsos del renderer y gestión de memoria. Se traslada la fase de cosecha a entorno PC (PCv).

## 2. Definición Técnica de Arquetipos (Matriz UCO)
El motor de scraping debe ser capaz de identificar y procesar los siguientes 8 arquetipos detectados en la auditoría HTML:
- **A:** Medicina (Acordeón Simple).
- **B:** Educación (Acordeón de Doble Nivel).
- **C:** ETSIAM (Pestañas de Titulación + Menciones).
- **D:** Filosofía y Letras (Pestañas + Acordeón).
- **E:** Ciencias del Trabajo (Doble Plan: Activo/Extinguido con IDs duplicados).
- **F:** EPS Córdoba (Acordeón + Tablas divididas por Cuatrimestre).
- **G:** EPS Belmez (Pestañas + Acordeón Multitabla).
- **H:** Ciencias (Doble Plan + Histórico Multicolumna).

## 3. Matriz de Exclusión Agresiva (Cero Ruido)
Está TERMINANTEMENTE PROHIBIDO ingerir registros que contengan:
- **Macro (Contenedores):** antiguo, extinto, extinción, anterior, licenciatura, demo.
- **Micro (Asignaturas):** practicum, prácticas, externas, tfg, tfm, trabajo fin, seminario, intercambio, clínica, rotatorio, mantenimiento, laboratorio.
- **Excepción de Protección:** NO excluir "Trabajo Social" ni "Derecho del Trabajo".

## 4. Hoja de Ruta para la Sesión en PC (LEY SUPREMA)
### Paso 1: Cosecha en PC (Harvester V18)
- Ejecutar `uco_harvester_pc.py` en entorno local.
- Asegurar la generación de `uco_master_map.json` (Válidas) y `uco_excluded_log.json` (Auditoría).

### Paso 2: Fusión de Contenido (Processor V5)
- El usuario debe facilitar `uco_data_backup.json` (archivo de 11MB generado en Termux con el contenido de los PDFs).
- Ejecutar `uco_pdf_processor.py` (Versión Fusión) para inyectar el contenido del backup en el mapa limpio generado por el PC.
- El resultado debe ser un `uco_data_final.json` con Nombres, Ramas y Años 100% verificados.

### Paso 3: Ingesta en Servidor (Importador V9)
- Subir `uco_data_final.json` a la carpeta `/data/` del servidor.
- Ejecutar `python manage.py import_uco_data --purge`.
- El comando DEBE realizar la purga manual por niveles (ContentRequest -> PendingContentTask -> Subject -> AcademicYear) para evitar errores de integridad referencial (IntegrityError 1048/1451) en MySQL.

## 5. Verificación de Integridad
- Los años académicos de Medicina deben ser correlativos (1º a 6º).
- Las ramas deben ser: Artes y Humanidades, Ciencias, Ciencias de la Salud, Ciencias Sociales y Jurídicas, Ingeniería y Arquitectura.
