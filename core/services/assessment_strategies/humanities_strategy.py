
def generate_item_prompt(context_text, question_obj, **kwargs):
    return f"""
ROL: Catedrático de Humanidades.
TAREA: Generar un comentario de texto o ensayo.
TIPO: {question_obj.get_interaction_type_display()}
SECCIÓN: {question_obj.section_label}

CONTEXTO:
{context_text[:4000]}...

INSTRUCCIÓN TÉCNICA:
Genera un objeto JSON válido con:
- "question_text": La pregunta o tema a desarrollar.
- "model_answer": Esquema de respuesta correcta o puntos clave.
"""

def generate_humanities_prompt(content_text, subject_name, tribunal_type="GENERIC"):
    return generate_item_prompt(content_text, type("MockQ", (), {"get_interaction_type_display": lambda: "General", "interaction_type": "QT_PROD", "section_label": "General"})())

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Contextualización', 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Comentario de Fuente', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Ensayo Dialéctico', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}
        ]
    }
