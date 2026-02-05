import json

def generate_item_prompt(content_text, question_obj, **kwargs):
    already_covered = kwargs.get("already_covered", [])
    objectives = kwargs.get("learning_objectives", {})
    syllabus = kwargs.get("syllabus", [])
    
    memory_context = ""
    if already_covered:
        memory_context = "\nCRITICAL: DO NOT REPEAT these previous topics:\n" + "\n".join([f"- {p[:80]}" for p in already_covered])

    # Construcción de directrices específicas según el tipo de sección
    specific_instructions = ""
    if "Fuente" in question_obj.section_label:
        specific_instructions = (
            "PEDAGOGICAL GOAL: PRIMARY SOURCE ANALYSIS.\n"
            "1. MANDATORY: You MUST QUOTE the specific fragment or describe the artwork/source at the BEGINNING of your question.\n"
            "2. CONTEXT: The student DOES NOT have the source material in front of them. You must provide it within the 'question_text'.\n"
            "3. Ask the student to analyze this specific quote/source connecting it with the author's context."
        )
    elif "Ensayo" in question_obj.section_label:
        specific_instructions = (
            "PEDAGOGICAL GOAL: DIALECTICAL ESSAY.\n"
            "1. Propose a controversial thesis or historiographical debate related to the content.\n"
            "2. Ask the student to argue for or against using academic evidence.\n"
            "3. BE SPECIFIC: Avoid generic questions like 'Write about...'. Refer to specific concepts from the syllabus."
        )
    else:
        specific_instructions = (
            "PEDAGOGICAL GOAL: CONCEPTUAL PRECISION.\n"
            "1. Focus on specific terminology, dates, authors, or artistic movements defined in the syllabus."
        )

    prompt = f"""ACT AS A HUMANITIES CHAIR (UGR). 
PEDAGOGICAL CONTEXT: {json.dumps(objectives)}
SYLLABUS: {json.dumps(syllabus)}
SOURCE MATERIAL: {content_text}
{memory_context}

TASK: Generate ONE (1) question for "{question_obj.section_label}".
Type: {question_obj.interaction_type}.

{specific_instructions}

GENERAL RULES:
1. Instructions and content MUST be in Spanish.
2. If Type is QT_SEL: Provide 4 UNIQUE and plausible options.
3. If Type is QT_PROD: Ask for an academic essay or critical analysis. Tell the student to take a PHOTO of their work (Handwritten preferred for retention).

JSON SCHEMA: {{"question_text": "...", "options": ["opt1", "opt2", "opt3", "opt4"], "model_answer": "..."}}"""
    return prompt

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'section_label': 'Conceptos Clave y Terminología', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'},
            {'section_label': 'Contexto Histórico y Cultural', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'},
            {'section_label': 'Análisis de Fuente Primaria', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'},
            {'section_label': 'Ensayo Dialéctico', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'}
        ]
    }

def generate_correction_prompt(question_text, model_answer, student_answer):
    return f"""ACT AS A HUMANITIES CHAIR (UGR).
TASK: Grade the student's essay/answer.

CRITERIA:
1. Historical Context: Does the student relate the topic to the correct period/author?
2. Argumentation: Is the essay well-structured? (Thesis -> Arguments -> Conclusion).
3. Evidence: Does the student use specific facts/data?

QUESTION: "{question_text}"
MODEL ANSWER (Guide): "{model_answer}"
STUDENT ANSWER: "{student_answer}"

INSTRUCTIONS:
- Rate from 0 to 100.
- Provide feedback in SPANISH, focusing on how to improve the argument.

OUTPUT FORMAT:
PUNTUACION: [0-100]
FEEDBACK: [Detailed qualitative feedback]"""

def get_ui_labels(subject_name, **kwargs):
    return {
        "reading_header": "FUENTE / TEXTO DE ANÁLISIS",
        "audio_header": "RECURSO AUDIOVISUAL",
        "recording_label": "RESPUESTA ORAL",
        "write_answer_placeholder": "Desarrolla tu análisis académico aquí...",
        "upload_label": "Subir Manuscrito/Imagen",
        "upload_help": "Clic o arrastrar archivo",
        "submit_button": "Entregar Evaluación"
    }
