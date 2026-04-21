<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_TEMPLATES.md -->
# V06DOC_TEMPLATES - CONTRATO DE INYECCIÓN DE CONTENIDO (V2.1 - DATA PROVIDER MODEL)

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

**Input (Desde Python):** "El Ítem {uuid} es un {widget_id}. Instrucción de llenado: {TaskInstruction}."

**Output (Desde IA):** Array `filled_items`.
*   **item_id**: [UUID] Debe coincidir con el solicitado.
*   **content**:
    *   stem: Enunciado técnico. **OBLIGATORIO:** Solo la pregunta/ejercicio. Prohibido incluir teoría o introducciones pedagógicas.
    *   media_assets: [Array] (Opcional).
    *   options: [Array] (Obligatorio para W-OBJ-STRIKE. Mínimo 4 opciones).
    *   text_with_gaps: [String] (Obligatorio para W-TXT-CLOZE).
*   **grading_logic**:
    *   correct_answer / gap_solutions / pairs: Soluciones según el widget.
    *   feedback_justification: **OBLIGATORIO:** Explicación académica y teórica de la respuesta. Único lugar permitido para el rol docente.
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

## 6. SECUENCIAS DE FASES POR SUBARQUETIPO (SUBDIVISION_SEQUENCE — CONTRATOS ESPECÍFICOS)

Esta sección documenta los contratos de inyección de contenido específicos para cada subarquetipo que requiere una secuencia de fases distinta de la estructura genérica. Complementa la Sección 2 (SUBDIVISION_SEQUENCE) con las particularidades pedagógicas de cada modelo.

### 6.1. Contrato de Fases: SUB-LIN-PHILO (UGR — Filología Hispánica)
*   **Fase 1 (SD_PHONO — Fonética y Fonología Histórica):** Contrato para el análisis de leyes fonéticas diacrónicas. Requiere estímulo de texto fuente con étimo latino (u origen) y salida JSON con la secuencia completa de estadios evolutivos intermedios. Cada estadio debe incluir: forma en ese estadio, ley fonética aplicada, tipo de Yod si procede (I/II/III/IV) y justificación. Motor: EV-DIAC-VAL. Widget: W-PHILO-IPA.
*   **Fase 2 (SD_MORPH_DIAC — Morfología Diacrónica):** Contrato con foco en paradigmas de declinación y conjugación histórica. La IA debe generar ítems que exijan la identificación de la ley de analogía o nivelación morfológica aplicada. Motor: EV-DIAC-VAL. Widget: W-PHILO-IPA.
*   **Fase 3 (SD_LEX_SEM — Lexicología y Semántica Histórica):** Contrato de análisis etimológico. La IA debe contrastar el étimo con los criterios del DCECH (Corominas y Pascual) y el CORDE/CDH. Identificación de cultismos, semicultismos y palabras patrimoniales. Identificación de cambios semánticos (metáfora, metonimia, elipsis). Motor: RBT-CANON. Widget: W-HUM-TEXT.
*   **Fase 4 (SD_TEXT_CRIT — Crítica Textual / Ecdótica):** Contrato de fijación de textos. Interfaz SPLIT_TEXT para colación de variantes y fijación de estema codicum. La IA genera el aparato crítico con variantes, adiciones, omisiones y propuesta de emendatio siguiendo la Metodología Blecua (UGR). Motor: EV-PALE. Widget: W-PHILO-ECDO.

### 6.2. Contrato de Fases: SUB-LIN-NORM (UGR — Filología Hispánica / El Español Actual: Norma y Uso, cód. 2831111) [NUEVO v5.1 — 2026-04-21]
*   **Estructura:** Cuatro fases secuenciales no compensables. Umbral mínimo del 75% por fase para superar la destreza (FAIL_LOGIC: FATAL por fase no superada). Rigor Engine x1.7 activo en todas las fases.
*   **Fase 1 (SD_CORPUS_ANALYSIS — Investigación y Validación Empírica):**
    *   **Widget:** W-LAW-NAV en Modo Lingüístico (W-LAW-NAV-LING).
    *   **Estímulo:** Consulta emulada en CORPES XXI/CREA sobre una construcción lingüística en conflicto (ej. pluralización de "haber" impersonal, uso de "detrás mío" vs. "detrás de mí", infinitivo fático). La IA genera el ítem con datos de frecuencia y distribución geográfica y registral reales.
    *   **Tarea:** El alumno interpreta los resultados del corpus, discrimina el uso culto del coloquial y el peninsular del americano, y emite un juicio científico sobre la aceptabilidad de la construcción en el registro académico.
    *   **Motor:** EV-NORM-ANALYSIS (valida la interpretación científica del uso frente a la prescripción panhispánica).
    *   **Layout:** SPLIT_TEXT (resultados de corpus en panel izquierdo — sticky; respuesta del alumno en panel derecho).
