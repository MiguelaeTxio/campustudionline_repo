# Emulador UGR: Estrategia Humanidades y Letras
def generate_humanities_prompt(content_text, subject_name, tribunal_type="GENERIC"):
    return f"Catedrático UGR. Comentario de Texto y Ensayo. JSON: questions."

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Contextualización', 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Comentario de Fuente', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Ensayo Dialéctico', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}
        ]
    }
