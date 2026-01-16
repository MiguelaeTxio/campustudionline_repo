from typing import List, Dict

def generate_course_metadata_prompt(
    topic_description: str, academic_context: str = ""
) -> str:
    """
    [V1 - GJGE] Phase 1: Generates the prompt to request course metadata in JSON format.
    """
    context_section = ""
    if academic_context:
        context_section = (
            "Para contextualizar la propuesta, considera el siguiente marco académico:\n"
            f"{academic_context}\n"
        )

    prompt = (
        "Actúa como un experto en catalogación académica y diseño instruccional. Tu única tarea es generar un objeto JSON con los metadatos para un curso sobre el siguiente tema:\n"
        f'**Tema del Curso:** "{topic_description}"\n\n'
        f"{context_section}\n"
        "La respuesta DEBE ser un único bloque de código JSON válido, sin texto introductorio, explicaciones adicionales ni marcadores de formato.\n"
        "El objeto JSON debe contener exclusivamente las siguientes claves y tipos de datos:\n"
        "{\n"
        '  "descripcion_corta": "string",\n'
        '  "audiencia": "string",\n'
        '  "requisitos_previos": ["string"],\n'
        '  "objetivos_aprendizaje": ["string"],\n'
        '  "clasificacion_intelectual": {\n'
        '    "categoria_general": "string",\n'
        '    "subcategoria": "string",\n'
        '    "palabras_clave": ["string"]\n'
        "  }\n"
        "}\n\n"
        "Por favor, genera el JSON completo con contenido detallado y pertinente basado en el tema del curso."
    )
    return prompt


def generate_master_schema_prompt(
    topic_description: str,
    academic_context: str = "",
    learning_objectives: str = "",
    syllabus: str = "",
) -> str:
    """
    [V3 - Síntesis Anti-Plagio] Phase 2: Generates a prompt to request the exhaustive course index.
    """
    context_section = ""
    if academic_context:
        context_section = (
            "**Contexto Académico:**\n"
            "Este curso se enmarca en el siguiente contexto, que debe guiar el nivel de profundidad y enfoque:\n"
            f"{academic_context}\n"
        )

    objectives_section = ""
    if learning_objectives:
        objectives_section = (
            "**Objetivos de Aprendizaje (Guía de Alcance):**\n"
            "Utiliza estos objetivos como una guía vinculante para definir el **alcance y la profundidad** de cada tema. No debes crear un curso para graduados si los objetivos son introductorios. El temario que generes debe ser el vehículo para cumplir estos objetivos, ni más ni menos.\n"
            f"{learning_objectives}\n"
        )

    syllabus_section = ""
    if syllabus:
        syllabus_section = (
            "**Temario Fuente (Ingredientes):**\n"
            "Este es el temario oficial de la asignatura. Trátalo como una lista de conceptos que debes cubrir en su totalidad.\n"
            f"{syllabus}\n"
        )

    prompt = (
        "Actúa como un catedrático experto en diseño curricular y redacción académica. Tu misión es crear una Tabla de Contenidos **completamente original** para una asignatura, basándote en un temario fuente. El resultado debe ser **semánticamente equivalente** (cubrir los mismos temas) pero **morfológicamente distinto** (redacción y estructura originales) para evitar cualquier acusación de plagio.\n"
        f'**Asignatura:** "{topic_description}"\n\n'
        f"{context_section}\n"
        f"{objectives_section}\n"
        f"{syllabus_section}\n"
        "**REGLAS VINCULANTES Y OBLIGATORIAS:**\n"
        "1.  **SÍNTESIS ORIGINAL (ANTI-PLAGIO):** Tu tarea principal es **re-expresar** los conceptos del Temario Fuente con una redacción original y profesional. **Por ejemplo, si el temario fuente dice 'Fundamentos de Programación', tu propuesta podría ser 'Bases de la programación'. Si dice 'Bucles', podrías proponer 'Procesos reiterativos en programación: Bucles'.**\n"
        "2.  **EXCLUSIÓN DE CONTENIDO PRÁCTICO:** Está **terminantemente prohibido** incluir en tu propuesta cualquier sección o tema que se refiera a contenido práctico (ej. 'Prácticas', 'Programa Práctáctico', 'Examen práctico'). Debes ignorar y descartar esas secciones del temario fuente.\n"
        "3.  **COBERTURA TOTAL:** Debes cubrir el 100% de los conceptos teóricos presentados en el Temario Fuente.\n"
        "4.  **FORMATO DE SALIDA ESTRICTO:** Tu respuesta debe ser **únicamente texto en formato Markdown**. No incluyas NADA MÁS: ni introducciones, ni resúmenes, ni explicaciones. Solo el índice.\n"
        "5.  **ESTRUCTURA JERÁRQUICA PROFUNDA:** Desglosa cada concepto en una estructura de libro de texto (`##` para temas principales, `###` y `####` para sub-secciones detalladas).\n"
        "6.  **LÍMITE DE ENTRADAS:** El índice total no debe superar las 500 entradas.\n\n"
        "Procede ahora a generar la Tabla de Contenidos original, sintetizada y detallada, adhiriéndote estrictamente a todas las reglas."
    )
    return prompt


