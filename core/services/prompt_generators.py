# [V3 - Arquitectura Simplificada] Este módulo centraliza la creación de prompts para la API de IA.
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
    This prompt instructs the AI to perform a creative re-writing and synthesis of the official syllabus,
    guided by learning objectives and explicitly filtering out practical content.
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
    [V4 - Blindaje de Contexto] Phase 3: Genera un prompt para desarrollar el contenido de una
    única subsección, inyectando un preámbulo de contexto académico para mitigar falsos
    positivos de los filtros de seguridad.
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


def generate_assessment_prompt(
    content_text: str,
    subject_type: str = "HUMANITIES",
    segment_info: str = "Evaluación Global",
    learning_objectives: str = ""
) -> str:
    """
    [HITO 6] Generador de Exámenes Universitarios Reales (V3 - Academic Rigor).
    Estructuras basadas en modelos oficiales (Cambridge B2, Ingeniería, UNED).
    """
    
    # --- ARQUETIPO: CIENCIAS EXACTAS (Cálculo/Ingeniería) ---
    if subject_type == "EXACT_SCIENCES":
        instructions = (
            "Actúa como un Catedrático de Ingeniería. Genera un EXAMEN FINAL riguroso.\n"
            "ESTRUCTURA OBLIGATORIA (4 PROBLEMAS DE DESARROLLO):\n"
            "Genera 4 Problemas Complejos. Cada problema debe tener apartados (a, b, c).\n"
            "1. Problema 1: Conceptos base / Cálculo directo (con variables numéricas).\n"
            "2. Problema 2: Aplicación práctica o resolución de problemas.\n"
            "3. Problema 3: Demostración o análisis de casos límite.\n"
            "4. Problema 4: Problema integrado de alta dificultad.\n\n"
            "REGLAS TÉCNICAS:\n"
            "- Usa LaTeX OBLIGATORIAMENTE para toda fórmula matemática: `\\\\(...\\\\)` (en línea) y `$$...$$` (bloque).\n"
            "- La 'model_answer' debe mostrar el desarrollo paso a paso, no solo el resultado final."
        )

    # --- ARQUETIPO: IDIOMAS (Certificación Oficial) ---
    elif subject_type == "LANGUAGES":
        instructions = (
            "Actúa como un Examinador Oficial de Acreditación Universitaria (Modelo CertAcles / CLM UGR). "
            "Tu objetivo es generar un examen de dominio de lengua extranjera (Nivel B2/C1) basado rigurosamente en el texto proporcionado.\n"
            "ESTRUCTURA OBLIGATORIA (4 DESTREZAS - SIN GRAMÁTICA AISLADA):\n\n"
            "**DESTREZA 1: COMPRENSIÓN LECTORA (Reading)**\n"
            "- Usa el texto proporcionado como base.\n"
            "- Genera 4 preguntas de COMPRENSIÓN PROFUNDA (no literal).\n"
            "- Formato: Preguntas de respuesta abierta breve o análisis de intención del autor.\n"
            "- NO generes ejercicios de rellenar huecos (Use of English).\n\n"
            "**DESTREZA 2: COMPRENSIÓN AUDITIVA (Listening)**\n"
            "- Escribe un guion de audio (Transcript) de 200 palabras que complemente el tema (ej: una entrevista a un experto o una conferencia).\n"
            "- REGLA DE FORMATO: El guion DEBE estar encerrado en: [---TRANSCRIPT---]...texto...[---END-TRANSCRIPT---]\n"
            "- Genera 2 preguntas sobre este audio. IMPORTANTE: El enunciado de la pregunta DEBE decir explícitamente: 'Escucha el audio y responde: [Tu Pregunta]'. No dejes el enunciado vacío.\n\n"
            "**DESTREZA 3: EXPRESIÓN ESCRITA (Writing)**\n"
            "- Tarea 1 (Interacción): Propón la redacción de un correo electrónico formal o carta al director relacionada con el tema (aprox 150 palabras).\n"
            "- Tarea 2 (Producción): Propón la redacción de un Ensayo de Opinión (Essay) discutiendo los pros y contras del tema (aprox 250 palabras).\n\n"
            "**DESTREZA 4: EXPRESIÓN ORAL (Speaking)**\n"
            "- Propón un tema para un Monólogo Sostenido (3-4 minutos).\n"
            "- OBLIGATORIO: Añade al final la etiqueta: [---RECORDING-REQUIRED---]."
        )

    else:
        instructions = (
            "Actúa como Profesor Titular de Humanidades. Genera un examen modelo Universidad/UNED.\n"
            "ESTRUCTURA OBLIGATORIA (3 PARTES):\n\n"
            "**PARTE 1: DEFINICIÓN DE CONCEPTOS**\n"
            "- Genera 4 preguntas cortas para definir conceptos clave o términos técnicos del texto.\n\n"
            "**PARTE 2: COMENTARIO DE TEXTO/OBRA**\n"
            "- Selecciona un fragmento significativo del texto proporcionado (o descríbelo si es una obra de arte).\n"
            "- Pide un análisis formal, estilístico e histórico-contextual.\n\n"
            "**PARTE 3: TEMA DE DESARROLLO**\n"
            "- Plantea 1 pregunta amplia de desarrollo ('Elabore un ensayo sobre...') que requiera relacionar autores, causas y consecuencias."
        )

    
    objectives_section = ""
    if learning_objectives:
        objectives_section = (
            "**GUÍA DOCENTE (OBJETIVOS DE APRENDIZAJE):**\n"
            "El examen debe certificar que el alumno ha adquirido las siguientes competencias. "
            "Prioriza preguntas que validen estos objetivos sobre detalles triviales del texto:\n"
            f"{learning_objectives}\n\n"
        )

    base_prompt = (
        f"{objectives_section}{instructions}\n\n"
        f"CONTEXTO: {segment_info}\n"
        "MATERIAL DE ESTUDIO (Fuente):\n"
        "--------------------------------------------------\n"
        f"{content_text[:45000]}\n"
        "--------------------------------------------------\n\n"
        "**FORMATO JSON (Strict Schema):**\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "question_text": "Enunciado del problema / Transcript + Pregunta / Tema Speaking...",\n'
        '      "question_type": "open_ended",\n'
        '      "model_answer": "Solución detallada..."\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "Nota: Genera TODOS los items solicitados en la estructura (aprox 10-12 items en total). No omitas ninguna parte."
    )
    return base_prompt