*   **Fase 2 (SD_MORPH_ANTINORM — Diagnóstico de Desviaciones Morfosintácticas):**
    *   **Widgets:** W-OBJ-STRIKE y W-TXT-CLOZE (Modo Input).
    *   **Estímulo:** La IA genera textos con fenómenos antinormativos incrustados: queísmo, dequeísmo, leísmo de persona y de cosa, laísmo, loísmo, discordancias en el orden de los clíticos, pasivas reflejas e impersonales incorrectas.
    *   **Tarea:** El alumno identifica el fenómeno con su nomenclatura técnica exacta, localiza la infracción en el texto y propone la corrección razonada.
    *   **Motor:** RBT-CANON (exigencia de precisión absoluta en la nomenclatura técnica del fenómeno; la paráfrasis o corrección sin identificación técnica no se admite).
    *   **Penalización:** NO_NEGATIVE_MARKING desactivado — penalización activa por respuesta incorrecta.
*   **Fase 3 (SD_ORTHO_PRESCRIPTIVE — Ortografía y Ortotipografía Académica):**
    *   **Widget:** W-HUM-TEXT en Modo Revisión y Control de Cambios.
    *   **Modos de entrada activos:** Teclado Latino Nativo y OCR/Captura de manuscrito exclusivamente. Occidentalización y Pad de Trazos deshabilitados (restricción SUB-LIN-NORM).
    *   **Estímulo:** La IA genera un texto con errores ortotipográficos deliberados conforme a la OLE 2010: uso incorrecto de mayúsculas diacríticas, puntuación compleja (comillas, rayas, paréntesis, guiones), acentuación de compuestos, gestión de extranjerismos y neologismos.
    *   **Tarea:** El alumno edita el texto mediante control de cambios visible (inserciones, eliminaciones y sustituciones diferenciadas visualmente), marca y clasifica cada error por categoría ortotipográfica y justifica la intervención con referencia a la OLE 2010.
    *   **Motor:** EV-NORM-ANALYSIS. Rigor x1.7.
*   **Fase 4 (SD_CRITICAL_NORM — Comentario Crítico y Justificación Bibliográfica):**
    *   **Widget:** W-HUM-TEXT con layout SPLIT_TEXT.
    *   **Modos de entrada activos:** Teclado Latino Nativo y OCR/Captura de manuscrito exclusivamente.
    *   **Panel izquierdo (Estímulo — Sticky):** Texto fuente inadecuado desde el punto de vista normativo (registro incorrecto, fenómenos antinormativos, desviaciones ortotipográficas).
    *   **Panel derecho (Editor):** El alumno redacta una justificación académica argumentada citando explícitamente la Nueva Gramática de la Lengua Española (NGLE, RAE/ASALE 2009) o el Diccionario Panhispánico de Dudas (DPD, RAE/ASALE 2005). Evalúa además la adecuación del registro al contexto comunicativo especificado (jurídico, administrativo o académico).
    *   **Motor:** DRA-HOLO.
    *   **FAIL_LOGIC:** FATAL para el ítem si la cita de una obra de referencia es falsa o inexacta.

### 6.3. Contrato de Fases: SUB-LIN-TRA-TECH (FTI-UGR — Traducción Especializada B-A Inglés, cód. 252113T) [NUEVO v5.1 — 2026-04-21]
*   **Estructura:** Tres bloques temáticos evaluables de forma independiente: Jurídico, CSH (Ciencias Sociales y Humanidades) y Científico-Técnico. Umbral mínimo 5/10 por bloque. Sin compensación entre bloques (FAIL_LOGIC: FATAL por bloque no superado). Secuencia de bloques: Jurídico → CSH → Científico-Técnico. Non-backtracking entre bloques.
*   **NOTA CRÍTICA:** SD_TRA_REVIEW NO existe como destreza evaluable en este subarquetipo. La evaluación oficial de la Guía Docente 252113T (FTI-UGR, aprobada 01/07/2025) consiste exclusivamente en traducciones directas cronometradas. La secuencia genética correcta es de tres destrezas: SD_TRA_ANALYSIS → SD_TERM_RESEARCH → SD_TRA_DRAFT.
*   **Fase 1 (SD_TRA_ANALYSIS + SD_TERM_RESEARCH — Preparación Documental):**
    *   **Widget:** W-DOC-RESOURCES (Panel de Recursos Documentales UGR).
    *   **Estímulo:** El alumno recibe el texto fuente en inglés en el panel izquierdo (sticky). El panel central proporciona acceso emulado a los recursos documentales certificados: IATE (terminología UE), UNTERM (terminología ONU), Diccionario panhispánico del español jurídico (DPEJ-RAE), Diccionario médico CUN, Glosario científico-técnico.
    *   **Tarea:** El alumno analiza la función textual, el destinatario y los problemas potenciales del texto (neologismos, ambigüedades sintácticas, densidad terminológica) y construye su glosario técnico bilingüe en el panel derecho consultando los recursos disponibles.
    *   **Motor:** EV-TRA-PRECISION-TECH (audita que los términos del glosario procedan de fuentes de autoridad y evalúa la calidad terminológica del glosario construido).
