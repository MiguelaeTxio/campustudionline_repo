import re
import json

def is_minor_language(subject_name):
    """Determina si la asignatura pertenece al itinerario Minor (A1-B2) según normativa UGR."""
    name = subject_name.upper()
    return any(x in name for x in ["MINOR", "MÍNOR", "IDIOMA MODERNO", "LENGUA C", "INICIAL", "A1", "A2", "NIVEL 1", "NIVEL I"])

def get_script_family(target_lang):
    """Identifica la familia de escritura para lógica de widgets (Logográficos/RTL)."""
    lang_upper = target_lang.upper()
    if any(x in lang_upper for x in ["CHINO", "JAPONÉS", "KANJI", "HANZI", "MANDARÍN"]): return "LOGOGRAPHIC"
    if any(x in lang_upper for x in ["ÁRABE", "HEBREO", "PERSA"]): return "RTL"
    if any(x in lang_upper for x in ["RUSO", "UCRANIANO", "BULGARO", "CIRÍLICO"]): return "CYRILLIC"
    return "LATIN"

def get_target_language(subject_name):
    """Extrae el nombre de la lengua del nombre de la asignatura."""
    clean_name = re.sub(r"\b(LENGUA|MODERNA|MODERNO|MINOR|MAIOR|MÍNOR|INICIAL|INTERMEDIO|AVANZADO|NIVEL|IDIOMA|LENGUA\s+[A-C])\b|[0-9]+|[:()]|\b[IVXLC]+\b", "", subject_name, flags=re.IGNORECASE)
    return clean_name.strip()

def get_ui_labels(subject_name, **kwargs):
    """Genera etiquetas bilingües deterministas (Minor) o en Target (Maior)."""
    target_lang = get_target_language(subject_name)
    itinerary = kwargs.get("itinerary", "MINOR")
    if itinerary == "MAIOR":
        return {
            "LBL_READING": f"{target_lang} / Reading",
            "LBL_LISTENING": f"{target_lang} / Listening",
            "LBL_WRITING": f"{target_lang} / Writing",
            "LBL_SPEAKING": f"{target_lang} / Speaking",
            "submit_button": "Submit Assessment",
            "write_placeholder": "Write here..."
        }
    return {
        "LBL_READING": f"{target_lang} / Lectura",
        "LBL_LISTENING": f"{target_lang} / Escucha",
        "LBL_WRITING": f"{target_lang} / Escritura",
        "LBL_SPEAKING": f"{target_lang} / Grabación",
        "submit_button": "Entregar Evaluación",
        "write_placeholder": "Escribe aquí..."
    }

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    """Fase A: Define la estructura física del examen."""
    itinerary = kwargs.get("itinerary", "MINOR")
    labels = get_ui_labels(subject_name, itinerary=itinerary)
    return {
        "skeleton": [
            {"section_label": labels["LBL_READING"], "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
            {"section_label": labels["LBL_READING"], "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
            {"section_label": labels["LBL_LISTENING"], "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
            {"section_label": labels["LBL_LISTENING"], "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
            {"section_label": labels["LBL_WRITING"], "interaction_type": "QT_PROD", "response_mode": "REQ_DUAL"},
            {"section_label": labels["LBL_SPEAKING"], "interaction_type": "QT_PROD", "response_mode": "REQ_REC"}
        ],
        "itinerary": itinerary,
        "ui_labels": labels,
        "requires_api_stimulus": True,
        "prompt_func": "generate_languages_stimuli_prompt"
    }

def generate_languages_stimuli_prompt(content_text, subject_name, **kwargs):
    """Genera el estímulo inicial con restricciones de nivel UGR."""
    target_lang = get_target_language(subject_name)
    return f"ACT AS AN ACADEMIC EXAMINER (UGR). LEVEL: HSK 3 / A2+. LENGTH: MAX 200 chars. SUBJECT: {target_lang}. JSON: {{'reading_stimulus': '...', 'listening_transcript': '...', 'cefr_level': 'A2/B1'}}"

def generate_item_prompt(content_text, question_obj, **kwargs):
    """Fase B: Relleno de ítems con blindaje de idioma."""
    target_lang = get_target_language(kwargs.get("target_lang", "Lengua Objetivo"))
    itinerary = kwargs.get("itinerary", "MINOR")
    instr_lang = "Spanish" if itinerary == "MINOR" else target_lang
    r_stimulus = kwargs.get("reading_stimulus", "")
    l_stimulus = kwargs.get("listening_transcript", "")
    
    context = f"STIMULUS: {r_stimulus}" if "Lectura" in question_obj.section_label else (f"STIMULUS: {l_stimulus}" if "Escucha" in question_obj.section_label else f"SOURCE: {content_text[:400]}")

    rules = "TYPE: MULTIPLE CHOICE (4 opts)" if question_obj.interaction_type == "QT_SEL" else "TYPE: OPEN PRODUCTION (No opts)"

    return f"ACT AS PROFESSOR (UGR). SUBJECT: {target_lang}. {context}. TASK: {question_obj.section_label}. {rules}. INSTR: {instr_lang}. CONTENT: {target_lang}. JSON: {{'question_text': '...', 'options': [...], 'model_answer': '...'}}"

def generate_correction_prompt(question_text, model_answer, student_answer):
    return f"Grade this: Q:{question_text} Model:{model_answer} Student:{student_answer}. Feedback in Spanish."
