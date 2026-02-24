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
# ESTADO: DOCUMENTACIÓN RE-ARQUITECTURADA Y CORE REPARADO

### PARTE MUTABLE (RESUMEN TÉCNICO Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (NRA)
*   **Reparación del Core:** Se ha refactorizado `core/services/gemini_service.py` para soportar `response_schema`, eliminando el bloqueo técnico de la generación.
*   **Evolución del Modelo:** Actualizado `assessment_v2/models/main.py` con `section_stimulus` y `layout_mode` para soportar paneles laterales dinámicos.
*   **Re-arquitectura "Python-Dictator":** Tras detectar una desalineación pedagógica grave (instrucciones en inglés, destrezas inapropiadas para niveles básicos), se ha reescrito la constelación documental del Hito 6. Se establece que Python define el esqueleto inmutable (Widgets y Estructura) y la IA solo rellena el contenido.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**OBJETIVO: IMPLEMENTACIÓN DEL MOTOR DE PLANTILLAS DETERMINISTA**

### I. FASE DE REFACTORIZACIÓN DEL ORQUESTRADOR
1.  Modificar `orchestrator/tasks.py` para que el bucle de generación inyecte contenido en `ExamItems` ya creados en BBDD.
2.  Eliminar la capacidad de la IA para proponer `widget_id` o `block_type`.

### II. FASE DE ESTRATEGIAS (SUBARCHETYPES)
1.  Implementar en `strategies/languages.py` el método `get_exam_skeleton()` que devuelva la receta fija según nivel e itinerario.
2.  Garantizar que para `LVL_A` + `MINOR`, las instrucciones se fuercen en Castellano y el contenido sea Chino Básico.

### III. FASE FRONTEND
1.  Modificar `exam_take.html` para renderizar el `section_stimulus` en un panel lateral persistente (`SPLIT_TEXT`).

