# Hito 20: Refinamiento del Proceso de Scraping de Datos (UAL)

## Estado de la Sesión: ÉXITO TOTAL (Recuperación APEX)
La sesión ha logrado revertir el fracaso previo mediante ingeniería inversa de los servicios internos de la Universidad de Almería (UAL), logrando una extracción de datos enriquecidos superior a la media de otras instituciones.

## Logros Técnicos:
1.  **Ingeniería Inversa de API:** Localización de los endpoints internos JBoss (`campus.ual.es/ual/api`) y Legacy JSP mediante el análisis de definiciones de servicios Angular.
2.  **Edge Processing (PDF Analysis):** Implementación de un procesador local con `pdfplumber` que descarga y analiza las Guías Docentes oficiales de la UAL.
3.  **Extracción de Rich Content:** Segmentación heurística de Objetivos de Aprendizaje (`learning_objectives`) y Temario Detallado (`course_content_outline`) directamente desde los PDFs oficiales de 2025-26.
4.  **Ingesta Masiva:** Procesamiento de 1972 asignaturas (1846 previamente cacheadas y 126 nuevas).
5.  **Normalización de Branding:** Actualización del nombre de la institución a "Institución Académica de Almería" para coherencia con el estándar de la plataforma.

## Archivos Involucrados:
- `web_scrapping/ual_full_harvester.py` (Extracción Estructural)
- `web_scrapping/ual_pdf_processor_v2.py` (Extracción de Contenido Rico)
- `academic_structure/management/commands/import_ual_data.py` (Importador)
- `SWAP/normalize_ual_name.py` (Normalizador de branding)

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
**Objetivo:** Migración Crítica al modelo Gemini 3 Flash.

1.  **Actualización de Entorno:**
    - Modificar `requirements.in`: Fijar `google-genai>=1.51.0`.
    - Ejecutar `pip-compile` y `pip-sync` en el servidor y local (`PCv`).
2.  **Refactorización de `core/services/gemini_service.py`:**
    - Cambiar ID del modelo a `models/gemini-3-flash`.
    - Sustituir `thinking_budget` por `thinking_level` (configurar nivel por defecto en 'medium').
    - Implementar la persistencia y envío de `Thought Signatures` en el historial de mensajes para evitar Errores 400 en sesiones multi-turno.
3.  **Auditoría de Prompts:**
    - Adaptar `DOCS/MAINS/CONTENT_PROMPTS.md` para aprovechar la mayor ventana de contexto y capacidad de razonamiento del nuevo modelo.
4.  **Verificación Empírica:** Generar un material de estudio de prueba y validar que la respuesta incluya los bloques de pensamiento correctos.
