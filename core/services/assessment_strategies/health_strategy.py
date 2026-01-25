# Emulador UGR: Estrategia Salud (ECOE)
def generate_health_prompt(content_text, subject_name="Salud"):
    return f"Tribunal ECOE UGR. Diagnóstico por Imagen y Actuación. JSON: questions."

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'label': 'Diagnóstico (Imagen)', 'source': 'SRC_IMG', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Juicio Clínico', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Protocolo de Actuación', 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}
        ]
    }
