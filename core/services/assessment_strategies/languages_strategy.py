import json
import re

def get_language_config(subject_name):
    """Determina el idioma objetivo y sus etiquetas localizadas."""
    name = subject_name.upper()
    if "CHINO" in name or "CHINESE" in name or "中文" in name:
        return {"lang": "CHINESE", "labels": ["阅读", "阅读: 填空", "语法", "语法: 填空", "句型转换", "听力", "听力: 填空", "写作", "口语"]}
    if "FRANC" in name or "FRENCH" in name:
        return {"lang": "FRENCH", "labels": ["Compréhension Écrite", "Texte à trous", "Grammaire", "Cloze ouvert", "Transformations", "Compréhension Orale", "Dictée", "Production Écrite", "Production Orale"]}
    # Default: Inglés / Castellano (Modelo UGR)
    return {"lang": "TARGET_LANGUAGE", "labels": ["Reading", "Reading: Gapped", "Use of English", "Open Cloze", "Key Word Transformation", "Listening", "Listening: Completion", "Writing", "Speaking"]}

def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    cfg = get_language_config(subject_name)
    return f"""Actúa como un Examinador del Centro de Lenguas Modernas (CLM) de la UGR.
OBJETIVO: Generar estímulos para un examen de {cfg['lang']}.
INSTRUCCIONES CRÍTICAS:
1. El 'reading_stimulus' y el 'listening_transcript' DEBEN estar escritos íntegramente en {cfg['lang']}.
2. Está TERMINANTEMENTE PROHIBIDO usar castellano o inglés en el contenido de los textos.
3. El Reading debe tener unas 350-400 palabras de nivel académico.

SALIDA JSON ÚNICAMENTE:
{{
  "detected_language": "{cfg['lang']}",
  "cefr_level": "B1",
  "reading_stimulus": "Texto en {cfg['lang']}...",
  "listening_transcript": "Transcripción en {cfg['lang']}..."
}}"""

def generate_languages_item_prompt(reading_text: str, listening_transcript: str, cefr_level: str, target_lang: str, question_obj, itinerary: str = 'MAIOR') -> str:
    """Genera el prompt para rrellenar UN SOLO objeto Question (Flujo Atómico)."""
    section = question_obj.section_label
    q_type = question_obj.interaction_type
    
    return f"""ACT AS: Professional Language Examiner.
TARGET ITINERARY: {itinerary} (Standard UGR/CLM)

MANDATORY INSTRUCTION LANGUAGE:
- IF ITINERARY is 'MINOR': The 'question_text' (instruction) MUST BE IN SPANISH (e.g. "Elige la opción correcta").
- IF ITINERARY is 'MAIOR': The 'question_text' (instruction) MUST BE IN {target_lang} (e.g. "Choose the correct option").

MANDATORY CONTENT LANGUAGE:
- All 'options', 'model_answer' and the exercise body MUST BE in {target_lang}.

JSON OUTPUT FORMAT:
{{
  "question_text": "Spanish instruction + Content",
  "interaction_type": "{q_type}",
  "options": ["Option1 in {target_lang}", "Option2", "Option3", "Option4"],
  "model_answer": "Correct answer in {target_lang}"
}}"""

def _build_maior_skeleton(lbls):
    skeleton = []
    for _ in range(5):
        skeleton.append({'label': lbls[0], 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'})
    for _ in range(5):
        skeleton.append({'label': lbls[1], 'source': 'SRC_TXT', 'interaction': 'QT_MATCH', 'response': 'REQ_MATCH'})
    for _ in range(10):
        skeleton.append({'label': lbls[2], 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPT', 'response': 'REQ_DROP'})
    for _ in range(5):
        skeleton.append({'label': lbls[4], 'source': 'SRC_DIR', 'interaction': 'QT_TRF', 'response': 'REQ_INPUT'})
    for _ in range(8):
        skeleton.append({'label': lbls[5], 'source': 'SRC_AUD', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'})
    skeleton.append({'label': lbls[7], 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'})
    skeleton.append({'label': lbls[7], 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'})
    skeleton.append({'label': lbls[8], 'source': 'SRC_AUD', 'interaction': 'QT_PROD', 'response': 'REQ_REC'})
    return skeleton

def _build_minor_skeleton(lbls):
    skeleton = []
    for _ in range(5):
        skeleton.append({'label': lbls[0], 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'})
    for _ in range(5):
        skeleton.append({'label': lbls[3], 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_INPUT'})
    for _ in range(5):
        skeleton.append({'label': lbls[3], 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_INPUT'})
    skeleton.append({'label': lbls[7], 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'})
    skeleton.append({'label': lbls[8], 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'})
    return skeleton

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    cfg = get_language_config(subject_name)
    lbls = cfg['labels']
    itinerary = kwargs.get('itinerary', None)
    
    if not itinerary:
        name_upper = subject_name.upper()
        # Detección agresiva: si contiene Minor/Mínor, es Minor.
        if re.search(r"M[IÍ]NOR", name_upper) or "SEGUNDA LENGUA" in name_upper:
            itinerary = "MINOR"
        else:
            itinerary = "MAIOR"

    if itinerary == "MINOR":
        skel = _build_minor_skeleton(lbls)
    else:
        skel = _build_maior_skeleton(lbls)
    return {
        'requires_api_stimulus': True,
        'prompt_func': 'generate_languages_stimuli_prompt',
        'skeleton': skel
    }


def generate_languages_exam_prompt(reading_text: str, listening_text: str) -> str:
    """
    [DEPRECATED] Función de compatibilidad para evitar ImportError en assessment/tasks.py.
    Mantiene vivo el sistema mientras se migran las tareas antiguas.
    """
    return f"""OBJETIVO: Generar preguntas sobre el texto.
    TEXTO: {reading_text[:500]}...
    INSTRUCCIONES: Genera 5 preguntas en formato JSON estándar."""