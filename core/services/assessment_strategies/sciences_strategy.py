import json

def generate_item_prompt(content_text, question_obj, **kwargs):
    already_covered = kwargs.get("already_covered", [])
    objectives = kwargs.get("learning_objectives", {})
    syllabus = kwargs.get("syllabus", [])
    
    memory_context = ""
    if already_covered:
        memory_context = "\nDO NOT REPEAT these problems:\n" + "\n".join([f"- {p[:80]}" for p in already_covered])

    prompt = f"""ACT AS AN ENGINEERING PROFESSOR (UGR). 
CONTEXT: {json.dumps(objectives)} | SYLLABUS: {json.dumps(syllabus)}
SOURCE: {content_text}
{memory_context}

TASK: Generate ONE (1) technical question for "{question_obj.section_label}".
Type: {question_obj.interaction_type}.
REQUIREMENT: Use LaTeX for ALL mathematical formulas.

RULES:
1. If QT_SEL: 4 UNIQUE options.
2. If QT_PROD: Ask for step-by-step resolution. Tell the student to take a PHOTO of their calculations.
JSON SCHEMA: {{"question_text": "...", "options": ["opt1", "opt2", "opt3", "opt4"], "model_answer": "Solution in LaTeX"}}"""
    return prompt

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'section_label': 'Fundamentos Teóricos', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'},
            {'section_label': 'Resolución de Problemas', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'},
            {'section_label': 'Cálculo Avanzado', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'}
        ]
    }

def get_ui_labels(subject_name, **kwargs):
    """Etiquetas de interfaz para arquetipo SCIENCES & TECH."""
    return {
        "reading_header": "MATERIAL DE REFERENCIA",
        "audio_header": "RECURSO DE APOYO",
        "recording_label": "EXPLICACIÓN VERBAL",
        "upload_label": "Subir Resolución (Foto/PDF)",
        "upload_help": "Adjuntar cálculos manuscritos",
        "write_answer_placeholder": "Desarrolla tu respuesta técnica aquí...",
        "submit_button": "Entregar Evaluación"
    }