def generate_atomic_content_prompt(
    course_title: str,
    section_title: str,
    master_schema: str,
    academic_context: str = "",
) -> str:
    """
    [V4 - Blindaje de Contexto] Phase 3: Genera un prompt para desarrollar el contenido de una única subsección.
    """
    context_preamble = ""
    if academic_context:
        context_preamble = (
            "## CONTEXTO ACADÉMICO OBLIGATORIO ##\n"
            "La siguiente solicitud es para generar contenido educativo riguroso y puramente académico. "
            "Este material formará parte de un curso universitario y debe ser tratado como tal, adhiriéndose "
            "a un enfoque objetivo, basado en hechos y terminología científica. Cualquier tema potencialmente "
            "sensible debe ser abordado desde una perspectiva estrictamente analítica y académica.\n"
            "Marco del curso:\n"
            f"{academic_context}\n"
            "-----------------------------------\n\n"
        )

    prompt = (
        f"{context_preamble}"
        f"Actúa como un Catedrático experto y un autor de libros de texto universitarios. Tu prestigio depende de la calidad y profundidad de tu trabajo.\n\n"
        f'Estás colaborando en la redacción del libro titulado: "{course_title}".\n\n'
        "Para que tengas un contexto absoluto sobre el alcance total de la obra y dónde encaja tu contribución, aquí tienes el índice completo del libro:\n"
        "--- INICIO DEL ÍNDICE COMPLETO ---\n"
        f"{master_schema}\n"
        "--- FIN DEL ÍNDICE COMPLETO ---\n\n"
        "-----------------------------------\n\n"
        f'Tu tarea específica es generar el contenido para la sección: **"{section_title}"**.\n\n'
        "**REQUISITOS OBLIGATORIOS DE FORMATO DE SALIDA:**\n"
        "1.  **FORMATO DE TEXTO PLANO (MARKDOWN):** Tu respuesta debe ser **exclusivamente texto en formato Markdown**. No incluyas texto introductorio, explicaciones, resúmenes, ni ningún tipo de estructura contenedora como JSON.\n"
        "2.  **SEPARADOR DE FUENTES OBLIGATORIO:** Después de desarrollar todo el contenido de la sección, DEBES incluir una línea que contenga única y exclusivamente el siguiente separador: `---FUENTES---`.\n"
        "3.  **BLOQUE DE FUENTES:** Inmediatamente después del separador, DEBES incluir un bloque de texto en formato Markdown listando entre 2 y 4 referencias bibliográficas (libros, artículos académicos) que respalden directamente el contenido generado.\n\n"
        "**REQUISITOS OBLIGATORIOS PARA EL CONTENIDO (ANTES DEL SEPARADOR):**\n"
        "-   **PROFUNDIDAD ACADÉMICA:** El contenido debe ser exhaustivo, riguroso y pedagógico. Explora implicaciones, presenta análisis críticos y contextos.\n"
        "-   **EXTENSIÓN SIGNIFICATIVA:** El desarrollo de la sección debe tener una extensión máxima de 2000 palabras.\n"
        "-   **ESTRUCTURA CLARA:** Utiliza sub-encabezados de Markdown (`####`) para organizar el contenido en subapartados lógicos.\n"
        "-   **RIQUEZA PEDAGÓGICA:** Enriquece el texto con ejemplos, listas, tablas y analogías.\n\n"
        "**Ejemplo de la estructura de respuesta que DEBES seguir:**\n"
        "```markdown\n"
        "#### Subapartado 1\n\n"
        "Texto del primer subapartado con listas y **negritas**.\n\n"
        "#### Subapartado 2\n\n"
        "Texto del segundo subapartado con más detalles.\n\n"
        "---FUENTES---\n\n"
        "- Apellido, A. (Año). *Título del Libro*. Editorial.\n"
        "- Apellido, B. (Año). Título del artículo. *Nombre de la Revista*, Volumen(Número), páginas.\n"
        "```\n\n"
        f'Procede ahora a generar el contenido y las fuentes para la sección **"{section_title}"**, cumpliendo rigurosamente todos los requisitos.'
    )
    return prompt


