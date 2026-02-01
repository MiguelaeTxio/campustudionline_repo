
def generate_item_prompt(context_text, question_obj, **kwargs):
    return f"""
ROL: Tribunal Médico (ECOE).
TAREA: Generar una estación clínica.
TIPO: {question_obj.get_interaction_type_display()}
SECCIÓN: {question_obj.section_label}

CONTEXTO (Caso Clínico):
{context_text[:4000]}...

INSTRUCCIÓN TÉCNICA:
Genera un objeto JSON válido con:
- "question_text": Enunciado clínico o pregunta.
- "model_answer": Protocolo o diagnóstico correcto.
- "options": Lista de opciones (si aplica).
"""

def generate_health_prompt(content_text, subject_name="Salud"):
    return generate_item_prompt(content_text, type("MockQ", (), {"get_interaction_type_display": lambda: "General", "interaction_type": "QT_PROD", "section_label": "General"})())

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Anamnesis y Exploración', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Juicio Clínico', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Plan Terapéutico', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}
        ]
    }
