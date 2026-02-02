import re
import json

def get_script_family(target_lang):
    """Determina la familia de grafías para aplicar reglas de UI y pedagogía."""
    lang_upper = target_lang.upper()
    if any(x in lang_upper for x in ["CHINO", "JAPONÉS", "KANJI", "HANZI", "MANDARÍN"]):
        return "LOGOGRAPHIC"
    if any(x in lang_upper for x in ["ÁRABE", "HEBREO", "PERSA"]):
        return "RTL"
    if any(x in lang_upper for x in ["RUSO", "UCRANIANO", "BULGARO", "CIRÍLICO"]):
        return "CYRILLIC"
    return "LATIN"

def get_target_language(subject_name):
    """Limpia el nombre de la asignatura para obtener el idioma puro."""
    clean_name = re.sub(r"\b(LENGUA|MODERNA|MODERNO|MINOR|MAIOR|MÍNOR|INICIAL|INTERMEDIO|AVANZADO|NIVEL|IDIOMA|LENGUA\s+[A-C])\b|[0-9]+|[:()]|\b[IVXLC]+\b", "", subject_name, flags=re.IGNORECASE)
    return clean_name.strip()

def is_minor_language(subject_name):
    """Utilidad para clasificación automática de itinerario."""
    name = subject_name.upper()
    return any(x in name for x in ["MINOR", "MÍNOR", "IDIOMA MODERNO", "LENGUA C", "INICIAL", "A1", "A2", "NIVEL 1", "NIVEL I"])

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """Define la estructura del examen según el itinerario."""
    target_lang = get_target_language(subject_name)
    script_family = get_script_family(target_lang)
    itinerary = kwargs.get("itinerary", "MINOR")
    skeleton = []
    if itinerary == "MINOR":
        for _ in range(3): skeleton.append({"section_label": "Vocabulario", "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"})
        for _ in range(4): skeleton.append({"section_label": "Gramática", "interaction_type": "QT_CLZ_OPT", "response_mode": "REQ_DROP"})
        if script_family == "LOGOGRAPHIC":
            skeleton.append({"section_label": "Caligrafía y Orden de Trazos", "interaction_type": "QT_PROD", "response_mode": "REQ_DUAL"})
        skeleton.append({"section_label": "Sintaxis y Traducción Aplicada", "interaction_type": "QT_PROD", "response_mode": "REQ_DUAL"})
        return {"requires_api_stimulus": False, "skeleton": skeleton, "itinerary": itinerary, "target_lang": target_lang}
    
    for _ in range(5): skeleton.append({'section_label': 'Reading Comprehension', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'})
    for _ in range(5): skeleton.append({'section_label': 'Language Use', 'interaction_type': 'QT_CLZ_OPT', 'response_mode': 'REQ_DROP'})
    for _ in range(2): skeleton.append({'section_label': 'Writing Task', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'})
    return {"requires_api_stimulus": True, "prompt_func": "generate_languages_stimuli_prompt", "skeleton": skeleton, "itinerary": itinerary, "target_lang": target_lang}

def generate_languages_stimuli_prompt(content_text, subject_name, **kwargs):
    target_lang = get_target_language(subject_name)
    return f"""ACT AS AN ACADEMIC EXAMINER. Generate Reading and Listening in {target_lang}. Syllabus: {content_text[:2000]} JSON: {{"reading_stimulus": "...", "listening_transcript": "...", "cefr_level": "..."}}"""

def generate_item_prompt(content_text, question_obj, **kwargs):
    """Motor de Generación: Blindaje Cloze (Prohibición de Teoría)."""
    target_lang = kwargs.get("target_lang", "English")
    itinerary = kwargs.get("itinerary", "MINOR")
    already_covered = kwargs.get("already_covered", [])
    instr_lang = "Spanish" if itinerary == "MINOR" else target_lang
    
    memory_context = ""
    if already_covered:
        memory_context = "\nCRITICAL: DO NOT REPEAT these previous questions/topics:\n" + "\n".join([f"- {p[:80]}" for p in already_covered])

    prompt = f"""ACT AS AN EXPERT PROFESSOR (UGR). TARGET: {target_lang}.
SOURCE MATERIAL: {content_text}
{memory_context}

TASK: Generate ONE (1) question for "{question_obj.section_label}".
Type: {question_obj.interaction_type}.

CRITICAL RULES FOR CLOZE (QT_CLZ_OPT / QT_CLZ_OPN):
1. MANDATORY: Create a PRACTICAL SENTENCE in {target_lang} with exactly ONE gap marked as "[...]".
2. PROHIBITED: Do not ask theoretical questions (e.g., "What does this mean?" or "When is X used?").
3. PROHIBITED: Do not mention lesson numbers or syllabus references in the question text.
4. EXAMPLE: "Yesterday I [...] to the cinema" instead of "What is the past of go?".

GENERAL RULES:
1. Instructions in {instr_lang}.
2. For multiple choice: 4 UNIQUE and plausible options.
3. For QT_PROD: Ask the student to take a PHOTO of the exercise.

JSON SCHEMA:
{{
  "question_text": "Practical sentence with [...] in {target_lang}. Instructions in {instr_lang}.",
  "options": ["opt1", "opt2", "opt3", "opt4"],
  "model_answer": "Correct answer"
}}"""
    return prompt

generate_languages_item_prompt = generate_item_prompt
