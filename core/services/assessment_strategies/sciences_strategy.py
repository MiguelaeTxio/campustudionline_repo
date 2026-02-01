
def generate_item_prompt(context_text, question_obj, **kwargs):
    return f"""
ROL: Profesor de Ingeniería/Ciencias.
TAREA: Generar un problema o cuestión teórica.
TIPO: {question_obj.get_interaction_type_display()}
SECCIÓN: {question_obj.section_label}
REQUISITO: Usa formato LaTeX para fórmulas matemáticas.

CONTEXTO:
{context_text[:3000]}...

INSTRUCCIÓN TÉCNICA:
Genera un objeto JSON válido con:
- "question_text": Enunciado del problema.
- "model_answer": Solución paso a paso (con LaTeX).
- "options": Lista de opciones (si es test).
"""

def generate_sciences_prompt(content_text, subject_name="Técnica"):
    return generate_item_prompt(content_text, type("MockQ", (), {"get_interaction_type_display": lambda: "General", "interaction_type": "QT_PROD", "section_label": "General"})())

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Fundamentos Teóricos', 'source': 'SRC_DIR', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Resolución de Problemas', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_INPUT'},
            {'label': 'Cálculo Avanzado', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_INPUT'}
        ]
    }
