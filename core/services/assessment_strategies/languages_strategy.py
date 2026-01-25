# Emulador UGR: Estrategia de Idiomas (Modelo ACLES)
def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    return f"Actúa como Examinador UGR para '{subject_name}'. Genera Reading (350 palabras) y Listening Transcript. JSON: detected_language, cefr_level, reading_stimulus, listening_transcript."

def generate_languages_exam_prompt(reading_text: str, listening_transcript: str, cefr_level: str = "B1") -> str:
    return f"Tribunal UGR Nivel {cefr_level}. Crea examen de 9 preguntas siguiendo el Master Plan (Cloze, Test, Prod). JSON: questions [question_text, source_type, interaction_type, response_mode, options, model_answer]."

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'requires_api_stimulus': True,
        'prompt_func': 'generate_languages_stimuli_prompt',
        'skeleton': [
            {'label': 'Reading: Multiple Choice', 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Reading: Gapped Text', 'source': 'SRC_TXT', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_DROP'},
            {'label': 'Use of English: Multiple Choice Cloze', 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPT', 'response': 'REQ_DROP'},
            {'label': 'Use of English: Open Cloze', 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_INPUT'},
            {'label': 'Use of English: Keyword Transformation', 'source': 'SRC_DIR', 'interaction': 'QT_TRF', 'response': 'REQ_INPUT'},
            {'label': 'Listening: Multiple Choice', 'source': 'SRC_AUD', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'},
            {'label': 'Listening: Sentence Completion', 'source': 'SRC_AUD', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_INPUT'},
            {'label': 'Writing Expression', 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'},
            {'label': 'Speaking Interaction', 'source': 'SRC_AUD', 'interaction': 'QT_PROD', 'response': 'REQ_REC'}
        ]
    }
