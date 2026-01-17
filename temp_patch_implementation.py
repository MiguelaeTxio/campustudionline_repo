import re

# ==============================================================================
# 1. ACTUALIZACIÓN DE PROMPT_GENERATORS.PY (DEFINICIÓN DE TRIBUNALES)
# ==============================================================================

NEW_CLASSIFICATION_PROMPT = r'''def generate_classification_prompt(subject_name: str, branch_name: str) -> str:
    """
    [HITO 6 - V13] Clasificador Semántico de Asignaturas (Granularidad Alta).
    Discrimina la naturaleza de la asignatura en 8 Arquetipos de Evaluación.
    """
    return (
        f"Analiza la asignatura '{subject_name}' perteneciente a la rama académica '{branch_name}'.\n"
        "Tu tarea es clasificarla en uno de los siguientes ARQUETIPOS DE TRIBUNAL:\n\n"
        "1. EXACT_SCIENCES: Matemáticas, Física, Ingeniería, Cálculo, Estructuras.\n"
        "2. LANGUAGES: Aprendizaje de idiomas (Inglés, Francés, Alemán...).\n"
        "3. LEGAL: Derecho, Legislación, Normativa, Constitucional, Procesal.\n"
        "4. ARTS: Historia del Arte, Estética, Música, Patrimonio, Composición.\n"
        "5. SOCIETY: Filosofía, Sociología, Política, Antropología, Pensamiento.\n"
        "6. HISTORY: Historia (Universal/España), Geografía, Arqueología.\n"
        "7. PHILOLOGY: Lingüística, Literatura, Gramática (teórica), Semántica.\n"
        "8. HUMANITIES_GENERIC: Para lo que no encaje en lo anterior (ej: Pedagogía, Biblioteconomía).\n\n"
        "Responde ÚNICA y EXCLUSIVAMENTE con una de las palabras clave: "
        "EXACT_SCIENCES, LANGUAGES, LEGAL, ARTS, SOCIETY, HISTORY, PHILOLOGY, HUMANITIES_GENERIC."
    )'''

