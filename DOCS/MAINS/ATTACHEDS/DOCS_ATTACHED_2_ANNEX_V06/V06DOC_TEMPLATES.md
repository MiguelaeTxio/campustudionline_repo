# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_TEMPLATES.md
# V06DOC_TEMPLATES - ESQUEMA DE DATOS "UGR-LEVEL EXAM CONTRACT" (V1.2 - SKELETON-FIRST)

Este documento define la estructura JSON obligatoria para la comunicación entre el motor de IA y el emulador. 

**ACTUALIZACIÓN SKELETON-FIRST:** El esqueleto del examen (Cabecera y Fases) es generado por Python mediante el método  de la estrategia. La IA genera el contenido de los ítems de forma atómica para cada sección.

## 1. CABECERA DEL EXAMEN (EXAM_HEADER - Orquestado por Python)
*   exam_id: [UUID] Identificador único de la sesión.
*   archetype_id: [ID] Referencia a V06DOC_ARCHETYPES.
*   sub_archetype_id: [ID] Referencia a V06DOC_SUBARCHETYPES.
*   itinerary_id: [ID] Referencia a V06DOC_SUBDIVISIONS (ITIN).
*   pedagogical_level: [LVL_A | LVL_B | LVL_C].
*   grading_params: Objeto con pesos relativos por subdivisión.

## 2. ESTRUCTURA DE FASES (SUBDIVISION_SEQUENCE - Orquestado por Python)
Definida por . Array de objetos de fase:
*   subdivision_id: [ID] (ej: SD_READ, SD_CALC).
*   title: Nombre público de la sección.
*   instructions: Guía de cumplimiento para el alumno.
*   time_limit: Segundos de bloqueo (0 para ilimitado).
*   items: Lista de bloques de evaluación (Poblados atómicamente por la IA).

## 3. DEFINICIÓN DE ÍTEMS (ITEM_PAYLOAD - Generado por IA)
Estructura obligatoria para cada ejercicio. La IA debe responder con un array  de estos objetos:
*   block_type: [ID] (ej: PRM_STRIKE, RPP_TRAZA, CLO-OPEN, CLO-MULTI, MAT-LINK, DRA-HOLO).
*   widget_id: [ID] (ej: W_OBJ_STRIKE, W_TECH_CALC, W_TXT_CLOZE, W_MIX_MATCH, W_HUM_TEXT).
*   content:
    *   stem: Enunciado técnico.
    *   media_assets: [Array] URLs de recursos (imágenes, audios).
    *   options: [Array] (Solo para Test) Lista de distractores.
    *   text_with_gaps: [String] (Solo para Cloze) Texto con marcadores de huecos.
*   grading_logic:
    *   correct_answer: Valor canónico esperado.
    *   penalty_factor: Float (Resta por error).
    *   kill_switch: Boolean (Error fatal - Ref: CDS-KILL).
    *   step_matrix: [JSON] (Solo para RPP) Mapa de pasos lógicos.
    *   pairs: [Dict] (Solo para MAT-LINK) Mapa de vinculación Drag & Drop.
*   metadata:
    *   competency_tag: [ID] (Referencia V06DOC_METADATA).
    *   cognitive_tag: [ID] (Referencia V06DOC_METADATA).

## 4. CONTRATO DE RESPUESTA (STUDENT_SUBMISSION)
*   item_id: ID del bloque resuelto.
*   raw_input: Datos brutos del widget.
*   timestamp: Momento de la respuesta.

## 5. REPORTE DE EVALUACIÓN (GRADING_REPORT)
*   item_score: Nota del ítem.
*   feedback_category: [ID] (Referencia V06DOC_METADATA - FB_CONCEPT, FB_FORMAL, etc.).
*   justification: Texto explicativo (Rol Catedrático).
