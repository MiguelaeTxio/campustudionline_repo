# Emulador UGR: Estrategia Derecho
def generate_legal_prompt(content_text, subject_name="Derecho"):
    return f"Catedrático Derecho UGR. Dictamen y Teoría. JSON: questions."

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Teoría Normativa', 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Teoría Normativa', 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Dictamen de Caso Práctico', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}
        ]
    }
