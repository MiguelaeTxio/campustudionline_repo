import json

def generate_item_prompt(content_text, question_obj, **kwargs):
    already_covered = kwargs.get("already_covered", [])
    objectives = kwargs.get("learning_objectives", {})
    syllabus = kwargs.get("syllabus", [])

    memory_context = ""
    if already_covered:
        memory_context = "\nDO NOT REPEAT these clinical scenarios:\n" + "\n".join([f"- {p[:80]}" for p in already_covered])

    prompt = f"""ACT AS A MEDICAL TRIBUNAL (ECOE). 
SYLLABUS: {json.dumps(syllabus)}
CASE CONTEXT: {content_text}
{memory_context}

TASK: Generate ONE (1) clinical question for "{question_obj.section_label}".
Type: {question_obj.interaction_type}.

RULES:
1. Focus on patient safety and evidence-based medicine.
2. If QT_SEL: 4 UNIQUE options.
3. If QT_PROD: Ask for diagnosis or nursing care plan. Tell the student to take a PHOTO of their clinical notes.
JSON SCHEMA: {{"question_text": "...", "options": ["opt1", "opt2", "opt3", "opt4"], "model_answer": "Clinical protocol"}}"""
    return prompt

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'section_label': 'Anamnesis y Exploración', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'},
            {'section_label': 'Juicio Clínico', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'},
            {'section_label': 'Plan Terapéutico', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'}
        ]
    }

def get_ui_labels(subject_name, **kwargs):
    """Etiquetas de interfaz para arquetipo HEALTH SCIENCES."""
    return {
        "reading_header": "MATERIAL DE REFERENCIA",
        "audio_header": "RECURSO AUDITIVO",
        "recording_label": "RESPUESTA POR VOZ",
        "write_answer_placeholder": "Desarrolla tu respuesta técnica aquí...",
        "upload_label": "Subir Resolución (Foto/PDF)",
        "upload_help": "Clic o arrastrar archivo",
        "submit_button": "Entregar Evaluación"
    }
