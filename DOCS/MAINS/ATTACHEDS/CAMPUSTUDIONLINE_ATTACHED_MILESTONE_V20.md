# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos

## 1. Visión
Consolidar la ingesta masiva de datos académicos de la Universidad de Córdoba (UCO) para el curso 2025/26 mediante el procesamiento de archivos JSON estructurados.

## 2. Objetivos Alcanzados (Sesión Actual)
*   **Cosecha Universal UCO**: Identificación de 1.336 códigos de asignatura únicos mediante navegación real por los hubs de facultades.
*   **Filtrado Estricto**: Exclusión de Dobles Grados, Itinerarios Bilingües y códigos administrativos de intercambio.
*   **Extracción de Contenidos**: Procesamiento local en Termux mediante el motor `pdfplumber`, capturando Objetivos de Aprendizaje, Esquemas de Contenidos y Bibliografía Fundamental del 100% de las guías existentes.
*   **Preparación de Ingesta**: Generación y subida al servidor de `/data/uco_data_final.json`.

## 3. Estado Actual
*   **Estado:** EN PROGRESO (Fase de Ingesta iniciada).

## 4. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
### Paso 1: Creación del Management Command `import_uco_data`
*   Desarrollar el script en `academic_structure/management/commands/`.
*   Implementar lógica de clasificación de Ramas (Knowledge Branches) basada en el Hub de origen del JSON.
*   Asegurar la creación atómica de la jerarquía: University (UCO) -> Branch -> Degree -> AcademicYear -> Subject.

### Paso 2: Ejecución e Integridad
*   Ejecutar la ingesta utilizando `python -m dotenv run python manage.py import_uco_data`.
*   Verificar la persistencia de los campos JSON (`learning_objectives`, `course_content_outline`, `bibliography`) en el modelo `Subject`.

### Paso 3: Deduplicación por Hash (Hito 20.1)
*   Ejecutar `calculate_content_hashes` para agrupar asignaturas idénticas bajo `ContentHashFamily`.
