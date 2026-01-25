# Emulador UGR: Estrategia Ciencias (ETSIIT)
def generate_sciences_prompt(content_text, subject_name="Técnica"):
    return f"Profesor UGR. Examen para '{subject_name}'. LaTeX obligatorio. JSON: questions."

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Fundamentos Teóricos', 'source': 'SRC_DIR', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Fundamentos Teóricos', 'source': 'SRC_DIR', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Resolución de Problemas', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_INPUT'},
            {'label': 'Resolución de Problemas', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_INPUT'}
        ]
    }
