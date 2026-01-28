import re
import json

def is_minor_language(subject_name):
    """
    Determina si una asignatura corresponde al itinerario MINOR (Idioma Moderno / Lengua C).
    Regla: Si contiene explícitamente 'Minor', 'Mínor', 'Inicial', 'Nivel' o es distinto de 'Estudios Ingleses/Franceses'.
    """
    name = subject_name.upper()
    if any(x in name for x in ["MINOR", "MÍNOR", "IDIOMA MODERNO", "LENGUA C", "INICIAL", "A1", "A2", "B1.1"]):
        return True
    if "FILOLOG" in name or "ESTUDIOS" in name or "LITERATURA" in name:
        return False
    return True

def get_target_language(subject_name):
    name = subject_name.upper()
    if "CHINO" in name or "CHINESE" in name or "中文" in name: return "CHINESE (Simplified)"
    if "FRANC" in name or "FRENCH" in name: return "FRENCH"
    if "ALEM" in name or "GERMAN" in name: return "GERMAN"
    if "JAPON" in name or "JAPANESE" in name: return "JAPANESE"
    if "ITALIA" in name or "ITALIAN" in name: return "ITALIAN"
    if "PORTU" in name or "PORTUGUESE" in name: return "PORTUGUESE"
    if "RUSO" in name or "RUSSIAN" in name: return "RUSSIAN"
    if "ARABE" in name or "ARABIC" in name: return "ARABIC"
    return "ENGLISH"

def get_localized_labels(target_lang):
    if target_lang == "CHINESE (Simplified)":
        return ["阅读理解 (Reading)", "完形填空 (Cloze)", "语法 (Grammar)", "句子排序 (Ordering)", "句型转换 (Transform)", "听力理解 (Listening)", "听写 (Dictation)", "写作 (Writing)", "口语 (Speaking)"]
    if target_lang == "FRENCH":
        return ["Compréhension Écrite", "Texte à trous", "Grammaire", "Cloze ouvert", "Transformations", "Compréhension Orale", "Dictée", "Production Écrite", "Production Orale"]
    return ["Reading Comprehension", "Multiple Choice Cloze", "Use of English", "Open Cloze", "Key Word Transformation", "Listening Comprehension", "Gap-fill Listening", "Writing", "Speaking"]

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    target_lang = get_target_language(subject_name)
    lbls = get_localized_labels(target_lang)
    itinerary = kwargs.get('itinerary')
    if not itinerary:
        itinerary = "MINOR" if is_minor_language(subject_name) else "MAIOR"

    skeleton = []
    if itinerary == "MINOR":
        for i in range(5): skeleton.append({'section_label': lbls[0], 'source_type': 'SRC_TXT', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO', 'options': []})
        for i in range(5): skeleton.append({'section_label': lbls[1], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP', 'options': []})
        for i in range(5): skeleton.append({'section_label': lbls[3], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPN', 'response_mode': 'REQ_INPUT', 'options': []})
        skeleton.append({'section_label': lbls[7], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
        skeleton.append({'section_label': lbls[7], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
    else:
        for _ in range(10): skeleton.append({'section_label': lbls[0], 'source_type': 'SRC_TXT', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(10): skeleton.append({'section_label': lbls[2], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP'})
        for _ in range(5): skeleton.append({'section_label': lbls[4], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_TRF', 'response_mode': 'REQ_INPUT'})
        for _ in range(8): skeleton.append({'section_label': lbls[5], 'source_type': 'SRC_AUD', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(2): skeleton.append({'section_label': lbls[7], 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
        skeleton.append({'section_label': lbls[8], 'source_type': 'SRC_AUD', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_REC'})

    return {
        'requires_api_stimulus': True,
        'prompt_func': 'generate_languages_stimuli_prompt',
        'item_prompt_func': 'generate_languages_item_prompt',
        'skeleton': skeleton,
        'itinerary': itinerary,
        'target_lang': target_lang
    }

def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    target_lang = get_target_language(subject_name)
    return f"""Actúa como un Examinador Oficial de Nivel C1/B2.
OBJETIVO: Generar los textos base (estímulos) para un examen de {target_lang}.
CONTEXTO ACADÉMICO: {subject_name}
CONTENIDO BASE:
{content_text[:800]}

INSTRUCCIONES OBLIGATORIAS:
1. Genera un 'reading_stimulus' (Texto de lectura) de 350-500 palabras en {target_lang} PERFECTO. Debe ser académico y denso.
2. Genera un 'listening_transcript' (Guion de audio) de 200-300 palabras en {target_lang}, estilo monólogo o entrevista radiofónica.
3. NO incluyas preguntas, solo los textos.
4. SALIDA JSON PURO.

JSON OUTPUT FORMAT:
{{
  "reading_stimulus": "Texto completo en {target_lang}...",
  "listening_transcript": "Texto del audio en {target_lang}..."
}}"""

def generate_languages_item_prompt(reading_text: str, listening_transcript: str, cefr_level: str, question_obj, itinerary: str = 'MAIOR', target_lang: str = 'ENGLISH') -> str:
    q_type = question_obj.interaction_type
    s_type = question_obj.source_type
    
    context_text = ""
    if s_type == 'SRC_TXT': context_text = f"BASED ON READING TEXT:\n{reading_text}"
    elif s_type == 'SRC_AUD': context_text = f"BASED ON LISTENING TRANSCRIPT:\n{listening_transcript}"
    else: context_text = "INDEPENDENT EXERCISE (Use of English / Grammar / Writing)."

    instruction_lang_rule = ""
    if itinerary == 'MINOR':
        instruction_lang_rule = "MANDATORY: The 'question_text' (the instruction/statement) MUST BE IN SPANISH (Castellano). Example: 'Elige la opción correcta'."
    else:
        instruction_lang_rule = f"MANDATORY: The 'question_text' (the instruction/statement) MUST BE IN {target_lang}. Example: 'Choose the correct option'."

    return f"""ROLE: {target_lang} Exam Generator ({cefr_level}).
TASK: Generate content for ONE question.
TYPE: {q_type}
{context_text}

{instruction_lang_rule}
CONTENT RULE: The 'options', 'model_answer' and the linguistic content MUST BE IN {target_lang}.

FORMAT SPECIFIC INSTRUCTIONS:
- IF QT_SEL: Provide 4 options.
- IF QT_CLZ_OPT: 'question_text' is sentence with gap, 'model_answer' is correct word.
- IF QT_TRF: 'question_text' is original + keyword. 'model_answer' is transformed sentence.

JSON OUTPUT:
{{
  "question_text": "Instruction...",
  "options": ["A", "B", "C", "D"], 
  "model_answer": "Correct answer..."
}}"""