*   **Fase 2 (SD_TRA_DRAFT — Traducción Directa Cronometrada):**
    *   **Widget:** W-MEDI-LAYOUT (panel izquierdo: texto fuente en inglés — sticky; panel derecho: editor de traducción).
    *   **Texto:** 200-250 palabras por bloque temático, conforme al baremo oficial de evaluación de la Guía Docente 252113T.
    *   **Tiempo límite:** 1 hora por bloque temático.
    *   **Tarea:** El alumno produce la traducción directa al español aplicando las equivalencias terminológicas validadas en la Fase 1. Se evalúa la precisión léxica, el cumplimiento del registro y la adecuación al género textual del bloque.
    *   **Motor:** EV-TRA-PRECISION-TECH con jerarquía de errores A/B/C: Categoría A (Sentido — Contrasentido -2.0, Sin sentido -1.5, Falso sentido -1.0), Categoría B (Terminología — lema no especializado -0.5), Categoría C (Gramática y Estilo — inadecuación de registro u error ortotipográfico OLE 2010, -0.2).
    *   **Non-backtracking:** Una vez enviado un bloque, el acceso queda bloqueado permanentemente.

### 6.4. Contrato de Fases: SUB-LIN-TRA-LIT (FTI-UGR — Literatura y Traducción Lengua B Inglés, cód. 25211NJ) [NUEVO v5.1 — 2026-04-21]
*   **Estructura:** Tres fases secuenciales evaluadas conjuntamente mediante DRA-HOLO-LIT. Umbral mínimo 5/10 en la media de los cuatro ejes de la rúbrica DRA-HOLO-LIT para superar el subarquetipo (coherente con la nota mínima 5 declarada en la Guía Docente 25211NJ). Non-backtracking entre fases: una vez completada y enviada una fase, el acceso queda bloqueado permanentemente.
*   **Fase 1 (SD_TRA_STYLE — Análisis Estilístico Comparado):**
    *   **Widget:** W-HUM-TEXT con layout SPLIT_TEXT.
    *   **Panel izquierdo (Estímulo — Sticky):** Texto literario fuente (poema o fragmento teatral/narrativo en inglés, autor anglófono del corpus de la asignatura 25211NJ). No editable. Permanece visible durante toda la fase.
    *   **Panel derecho (Editor):** El alumno redacta el análisis estilístico en modo edición libre.
    *   **Tarea:** Identificación y descripción de la voz autorial, los rasgos estilísticos (registro, tono, ritmo, figuras retóricas), los culturemas y los retos de transferencia que plantea el texto fuente para la traducción al español.
    *   **Extensión mínima del análisis:** 300 palabras.
    *   **Motor:** DRA-HOLO-LIT (Ejes 1 y 2).
    *   **Modos de entrada activos:** Teclado Latino Nativo y OCR/Captura de manuscrito. Occidentalización y Pad de Trazos deshabilitados (no aplican para inglés→español).
*   **Fase 2 (SD_TRA_CREATIVE — Transferencia Estética):**
    *   **Widget:** W-HUM-TEXT en modo SPLIT_TEXT.
    *   **Panel izquierdo (Estímulo — Sticky):** El mismo texto literario fuente de la Fase 1. No editable.
    *   **Panel derecho (Editor):** El alumno redacta su traducción literaria al español en modo edición libre.
    *   **Tarea:** Producción de la traducción literaria al español preservando el efecto estético del original. Gestión documentada de culturemas, intertextos y juegos lingüísticos. Las compensaciones adoptadas deben ser coherentes con el análisis realizado en la Fase 1.
    *   **Motor:** DRA-HOLO-LIT (Ejes 1, 2 y 3).
    *   **Modos de entrada activos:** Teclado Latino Nativo y OCR/Captura de manuscrito. Occidentalización y Pad de Trazos deshabilitados.
*   **Fase 3 (SD_TRA_CRIT — Comentario Exegético y Justificación Traductológica):**
    *   **Widget:** W-HUM-TEXT en modo libre (sin panel lateral).
    *   **Tarea:** El alumno redacta el ensayo crítico justificando de forma razonada y documentada las decisiones traductoras adoptadas en las Fases 1 y 2. Extensión: 1500-2000 palabras, conforme a los criterios de evaluación de la Guía Docente 25211NJ. El ensayo debe incluir citas correctas de la bibliografía traductológica oficial: Reynolds (2011), Venuti (2017) y el marco del Skopos.
    *   **Motor:** DRA-HOLO-LIT (Eje 4 exclusivamente).
    *   **Control de originalidad:** Enviado a través de Turnitin emulado para verificación de originalidad.
    *   **FAIL_LOGIC:** FATAL para la destreza si el ensayo carece de fundamentación bibliográfica o reproduce opiniones ajenas sin argumentación original.
