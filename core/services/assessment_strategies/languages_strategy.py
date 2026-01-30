import re
import json

def is_minor_language(subject_name):
    name = subject_name.upper()
    if any(x in name for x in ["MINOR", "MÍNOR", "IDIOMA MODERNO", "LENGUA C", "INICIAL", "A1", "A2", "B1.1"]):
        return True
    return "FILOLOG" not in name and "ESTUDIOS" not in name and "LITERATURA" not in name

def get_target_language(subject_name):
    name = subject_name.upper()
    langs = {
        "CHINO": "CHINESE (Simplified)", "CHINESE": "CHINESE (Simplified)", "中文": "CHINESE (Simplified)",
        "FRANC": "FRENCH", "FRENCH": "FRENCH",
        "ALEM": "GERMAN", "GERMAN": "GERMAN",
        "JAPON": "JAPANESE", "JAPANESE": "JAPANESE",
        "ITALIA": "ITALIAN", "ITALIAN": "ITALIAN",
        "PORTU": "PORTUGUESE", "RUSO": "RUSSIAN", "ARABE": "ARABIC"
    }
    for key, val in langs.items():
        if key in name: return val
    return "ENGLISH"

def get_localized_labels(target_lang):
    if "CHINESE" in target_lang:
        return ["阅读理解 (Reading)", "完形填空 (Cloze)", "语法 (Grammar)", "句子排序 (Ordering)", "句型转换 (Transform)", "听力理解 (Listening)", "听写 (Dictation)", "写作 (Writing)", "口语 (Speaking)"]
    return ["Reading Comprehension", "Multiple Choice Cloze", "Grammar", "Open Cloze", "Key Word Transformation", "Listening Comprehension", "Dictation", "Writing", "Speaking"]

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    target_lang = get_target_language(subject_name)
    lbls = get_localized_labels(target_lang)
    itinerary = kwargs.get('itinerary') or ("MINOR" if is_minor_language(subject_name) else "MAIOR")

    skeleton = []
    if itinerary == "MINOR":
        # 5 Reading (Test)
        for _ in range(5): skeleton.append({'section_label': lbls[0], 'source_type': 'SRC_TXT', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        # 5 Multiple Choice Cloze
        for _ in range(5): skeleton.append({'section_label': lbls[1], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP'})
        # 5 Open Cloze (Rellenar huecos sin opciones)
        for _ in range(5): skeleton.append({'section_label': lbls[3], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPN', 'response_mode': 'REQ_INPUT'})
        # 2 Writing
        for _ in range(2): skeleton.append({'section_label': lbls[7], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
    else:
        # Estructura MAIOR (36 ítems)
        for _ in range(10): skeleton.append({'section_label': lbls[0], 'source_type': 'SRC_TXT', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(10): skeleton.append({'section_label': lbls[1], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP'})
        for _ in range(5): skeleton.append({'section_label': lbls[4], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_TRF', 'response_mode': 'REQ_INPUT'})
        for _ in range(8): skeleton.append({'section_label': lbls[5], 'source_type': 'SRC_AUD', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(2): skeleton.append({'section_label': lbls[7], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
        skeleton.append({'section_label': lbls[8], 'source_type': 'SRC_AUD', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_REC'})

    return {
        'requires_api_stimulus': True,
        'prompt_func': 'generate_languages_stimuli_prompt',
        'skeleton': skeleton,
        'itinerary': itinerary,
        'target_lang': target_lang
    }

def generate_languages_stimuli_prompt(content_text, subject_name):
    target_lang = get_target_language(subject_name)
    return f"""ROL: Examinador {target_lang}.
TAREA: Generar estímulos base para examen.
CONTEXTO: {subject_name}.
CONTENIDO: {content_text[:1000]}

INSTRUCCIONES:
1. 'reading_stimulus': Texto de 400 palabras en {target_lang}.
2. 'listening_transcript': Guion de audio en {target_lang}.
3. Solo textos, sin preguntas.
4. JSON Puro.
"""

def generate_languages_item_prompt(reading_text, listening_transcript, cefr_level, question_obj, itinerary='MAIOR', target_lang='ENGLISH'):
    q_type = question_obj.interaction_type
    s_type = question_obj.source_type
    
    context = ""
    if s_type == 'SRC_TXT': context = f"TEXTO DE REFERENCIA:\n{reading_text}"
    elif s_type == 'SRC_AUD': context = f"GUION DE AUDIO:\n{listening_transcript}"
    else: context = "CONOCIMIENTO GENERAL DEL IDIOMA."

    instr_lang = "CASTELLANO (Español)" if itinerary == 'MINOR' else target_lang

    return f"""ROL: Generador de ítems {target_lang} ({cefr_level}).
TAREA: Crear UNA pregunta de tipo {q_type}.
CONTEXTO: {context}

REGLAS CRÍTICAS DE CONTENIDO (EVITA LA GENERACIÓN FANTASMA):
1. El campo 'question_text' DEBE contener la instrucción en {instr_lang} SEGUIDA del contenido del ejercicio en {target_lang}.
2. Si es {q_type} 'QT_SEL' (Test): 'question_text' debe incluir una pregunta específica sobre el texto.
3. Si es {q_type} 'QT_CLZ_OPT' o 'QT_CLZ_OPN': 'question_text' debe incluir una frase completa con un hueco marcado como '[...]'.
4. Si es {q_type} 'QT_PROD' (Writing): 'question_text' debe describir un escenario de redacción detallado.

EJEMPLO DE SALIDA (Para Minor Chino):
{{
  "question_text": "Elige la respuesta correcta basada en el texto: [Pregunta en Chino aquí]",
  "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
  "model_answer": "Opción Correcta"
}}

SALIDA JSON PURO. NO AÑADAS COMENTARIOS EXTRA.
"""