def generate_classification_prompt(subject_name: str, branch_name: str) -> str:
    """
    [HITO 6 - V12] Clasificador Semántico de Asignaturas.
    Discrimina la naturaleza de la asignatura basándose en su nombre y rama.
    """
    return (
        f"Analiza la asignatura '{subject_name}' perteneciente a la rama académica '{branch_name}'.\n"
        "Tu tarea es clasificarla en uno de los siguientes 3 Arquetipos de Evaluación:\n\n"
        "1. EXACT_SCIENCES: Elige esto SOLO si la asignatura implica resolución de problemas matemáticos, cálculo, física o ingeniería pura.\n"
        "   - Ejemplo: 'Cálculo I', 'Física Cuántica', 'Estructuras de Hormigón', 'Resistencia de Materiales'.\n"
        "   - EXCEPCIÓN: Si es una asignatura teórica en una carrera técnica (ej: 'Historia de la Arquitectura', 'Legislación'), NO uses esto.\n\n"
        "2. LANGUAGES: Elige esto SOLO si el objetivo principal es aprender un segundo idioma (Gramática, Vocabulario).\n"
        "   - Ejemplo: 'Inglés III', 'Francés para Turismo', 'Alemán B2'.\n\n"
        "3. HUMANITIES: Para todo lo demás. Incluye Historia, Derecho, Biología, Arte, Teoría, Legislación, Medicina, etc.\n"
        "   - Ejemplo: 'Legislación Urbanística' (aunque sea de Arquitectura), 'Historia del Arte', 'Derecho Romano'.\n\n"
        "Responde ÚNICA y EXCLUSIVAMENTE con una de las 3 palabras clave: EXACT_SCIENCES, LANGUAGES o HUMANITIES."
    )


def generate_assessment_prompt(
    content_text: str,
    subject_type: str = "HUMANITIES",
    segment_info: str = "Evaluación Global",
    learning_objectives: str = ""
) -> str:
    """
    [HITO 6] Generador de Exámenes Universitarios Reales (V4 - UGR Strict Emulator).
    """
    
    # --- ARQUETIPO: CIENCIAS EXACTAS (ETSIIT UGR) ---
    if subject_type == "EXACT_SCIENCES":
        instructions = "Actúa como un Catedrático de Ingeniería. Genera un EXAMEN FINAL riguroso.\nESTRUCTURA OBLIGATORIA (4 PROBLEMAS):\nGenera 4 Problemas de Desarrollo Complejos. NO uses preguntas tipo test.\n1. Problema 1: Conceptos base / Cálculo directo.\n2. Problema 2: Aplicación práctica.\n3. Problema 3: Demostración o caso límite.\n4. Problema 4: Problema integrado.\n\nREGLAS TÉCNICAS:\n- Usa LaTeX OBLIGATORIAMENTE para fórmulas: \\(...\\) y $$...$$.\n- Establece 'question_type': 'open_ended'."

    # --- ARQUETIPO: IDIOMAS (CLM UGR - CertAcles) ---
    elif subject_type == "LANGUAGES":
        instructions = "Actúa como un Examinador Oficial CertAcles. Generarás un examen de 4 secciones. \nESTA PROHIBIDO omitir cualquier sección. Debes completar el checklist:\n\n1. [ ] SECCIÓN READING: Genera 4 preguntas 'multiple_choice' con 4 opciones cada una.\n2. [ ] SECCIÓN LISTENING: Genera un Transcript (200 palabras) entre [---TRANSCRIPT---] y [---END-TRANSCRIPT---]. Luego genera 2 preguntas 'multiple_choice' (3 opciones) sobre ese audio.\n3. [ ] SECCIÓN WRITING: Genera 1 tarea de redacción (Essay o Email) tipo 'open_ended'.\n4. [ ] SECCIÓN SPEAKING: Genera 1 tema de monólogo tipo 'open_ended' + etiqueta [---RECORDING-REQUIRED---].\n\n**REGLA DE ORO:** La respuesta debe contener exactamente 8 preguntas en total (4 Reading + 2 Listening + 1 Writing + 1 Speaking).\n**EJEMPLO OBLIGATORIO DE FORMATO JSON:**\n{\n  \"question_text\": \"...\",\n  \"question_type\": \"multiple_choice\",\n  \"options\": [\"a) ...\", \"b) ...\", \"c) ...\", \"d) ...\"],\n  \"model_answer\": \"a) ...\"\n}"

    # --- ARQUETIPO: HUMANIDADES (UNED/UGR) ---
    else:
        instructions = "Actúa como Profesor Titular de Humanidades. Genera un examen mixto:\n1. **Definición de Conceptos (Test):** 2 preguntas teóricas clave.\n  - TIPO: 'multiple_choice'.\n   - Opciones: 4 opciones.\n2. **Comentario de Texto:** 1 fragmento para analizar.\n   - TIPO: 'open_ended'.\n3. **Desarrollo:** 1 pregunta amplia de ensayo.\n   - TIPO: 'open_ended'."

    objectives_section = ""
    if learning_objectives:
        objectives_section = f"**OBJETIVOS DE APRENDIZAJE:**\n{learning_objectives}\n\n"

    base_prompt = f"""{objectives_section}{instructions}

CONTEXTO: {segment_info}
FUENTE:
--------------------------------------------------
{content_text[:45000]}
--------------------------------------------------

**FORMATO JSON ESTRICTO:**
{{
  "questions": [
    {{
      "question_text": "Enunciado...",
      "question_type": "multiple_choice" O "open_ended",
      "options": ["a) Opción 1", "b) Opción 2", "c) Opción 3"] (SOLO SI ES multiple_choice),
      "model_answer": "Respuesta correcta (letra o desarrollo)..."
    }}
  ]
}}
IMPORTANTE: Si 'question_type' es 'multiple_choice', el campo 'options' es OBLIGATORIO."""
    return base_prompt


