import json

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

def generate_languages_exam_prompt(reading_text: str, listening_transcript: str, cefr_level: str = "B1") -> str:
    return f"""Eres un Tribunal de Acreditación Lingüística ACLES/UGR.
Crea un examen basado en el Reading y Listening proporcionados.
NIVEL: {cefr_level}.

REGLAS DE ORO:
1. Idioma: Todo el contenido (enunciados, opciones, respuestas) DEBE estar en el idioma del examen.
2. Contrato Cloze: Para preguntas tipo 'QT_CLZ_OPT' o 'QT_CLZ_OPN', DEBES insertar los huecos en el 'question_text' usando corchetes.
   Ejemplo: "Hoy [hace/está] un buen día" o "Yo [tengo] hambre".
3. No incluyas letras de opción (a, b, c) en las cadenas de texto de 'options'.

JSON STRUCTURE:
{{
  "questions": [
    {{
      "question_text": "Texto con [...] si aplica",
      "interaction_type": "QT_SEL | QT_CLZ_OPT | QT_CLZ_OPN | QT_TRF | QT_PROD",
      "options": ["opcion1", "opcion2"],
      "model_answer": "respuesta_exacta"
    }}
  ]
}}"""

def _build_maior_skeleton(lbls):
    """
    ITINERARIO MAIOR (Estándar ACLES): Alta Densidad.
    Total: ~35-40 preguntas.
    """
    skeleton = []
    
    # Bloque 1: Comprensión Lectora (10 ítems)
    # Tarea 1.1: Selección Múltiple (5 ítems)
    for _ in range(5):
        skeleton.append({'label': lbls[0], 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'})
    # Tarea 1.2: Emparejamiento (Simulado con Matching/Selection para simplicidad de v1)
    for _ in range(5):
        skeleton.append({'label': lbls[1], 'source': 'SRC_TXT', 'interaction': 'QT_MATCH', 'response': 'REQ_MATCH'})

    # Bloque 2: Uso de la Lengua (15 ítems)
    # Tarea 2.1: Cloze (10 huecos)
    for _ in range(10):
        skeleton.append({'label': lbls[2], 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPT', 'response': 'REQ_DROP'})
    # Tarea 2.2: Keyword Transformation (5 frases)
    for _ in range(5):
        skeleton.append({'label': lbls[4], 'source': 'SRC_DIR', 'interaction': 'QT_TRF', 'response': 'REQ_INPUT'})

    # Bloque 3: Comprensión Auditiva (8 ítems)
    for _ in range(8):
        skeleton.append({'label': lbls[5], 'source': 'SRC_AUD', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'})

    # Bloque 4: Expresión Escrita (2 ítems)
    skeleton.append({'label': lbls[7], 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}) # Carta
    skeleton.append({'label': lbls[7], 'source': 'SRC_TXT', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}) # Ensayo

    # Bloque 5: Expresión Oral (1 ítem)
    skeleton.append({'label': lbls[8], 'source': 'SRC_AUD', 'interaction': 'QT_PROD', 'response': 'REQ_REC'})
    
    return skeleton

def _build_minor_skeleton(lbls):
    """
    ITINERARIO MINOR (Syllabus Based): Densidad Media.
    Total: ~17 ítems.
    """
    skeleton = []
    
    # Bloque 1: Comprensión y Gramática (15 ítems)
    for _ in range(5): # Reading
        skeleton.append({'label': lbls[0], 'source': 'SRC_TXT', 'interaction': 'QT_SEL', 'response': 'REQ_RADIO'})
    for _ in range(5): # Ordenación (simulada con Cloze Open para MVP)
        skeleton.append({'label': lbls[3], 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_INPUT'})
    for _ in range(5): # Vocabulario exacto
        skeleton.append({'label': lbls[3], 'source': 'SRC_DIR', 'interaction': 'QT_CLZ_OPN', 'response': 'REQ_INPUT'})

    # Bloque 2: Producción (2 ítems)
    skeleton.append({'label': lbls[7], 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'})
    skeleton.append({'label': lbls[8], 'source': 'SRC_DIR', 'interaction': 'QT_PROD', 'response': 'REQ_DUAL'}) # Caligrafía/Oral simple

    return skeleton

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """
    Factory method para obtener la estructura del examen.
    [HITO 6] Ahora soporta itinerarios MAIOR/MINOR.
    """
    cfg = get_language_config(subject_name)
    lbls = cfg['labels']
    
    # Detección de itinerario (si se pasa en kwargs o por nombre)
    itinerary = kwargs.get('itinerary', None)
    
    # Fallback de detección por nombre si no viene explícito
    if not itinerary:
        name_upper = subject_name.upper()
        if "MAIOR" in name_upper or "ESPECIALIDAD" in name_upper:
            itinerary = "MAIOR"
        elif "MINOR" in name_upper or "SEGUNDA LENGUA" in name_upper:
            itinerary = "MINOR"
        else:
            itinerary = "MAIOR" # Default UGR

    if itinerary == "MINOR":
        skel = _build_minor_skeleton(lbls)
    else:
        skel = _build_maior_skeleton(lbls)

    return {
        'requires_api_stimulus': True,
        'prompt_func': 'generate_languages_stimuli_prompt',
        'skeleton': skel
    }