NEW_ASSESSMENT_PROMPT = r'''def generate_assessment_prompt(
    content_text: str,
    subject_type: str = "HUMANITIES_GENERIC",
    segment_info: str = "Evaluación Global",
    learning_objectives: str = ""
) -> str:
    """
    [HITO 6 - V5] Generador de Exámenes Universitarios con Tribunales Especializados.
    """
    
    # --- CONFIGURACIÓN DE TRIBUNALES (HUMANIDADES Y CIENCIAS SOCIALES) ---
    # Estructura Estándar: 2 Test + 1 Práctico + 1 Ensayo
    humanities_structure = (
        "ESTRUCTURA OBLIGATORIA (4 PREGUNTAS):\n"
        "1. [TEST] Conceptos Fundamentales: 2 preguntas 'multiple_choice' (4 opciones) sobre terminología clave.\n"
        "2. [PRÁCTICO] Análisis Aplicado: 1 pregunta 'open_ended' que plantee un caso práctico, análisis de fragmento o aplicación de norma.\n"
        "3. [ENSAYO] Síntesis Crítica: 1 pregunta 'open_ended' de desarrollo extenso y relación de conceptos.\n"
    )

    tribunals = {
        "LEGAL": {
            "role": "Catedrático de Derecho y Magistrado",
            "focus": "Céntrate en la interpretación normativa, jurisprudencia y aplicación de leyes. Evalúa el rigor jurídico.",
            "structure": humanities_structure
        },
        "ARTS": {
            "role": "Historiador del Arte y Crítico",
            "focus": "Céntrate en el análisis formal, iconografía, estilo y contexto histórico-artístico.",
            "structure": humanities_structure
        },
        "SOCIETY": {
            "role": "Catedrático de Sociología y Filosofía",
            "focus": "Céntrate en corrientes de pensamiento, dialéctica, estructuras sociales e implicaciones éticas.",
            "structure": humanities_structure
        },
        "HISTORY": {
            "role": "Doctor en Historia",
            "focus": "Céntrate en la causalidad, cronología, análisis de fuentes y contextos geopolíticos.",
            "structure": humanities_structure
        },
        "PHILOLOGY": {
            "role": "Lingüista y Filólogo",
            "focus": "Céntrate en el análisis textual, pragmática, evolución de la lengua y crítica literaria.",
            "structure": humanities_structure
        },
        "HUMANITIES_GENERIC": {
            "role": "Profesor Titular Universitario",
            "focus": "Evalúa la comprensión profunda, capacidad de síntesis y rigor académico.",
            "structure": humanities_structure
        }
    }

    # --- LÓGICA DE SELECCIÓN DE INSTRUCCIONES ---
    
    if subject_type == "EXACT_SCIENCES":
        instructions = (
            "Actúa como un Catedrático de Ingeniería. Genera un EXAMEN FINAL riguroso.\n"
            "ESTRUCTURA OBLIGATORIA (4 PROBLEMAS):\n"
            "Genera 4 Problemas de Desarrollo Complejos. NO uses preguntas tipo test.\n"
            "1. Problema 1: Conceptos base / Cálculo directo.\n"
            "2. Problema 2: Aplicación práctica.\n"
            "3. Problema 3: Demostración o caso límite.\n"
            "4. Problema 4: Problema integrado.\n\n"
            "REGLAS TÉCNICAS:\n"
            "- Usa LaTeX OBLIGATORIAMENTE para fórmulas: \\(...\\) y $$...$$.\n"
            "- Establece 'question_type': 'open_ended'."
        )

    elif subject_type == "LANGUAGES":
        # Fallback para idiomas si entrara por este flujo (aunque suele ir por ugr_questions)
        instructions = (
            "Actúa como un Examinador Oficial. Genera un examen de comprobación:\n"
            "1. Reading Comprehension (2 preguntas multiple_choice).\n"
            "2. Use of English / Grammar (1 pregunta multiple_choice).\n"
            "3. Writing Task (1 pregunta open_ended)."
        )

    else:
        # Selección del Tribunal de Humanidades
        tribunal = tribunals.get(subject_type, tribunals["HUMANITIES_GENERIC"])
        instructions = (
            f"Actúa como {tribunal['role']}.\n"
            f"{tribunal['focus']}\n\n"
            f"{tribunal['structure']}"
        )

    objectives_section = ""
    if learning_objectives:
        objectives_section = f"**OBJETIVOS DE APRENDIZAJE:**\n{learning_objectives}\n\n"

    base_prompt = f"""{objectives_section}{instructions}

CONTEXTO: {segment_info}
FUENTE ÚNICA DE LA VERDAD (SOLO ESTE TEXTO):
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
    return base_prompt'''

NEW_UGR_PROMPT = r'''def generate_ugr_questions_prompt(reading_text: str, listening_text: str, subject_type: str = "HUMANITIES") -> str:
    """
    [HITO 6 - V11] Tribunal de Examen UGR: Genera las 4 secciones obligatorias.
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
    return prompt'''

with open("/home/MiguelAeTxio/SWAP/prompt_generators.py.prop", "r", encoding="utf-8") as f:
    prompts_content = f.read()

# Reemplazos en prompt_generators.py
pattern_class = r'def generate_classification_prompt.*?return \(\s*f"Analiza la asignatura.*?HUMANITIES\."\s*\)'
match_class = re.search(pattern_class, prompts_content, re.DOTALL)
if match_class:
    prompts_content = prompts_content.replace(match_class.group(0), NEW_CLASSIFICATION_PROMPT)

pattern_assess = r'def generate_assessment_prompt.*?subject_type: str = "HUMANITIES",.*?return base_prompt'
match_assess = re.search(pattern_assess, prompts_content, re.DOTALL)
if match_assess:
    prompts_content = prompts_content.replace(match_assess.group(0), NEW_ASSESSMENT_PROMPT)

pattern_ugr = r'def generate_ugr_questions_prompt.*?subject_type: str = "HUMANITIES"\) -> str:.*?return prompt'
match_ugr = re.search(pattern_ugr, prompts_content, re.DOTALL)
if match_ugr:
    prompts_content = prompts_content.replace(match_ugr.group(0), NEW_UGR_PROMPT)

with open("/home/MiguelAeTxio/SWAP/prompt_generators.py.prop", "w", encoding="utf-8") as f:
    f.write(prompts_content)


# ==============================================================================
# 2. ACTUALIZACIÓN DE TASKS.PY (LÓGICA DE ENRUTADOR)
# ==============================================================================

