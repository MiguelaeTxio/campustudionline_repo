### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

**Nota para el cierre (`PCS`):** Esta sección debe ser copiada textualmente en la "Hoja de Ruta para la Siguiente Sesión" para garantizar la persistencia de la Ley.

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (REPARACIÓN DE EMERGENCIA - ARQUETIPO IDIOMAS)

**Estado Actual:** CRÍTICO. El sistema genera preguntas "meta" sobre el examen (ej: "¿Qué es ACLES?") en lugar de sobre el texto, filtra etiquetas técnicas (`QT_SEL`) al usuario final y rompe la regla de inmersión lingüística (preguntas en inglés para texto chino).

1.  **Tarea 1 (Prompt Engineering Quirúrgico): Reparación de `languages_strategy.py`**
    *   **Objetivo:** Eliminar la "alucinación de rol".
    *   **Acción:** Reescribir `generate_languages_exam_prompt`. Eliminar instrucciones que confunden a la IA sobre su rol ("Actúa como tribunal") y sustituirlas por instrucciones funcionales estrictas ("Genera preguntas BASADAS EXCLUSIVAMENTE en el texto proporcionado").
    *   **Acción:** Forzar el idioma de salida de las preguntas para que coincida con el del texto (Regla de Inmersión).

2.  **Tarea 2 (Saneamiento de Parser): Blindaje en `orchestrator/tasks.py`**
    *   **Objetivo:** Limpiar la "basura técnica" visual.
    *   **Acción:** Implementar una limpieza Regex en `_parse_assessment_text` para eliminar patrones como `(QT_SEL)`, `(QT_CLZ_OPT)` o prefijos numéricos que la IA inserta en el `question_text`.

3.  **Tarea 3 (Lógica Cloze): Reparación de Formato de Huecos**
    *   **Objetivo:** Que los ejercicios de rellenar huecos sean oraciones con huecos, no preguntas.
    *   **Acción:** Modificar el prompt para exigir explícitamente el formato "Oración con token `[...]`" para los tipos `QT_CLZ_*`, penalizando las oraciones interrogativas.

4.  **Tarea 4 (Validación Visual): Auditoría de Plantillas**
    *   **Objetivo:** Asegurar que el widget de dropdown se renderiza correctamente cuando el texto contiene el token `[...]`.
