# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos

## 1. Visión
Optimizar la ingesta de datos académicos (UCO) mediante ejecución local en Termux y filtros de integridad.

## 2. Objetivos Específicos
*   Eliminar duplicados geográficos e idiomáticos mediante Regex.
*   Desarrollar scraper para la Universidad de Córdoba (UCO).
*   Implementar flujo de trabajo local (Termux) -> Servidor (JSON).

## 3. Estado Actual
*   **Estado:** EN PROGRESO

## 4. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
### Paso 1: Auditoría de Scrapers Existentes
*   Analizar `academic_structure/management/commands/import_ugr_data.py`.
### Paso 2: Desarrollo Scraper UCO (Local Termux)
*   Crear script `uco_scraper.py` con lógica de limpieza Regex.
### Paso 3: Ingesta en Servidor
*   Crear management command `import_uco_data` para procesar el JSON.
