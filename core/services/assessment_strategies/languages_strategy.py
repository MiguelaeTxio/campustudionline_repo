import re
import json

def is_minor_language(subject_name):
    """Identifica si es un nivel inicial (A1-A2) por palabras clave."""
    name = subject_name.upper()
    return any(x in name for x in ["MINOR", "MÍNOR", "IDIOMA MODERNO", "LENGUA C", "INICIAL", "A1", "A2", "NIVEL 1", "NIVEL I"])

def get_target_language(subject_name):
    """Extrae el idioma puro eliminando el ruido administrativo."""
    clean_name = re.sub(r'\b(LENGUA|MODERNA|MODERNO|MINOR|MAIOR|MÍNOR|INICIAL|INTERMEDIO|AVANZADO|NIVEL|IDIOMA|LENGUA\s+[A-C])\b|[0-9]+|[:()]|\b[IVXLC]+\b', '', subject_name, flags=re.IGNORECASE)
    return clean_name.strip()

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """Estructura atómica (Minor) o compleja (Maior) con etiquetas genéricas."""
    target_lang = get_target_language(subject_name)
    itinerary = kwargs.get('itinerary') or ("MINOR" if is_minor_language(subject_name) else "MAIOR")

    skeleton = []
    if itinerary == "MINOR":
        # Bloques Minor (Instrucciones en ES, Contenido en Idioma Objetivo)
        for _ in range(5): skeleton.append({'section_label': 'Vocabulario', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(5): skeleton.append({'section_label': 'Gramática', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP'})
        for _ in range(5): skeleton.append({'section_label': 'Sintaxis', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_ORDER', 'response_mode': 'REQ_ORDER'})
        for _ in range(2): skeleton.append({'section_label': 'Escritura', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
        return {'requires_api_stimulus': False, 'skeleton': skeleton, 'itinerary': itinerary, 'target_lang': target_lang}
    else:
        # Bloques Maior (Inmersión Total)
        for _ in range(10): skeleton.append({'section_label': 'Reading Comprehension', 'source_type': 'SRC_TXT', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(10): skeleton.append({'section_label': 'Language Use', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP'})
        for _ in range(5): skeleton.append({'section_label': 'Transformation', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_TRF', 'response_mode': 'REQ_INPUT'})
        for _ in range(8): skeleton.append({'section_label': 'Listening', 'source_type': 'SRC_AUD', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
        for _ in range(2): skeleton.append({'section_label': 'Writing', 'source_type': 'SRC_DIR', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
        skeleton.append({'section_label': 'Speaking', 'source_type': 'SRC_AUD', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_REC'})
        return {'requires_api_stimulus': True, 'prompt_func': 'generate_languages_stimuli_prompt', 'skeleton': skeleton, 'itinerary': itinerary, 'target_lang': target_lang}

def generate_languages_stimuli_prompt(content_text, subject_name):
    """Genera estímulo obligando a la IA a identificar el idioma y usarlo."""
    target_lang = get_target_language(subject_name)
    return f"""ACT AS AN ACADEMIC CHAIR.
TASK: Generate a Reading Stimulus (500 words) in the target language: {target_lang}.
STRICT RULE: The field 'reading_stimulus' MUST contain ONLY the clean text in {target_lang}. 
No JSON nesting. No title/author keys.
CONTENT BASE: {content_text[:1200]}"""

def generate_languages_item_prompt(reading_text, listening_transcript, cefr_level, question_obj, itinerary='MAIOR', target_lang='ENGLISH'):
    """Prompt Universal: Delega la localización de la etiqueta en la IA."""
    q_type = question_obj.interaction_type
    original_label = question_obj.section_label
    
    if itinerary == 'MINOR':
        return f"""ACT AS AN EXAM CREATOR FOR THE LANGUAGE: {target_lang}.
STRICT RULE: JSON ONLY. NO PREAMBLE. NO CONVERSATION.
STUDENT: Spanish speaker (Beginner). 
TASK: Create ONE (1) question of type {q_type}.
INSTRUCTIONS: In SPANISH.
CONTENT: In {target_lang}. NO ENGLISH.
LOCALIZATION: Translate the section label '{original_label}' to {target_lang}.
SCHEMA: {{"question_text": "...", "options": ["...", "..."], "model_answer": "..."}}
FIELD 'model_answer': MANDATORY."""
    
    return f"""ACT AS A NATIVE EXAMINER IN {target_lang}.
STRICT IMMERSION: Use 100% {target_lang}. 
TASK: ONE (1) {q_type} question.
LOCALIZATION: Translate the header '{original_label}' to {target_lang}.
JSON SCHEMA: {{"question_text": "...", "options": ["...", "..."], "model_answer": "..."}}"""
