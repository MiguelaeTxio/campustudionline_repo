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
# ESTADO: REFACTORIZACIÓN TÉCNICA COMPLETADA (DESBLOQUEADO)

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (CSO)
*   **Orquestación Atómica:** Se ha refactorizado `orchestrator/tasks.py` implementando el bucle iterativo por sección y el modelo *Skeleton-First*.
*   **Resiliencia:** Implementado el protocolo de reintentos (3 intentos / 10 min) para la API de clasificación.
*   **UI Dinámica:** Refactorizada `exam_take.html` eliminando lógica hardcodeada. Los widgets se cargan dinámicamente según el `widget_id` del contrato JSON.
*   **Calidad de Código:** Superada la validación de `djlint` tras corregir errores de estructura y accesibilidad.
*   **Documentación:** Actualizado `V06DOC_ROADMAP.md`, levantando oficialmente el bloqueo crítico de alineación.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**PROHIBIDO AVANZAR SIN CUMPLIR ESTOS PUNTOS:**

1.  **TEST DE INTEGRACIÓN ACADÉMICA:** Generar examen de 'Lenguas' (B2) para verificar `immersion_mode='TOTAL'` (instrucciones en idioma objetivo).
2.  **VERIFICACIÓN DE PERSISTENCIA:** Validar el guardado de `student_responses` para widgets complejos (`W-MIX-MATCH`, `W-TECH-CALC`).
3.  **AUDITORÍA SKELETON-FIRST:** Verificar en BD la creación previa de `ExamSection` antes de las llamadas a Gemini.

