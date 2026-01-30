
def generate_item_prompt(context_text, question_obj):
    return f"""
ROL: Catedrático de Derecho.
TAREA: Generar el contenido para una pregunta de examen basada en el arquetipo SOCIO_LEGAL.
TIPO: {question_obj.get_interaction_type_display()} ({question_obj.interaction_type})
SECCIÓN: {question_obj.section_label}

CONTEXTO (Supuesto de Hecho):
{context_text[:4000]}...

INSTRUCCIÓN TÉCNICA:
Genera un objeto JSON válido con los campos:
- "question_text": El enunciado completo.
- "model_answer": La fundamentación jurídica correcta.
- "options": Lista de strings (solo si es tipo Test/Selección).
"""

def generate_legal_prompt(content_text, subject_name="Derecho"):
    # Legacy support
    return generate_item_prompt(content_text, type("MockQ", (), {"get_interaction_type_display": lambda: "General", "interaction_type": "QT_PROD", "section_label": "General"})())

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Identificación Normativa', 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Fundamentación Jurídica', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Dictamen Final', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}
        ]
    }
