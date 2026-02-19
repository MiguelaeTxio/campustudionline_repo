<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md -->

### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse OBLIGATORIAMENTE con la siguiente constelación documental:
*   V06DOC_ARCHETYPES.md
*   V06DOC_SUBARCHETYPES.md
*   V06DOC_SUBDIVISIONS.md
*   V06DOC_BLOCKS.md
*   V06DOC_WIDGETS.md
*   V06DOC_METADATA.md
*   V06DOC_LEVELS.md
*   V06DOC_TEMPLATES.md
*   V06DOC_STRUCTURE.md
*   V06DOC_LOGIC_MAPPING.md
*   V06DOC_ROADMAP.md

**PROTOCOLO DEL MANIFIESTO (FUENTE DE LA VERDAD):**
El archivo V06DOC_ROADMAP.md es la ÚNICA fuente de verdad para el progreso. 
1. Es OBLIGATORIO auditar este archivo al inicio de cada sesión.
2. Es MANDATORIO actualizar su estado atómico (Checklist) al cierre de cada sesión.

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: RECTIFICACIÓN ESTRUCTURAL COMPLETADA (FASE 6 - EPI)

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA RECTIFICACIÓN (SESIÓN EPI)
*   **Alineación Documental:** Se han rectificado `V06DOC_LEVELS` y `V06DOC_LOGIC_MAPPING` para integrar la Matriz de Inmersión Lingüística oficial de la UGR.
*   **Identidad Cognitiva:** Implementada la clasificación de asignaturas vía API (`gemini-2.5-flash-lite`) en `logic.py`, eliminando los diccionarios Regex obsoletos.
*   **Estrategias Espejo:** Las 5 estrategias (`tech`, `health`, `social`, `hum`, `lang`) han sido reescritas bajo el modelo Atómico (Skeleton-First), implementando `get_section_plan` y esquemas de salida compatibles con OpenAPI 3.0.
*   **Validación:** Superada la auditoría híbrida (IA + Python). El sistema deduce correctamente la inmersión (Chino A1=Vehicular, Italiano C1=Total).

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**PROHIBIDO AVANZAR SIN CUMPLIR ESTOS PUNTOS SEGÚN V06DOC_STRUCTURE:**

1.  **REFACTORIZACIÓN DEL ORQUESTADOR (`orchestrator/tasks.py`):**
    *   Modificar el bucle de generación para que sea iterativo por sección.
    *   Implementar la creación previa de `ExamSection` antes de las llamadas a la IA.
    *   Inyectar el `immersion_mode` y `pedagogical_level` en los prompts atómicos.
2.  **REFACTORIZACIÓN DE UI (`exam_take.html`):**
    *   Eliminar widgets hardcodeados.
    *   Implementar la lógica dinámica de carga de widgets basándose en el `widget_id` del contrato JSON.
3.  **SISTEMA DE REINTENTOS:**
    *   Implementar el protocolo de resiliencia (3 reintentos / 10 min) en caso de fallo de API de clasificación.

