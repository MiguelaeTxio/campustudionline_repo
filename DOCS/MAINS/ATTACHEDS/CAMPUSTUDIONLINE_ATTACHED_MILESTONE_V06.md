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
# ESTADO: EN PROGRESO (FASE 6: GENERACIÓN SEGMENTADA - PENDIENTE ORQUESTADOR)

## 1. RESUMEN TÉCNICO DE LA SESIÓN
*   **Hito 37 - SDK v1 Sync:** `system_instruction` correctamente integrado en `core/services/gemini_service.py` (`GenerateContentConfig`), verificado con la documentación oficial.
*   **Hito 6 - Tracking y Costes:** `api_key_name` añadido a `assessment_v2/models/tracking.py` y el `TrackingService` actualizado para registrarlo, cumpliendo requisitos de auditoría.
*   **Hito 6 - Refinamiento de Reporting:** `GradingOrchestrator` en `assessment_v2/services/engine/logic.py` extendido para integrar la taxonomía de feedback (FB_*) y generar el resumen cualitativo ("Voz del Catedrático").
*   **Hito 6 - Arquitectura Skeleton-First:** Documentación de la constelación V06 actualizada (`V06DOC_STRUCTURE.md`, `V06DOC_ROADMAP.md`, `V06DOC_TEMPLATES.md`) para reflejar la estrategia de generación segmentada (Esqueleto Python + Llenado Atómico IA).
*   **Hito 6 - Estrategia de Lenguas:** `assessment_v2/services/engine/strategies/languages.py` actualizado con `get_section_plan()` y prompts adaptados para la generación atómica, incluyendo memoria de contexto y schema formal OpenAPI 3.0.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**OBJETIVO:** Finalizar la implementación de la Arquitectura de Generación Segmentada (Skeleton-First) y validar su robustez.

### TAREAS CRÍTICAS (ORDEN OBLIGATORIO)

1.  **IMPLEMENTACIÓN DEL BUCLE EN ORQUESTADOR:**
    *   Refactorizar `orchestrator/tasks.py:generate_exam_task` para implementar el bucle de generación de ítems sección por sección.
    *   Asegurar el manejo del rango de temario seleccionado (context_text).
    *   Gestionar la memoria de ítems ya generados (`generated_item_titles`) para evitar repeticiones.

2.  **TESTEO INTEGRAL Y VBO:**
    *   Realizar pruebas exhaustivas del flujo completo (creación de examen, generación por secciones, parseo JSON, registro de tracking) con diversas asignaturas y contextos.
    *   Obtener el Visto Bueno (VBO) para la Fase 6 del Hito.

---
**DIRECTRIZ TÉCNICA:** La próxima sesión se inicia cargando la constelación documental V06 y este anexo actualizado. La prioridad es la finalización y validación del orquestador.