def generate_stimulus_creation_prompt(content_source: str, subject_name: str, subject_type: str = "HUMANITIES") -> str:
    """
    [HITO 6 - V11] Generador de Estímulos con Nivel Dinámico Adaptativo.
    """
    target_language = "el idioma de la asignatura"
    idiomas_map = {"italiano": "Italiano", "ingles": "Inglés", "english": "Inglés", "frances": "Francés", "aleman": "Alemán"}
    for k, v in idiomas_map.items():
        if k in subject_name.lower():
            target_language = v
            break

    if subject_type == "LANGUAGES":
        instructions = (
            f"1. Analiza el nombre de la asignatura: '{subject_name}' e identifica el nivel (A1, B2, Inicial, Avanzado, etc.).\n"
            "2. Identifica los puntos gramaticales en la FUENTE.\n"
            "3. Selecciona un tema de actualidad o cultura.\n"
            f"4. Redacta un texto (Reading) y un guion (Listening) en {target_language}.\n"
            "5. REGLA CRÍTICA: La complejidad del vocabulario y la sintaxis DEBE CORRESPONDERSE EXACTAMENTE con el nivel pedagógico detectado."
        )
    else:
        instructions = "Genera un texto de análisis académico profundo sobre el tema, adaptando la complejidad al nivel de la asignatura."

    prompt = (
        "Actúa como un Examinador Pedagogo Senior.\n\n"
        f"ASIGNATURA: {subject_name}\n"
        f"FUENTE TÉCNICA:\n{content_source[:15000]}\n\n"
        f"MISION:\n{instructions}\n\n"
        "REGLAS DE ORO:\n"
        "- El nivel de dificultad debe ser coherente con el contexto.\n"
        f"- Idioma de salida para los textos: {target_language}.\n\n"
        "FORMATO DE SALIDA JSON ESTRICTO:\n"
        "{\n"
        '  "reading_stimulus": "Texto auténtico...",\n'
        '  "listening_transcript": "Guion de audio auténtico..."\n'
        "}"
    )
    return prompt
def generate_ugr_questions_prompt(reading_text: str, listening_text: str, subject_type: str = "HUMANITIES") -> str:
    """
    [HITO 6 - V10] Tribunal de Examen UGR: Genera las 4 secciones obligatorias.
    """
    prompt = (
        "Actúa como un Tribunal de Examen Universitario. Tu misión es generar un examen "
        "estructurado en 4 SECCIONES basándote en los textos proporcionados.\n\n"
        f"TEXTOS DE REFERENCIA:\n"
        f"1. LECTURA: {reading_text[:3000]}\n"
        f"2. AUDIO: {listening_text[:3000]}\n\n"
        "ESTRUCTURA OBLIGATORIA DEL EXAMEN (Total 8 tareas):\n"
        "**NOTA DE FORMATO:** Debes separar CADA sección con un encabezado Markdown H3 en el idioma del examen (ej: '### READING', '### LETTURA', '### LESEVERSTEHEN').\n"
        "1. SECCIÓN READING: 4 preguntas 'multiple_choice' sobre el texto de LECTURA.\n"
        "2. SECCIÓN LISTENING: 2 preguntas 'multiple_choice' sobre el texto de AUDIO.\n"
        "3. SECCIÓN WRITING: 1 tarea de redacción académica (open_ended) relacionada con los temas.\n"
        "4. SECCIÓN SPEAKING: 1 tema de exposición oral (open_ended). IMPORTANTE: Debes incluir "
        "el marcador [---RECORDING-REQUIRED---] al final del enunciado del Speaking.\n\n"
        "FORMATO JSON ESTRICTO:\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "question_text": "Enunciado...",\n'
        '      "question_type": "multiple_choice" | "open_ended",\n'
        '      "options": ["a)...", "b)...", "c)...", "d)..."],\n'
        '      "model_answer": "..."\n'
        "    }\n"
        "  ]\n"
        "}"
    )
    return prompt
