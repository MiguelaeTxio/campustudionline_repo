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
        return ["Comprensión Lectora (阅读理解)", "Ordenación de Frases (句子排序)", "Gramática (语法)", "Cloze Abierto (完形填空)", "Transformación (句型转换)", "Comprensión Auditiva (听力理解)", "Dictado (听写)", "Expresión Escrita (写作)", "Caligrafía y Trazos (书法/写字)"]
    return ["Comprensión Lectora", "Ordenación de Frases", "Gramática", "Cloze Abierto", "Transformación de Frases", "Comprensión Auditiva", "Dictado", "Expresión Escrita", "Expresión Oral"]

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

    # [HITO 6] Blindaje Lingüístico Anti-Inglés e Inmersión en Castellano
    system_instruction = ""
    if itinerary == 'MINOR':
        system_instruction = f"""
*** REGLA DE ORO DE IDIOMA (CUMPLIMIENTO OBLIGATORIO) ***
- EL ESTUDIANTE ES ESPAÑOL Y NO ENTIENDE NADA DE INGLÉS (ENGLISH IS FORBIDDEN).
- EL CAMPO 'question_text' DEBE CONTENER EXCLUSIVAMENTE CASTELLANO Y {target_lang}.
- PROHIBICIÓN ABSOLUTA: NO UTILICES NI UNA SOLA PALABRA EN INGLÉS EN EL RESULTADO.
- ESTRUCTURA OBLIGATORIA DEL 'question_text':
    1. INSTRUCCIÓN EN CASTELLANO (Ej: 'Teniendo en cuenta el texto anterior, responde...')
    2. SALTO DE LÍNEA (\n).
    3. CONTENIDO/PREGUNTA EN {target_lang}.
"""
    else:
        system_instruction = f"The 'question_text' MUST be 100% in {target_lang}. ENGLISH IS STRICTLY FORBIDDEN. If the target language is not English, do not use a single English word."

    return f"""ACT AS AN EXPERT EXAM CREATOR.
TASK: Create UNA (1) question of type {q_type} for a {cefr_level} level exam.

TARGET LANGUAGE: {target_lang}
STUDENT PROFILE: Spanish speaker (Understand ONLY Spanish and the Target Language).

{system_instruction}

CONTEXT FOR GENERATION:
{context}

REGLAS CRÍTICAS DE SALIDA:
1. El campo 'question_text' NO puede contener inglés.
2. Si es {q_type} 'QT_SEL': Formula la pregunta en {target_lang}.
3. Si es {q_type} 'QT_CLZ_OPT' o 'QT_CLZ_OPN': Escribe la frase en {target_lang} con un hueco '[...]'.
4. Si es {q_type} 'QT_ORDER': Entrega una frase desordenada en {target_lang}.

EJEMPLO DE 'question_text' PARA MINOR CHINO (Bilingüe):
"Lee el siguiente enunciado y selecciona la opción correcta:\\n\\n关于春节的说法..."

SALIDA JSON PURO. SIN COMENTARIOS.
"""
