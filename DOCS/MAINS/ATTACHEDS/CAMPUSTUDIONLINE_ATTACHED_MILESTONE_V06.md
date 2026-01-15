# Hito 6: Sistema de Autoevaluaciones con IA (EMULADOR UGR - RECONSTRUCCIÓN V4)

**Estado:** 🚧 EN DESARROLLO (Nueva Arquitectura de Precisión)
**Modelo Vinculante:** `gemini-3-flash-preview`

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### FASE 1: Re-arquitectura del Modelo y Selección (UI)
1.  **Modificación del Modelo `Assessment`:**
    *   Sustituir el campo `target_segment` (choices Q1, Q2, Q3) por un `JSONField` llamado `selection_range` que almacenará los índices o slugs de los temas del `master_schema` seleccionados por el usuario.
    *   Añadir campos de texto `reading_stimulus` y `listening_transcript` para persistir los materiales generados en el paso 1 del pipeline.
2.  **Vista de Configuración de Examen:**
    *   Implementar una vista que parsee el `master_schema` del contenido original y lo presente en una lista de selección o slider doble.
3.  **Frontend de Selección:**
    *   Diseñar el formulario de selección de temas previo a la creación del objeto `Assessment`.

### FASE 2: El Motor UGR (Pipeline de 3 Pasos en `tasks.py`)
1.  **Paso 1 (Generación de Estímulo):** Petición a Gemini 3 para crear un texto de Reading (500 palabras) y un guion de Listening (200 palabras) inéditos, basados estrictamente en los temas seleccionados.
2.  **Paso 2 (Generación de Ítems de Test):** Petición para generar 6 preguntas `multiple_choice` (4 Reading + 2 Listening) basadas en el estímulo del Paso 1.
3.  **Paso 3 (Generación de Producción):** Petición para las tareas de Writing y Speaking.

### FASE 3: UX y Presentación
1.  **Sidebar de Referencia:** Modificar la Sidebar para que cargue exclusivamente el contenido de `assessment.reading_stimulus`.
2.  **Hardening MathJax:** Asegurar que MathJax ignore la Sidebar para evitar conflictos con los símbolos `#` del Markdown.