NEW_TASK_LOGIC = r'''                if step == 0:
                    log_assessment_task_event(assessment_id, f"PASO 0 (Clasificación) - Key: {api_key.name}")
                    class_prompt = generate_classification_prompt(subject_name, branch_name)
                    success_class, class_resp, _ = generate_text_content(class_prompt, api_key=api_key)
                    
                    if success_class:
                        raw_type = clean_json_response(class_resp).strip().upper()
                        # Saneamiento de los 8 tipos nuevos
                        valid_types = [
                            "EXACT_SCIENCES", "LANGUAGES", "LEGAL", "ARTS", 
                            "SOCIETY", "HISTORY", "PHILOLOGY", "HUMANITIES_GENERIC"
                        ]
                        found_type = "HUMANITIES_GENERIC"
                        for vt in valid_types:
                            if vt in raw_type:
                                found_type = vt
                                break
                        
                        subject_type = found_type
                        log_assessment_task_event(assessment_id, f"Clasificación API: {subject_type}")
                        step = 1
                    else:
                        raise ResourceExhausted(class_resp)

                elif step == 1:
                    log_assessment_task_event(assessment_id, f"PASO 1 (Fuente de Verdad) - Arquetipo: {subject_type}")
                    selection = assessment.selection_range
                    # Contenido REAL filtrado por sliders
                    filtered_source = filter_content_by_selection(full_content, selection) if selection else full_content
                    
                    # [HITO 6] BIFURCACIÓN DE FUENTE DE VERDAD
                    if subject_type == "LANGUAGES":
                        # IDIOMAS: Generación creativa obligatoria
                        log_assessment_task_event(assessment_id, "Modo IDIOMAS: Generando estímulos artificiales...")
                        prompt = generate_stimulus_creation_prompt(filtered_source, subject_name, subject_type)
                        success, text, _ = generate_text_content(prompt, api_key=api_key)
                        if not success: raise ResourceExhausted(text)
                        
                        dat = dirtyjson.loads(clean_json_response(text))
                        r_text = dat.get('reading_stimulus', '')
                        l_text = dat.get('listening_transcript', '')
                        if not r_text: raise ValueError("IA de Idiomas no generó reading_stimulus.")
                        
                    else:
                        # HUMANIDADES / CIENCIAS: Fuente = Contenido Real
                        log_assessment_task_event(assessment_id, "Modo TRIBUNAL: Usando contenido real como Fuente Única.")
                        r_text = filtered_source
                        l_text = ""
                        
                        if not r_text or len(r_text) < 50:
                            r_text = full_content # Fallback

                    with transaction.atomic():
                        aa = Assessment.objects.select_for_update().get(pk=assessment_id)
                        aa.reading_stimulus = r_text
                        aa.listening_transcript = l_text
                        aa.status = Assessment.AssessmentStatus.PROCESSING
                        aa.save(update_fields=['reading_stimulus', 'listening_transcript', 'status'])
                    step = 2

                elif step == 2:
                    log_assessment_task_event(assessment_id, f"PASO 2 (Tribunal) - Key: {api_key.name}")
                    
                    if subject_type == "LANGUAGES":
                        prompt = generate_ugr_questions_prompt(r_text, l_text, subject_type)
                    else:
                        # Tribunal Especializado: Pasa el subject_type (LEGAL, ARTS, etc.)
                        prompt = generate_assessment_prompt(r_text, subject_type=subject_type)
                    
                    success, text, _ = generate_text_content(prompt, api_key=api_key)
                    if not success: raise ResourceExhausted(text)
                    
                    questions_data = _parse_assessment_text(text)
                    if not questions_data: raise ValueError("IA no devolvió preguntas válidas.")'''

with open("/home/MiguelAeTxio/SWAP/tasks.py.prop", "r", encoding="utf-8") as f:
    tasks_content = f.read()

# Patrón para el bucle en tasks.py
# Busca desde "if step == 0:" hasta la validación de preguntas del paso 2
pattern_tasks = re.compile(r'if step == 0:.*?questions_data = _parse_assessment_text\(text\)\n\s+if not questions_data: raise ValueError\("IA no devolvió preguntas válidas\."\)', re.DOTALL)

match_tasks = pattern_tasks.search(tasks_content)
if match_tasks:
    tasks_content = tasks_content.replace(match_tasks.group(0), NEW_TASK_LOGIC)

with open("/home/MiguelAeTxio/SWAP/tasks.py.prop", "w", encoding="utf-8") as f:
    f.write(tasks_content)
