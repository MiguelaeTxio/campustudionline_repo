# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_TEMPLATES.md
# V06DOC_TEMPLATES - CONTRATO DE INYECCIÓN DE CONTENIDO (V2.0 - PYTHON DICTATOR)

Este documento define el contrato de datos entre el orquestador y la IA. 

**ESTÁNDAR DE PLANTILLA RÍGIDA:** La estructura del examen (Secciones e Ítems) es generada por Python antes de la llamada. La IA actúa como motor de renderizado de contenido, rellenando los campos de texto del esqueleto sin poder alterar los widgets ni la jerarquía definida.

## 1. CABECERA DEL EXAMEN (EXAM_HEADER - Orquestado por Python)
*   exam_id: [UUID] Identificador único de la sesión.
*   archetype_id: [ID] Referencia a V06DOC_ARCHETYPES.
*   sub_archetype_id: [ID] Referencia a V06DOC_SUBARCHETYPES.
*   itinerary_id: [ID] Referencia a V06DOC_SUBDIVISIONS (ITIN).
*   pedagogical_level: [LVL_A | LVL_B | LVL_C].
*   grading_params: Objeto con pesos relativos por subdivisión.
*   **expiration_date**: [DATETIME] Fecha límite de realización.
    *   **Regla de Negocio (Anti-Abuso):** Se establece automáticamente en **24 horas** tras la finalización de la generación (Estado 'READY').
    *   **Penalización (Política de Tolerancia Cero):** Si el examen no se completa antes de esta fecha, se aplica una **PENALIZACIÓN TOTAL**. El usuario pierde **toda la cuota semanal restante** de forma inmediata, quedando inhabilitado para solicitar nuevas evaluaciones hasta el siguiente ciclo de reseteo.

## 2. ESTRUCTURA DE FASES (SUBDIVISION_SEQUENCE - Orquestado por Python)
Definida por . Array de objetos de fase:
*   subdivision_id: [ID] (ej: SD_READ, SD_CALC).
*   title: Nombre público de la sección.
*   instructions: Guía de cumplimiento para el alumno.
*   time_limit: Segundos de bloqueo (0 para ilimitado).
*   items: Lista de bloques de evaluación (Poblados atómicamente por la IA).
*   **section_stimulus**: [NUEVO V1.4] (Opcional) Texto, HTML o URL de imagen que sirve de contexto compartido (Reading, Caso, Gráfico). Se renderiza en el Panel Lateral Persistente.
*   **layout_mode**: [NUEVO V1.4] Define la distribución visual:
    *   `STANDARD`: Ancho completo (sin panel lateral). Ideal para Matemáticas/Tests rápidos.
    *   `SPLIT_TEXT`: Panel lateral de texto (Reading/Caso).
    *   `SPLIT_VISUAL`: Panel lateral de imagen/media (Anatomía/Arte).

## 3. DEFINICIÓN DE ÍTEMS (ITEM_PAYLOAD - Rellenado de Plantilla)
La IA recibe los ítems vacíos (definidos por la Estrategia) y devuelve **exclusivamente** el contenido.

**Input (Desde Python):** "El Ítem {uuid} es un {widget_id}. Genera contenido."

**Output (Desde IA):** Array `filled_items`.
*   **item_id**: [UUID] Debe coincidir con el solicitado.
*   **content**:
    *   stem: Enunciado técnico (Traducido según nivel).
    *   media_assets: [Array] (Opcional).
    *   options: [Array] (Solo si el widget lo requiere).
    *   text_with_gaps: [String] (Solo si el widget lo requiere).
*   **grading_logic**:
    *   correct_answer / gap_solutions / pairs: Soluciones según el widget.
    *   feedback_justification: Explicación académica.
*   **metadata**:
    *   competency_tag: [ID].

**NOTA:** La IA tiene PROHIBIDO devolver `widget_id` o `block_type`. Si lo hace, se descarta por error de formato.

## 4. CONTRATO DE RESPUESTA (STUDENT_SUBMISSION)
*   item_id: ID del bloque resuelto.
*   raw_input: Datos brutos del widget.
*   timestamp: Momento de la respuesta.

## 5. REPORTE DE EVALUACIÓN (GRADING_REPORT)
*   item_score: Nota del ítem.
*   feedback_category: [ID] (Referencia V06DOC_METADATA - FB_CONCEPT, FB_FORMAL, etc.).
*   justification: Texto explicativo (Rol Catedrático).
