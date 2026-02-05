import re
import json

def get_script_family(target_lang):
    lang_upper = target_lang.upper()
    if any(x in lang_upper for x in ["CHINO", "JAPONÉS", "KANJI", "HANZI", "MANDARÍN"]): return "LOGOGRAPHIC"
    if any(x in lang_upper for x in ["ÁRABE", "HEBREO", "PERSA"]): return "RTL"
    if any(x in lang_upper for x in ["RUSO", "UCRANIANO", "BULGARO", "CIRÍLICO"]): return "CYRILLIC"
    return "LATIN"

def get_target_language(subject_name):
    clean_name = re.sub(r"\b(LENGUA|MODERNA|MODERNO|MINOR|MAIOR|MÍNOR|INICIAL|INTERMEDIO|AVANZADO|NIVEL|IDIOMA|LENGUA\s+[A-C])\b|[0-9]+|[:()]|\b[IVXLC]+\b", "", subject_name, flags=re.IGNORECASE)
    return clean_name.strip()

def is_minor_language(subject_name):
    name = subject_name.upper()
    return any(x in name for x in ["MINOR", "MÍNOR", "IDIOMA MODERNO", "LENGUA C", "INICIAL", "A1", "A2", "NIVEL 1", "NIVEL I"])

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    target_lang = get_target_language(subject_name)
    itinerary = kwargs.get("itinerary", "MINOR")
    # Esqueleto técnico agnóstico (LBL_...)
    skeleton = [
        {"section_label": "LBL_READING", "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
        {"section_label": "LBL_READING", "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
        {"section_label": "LBL_LISTENING", "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
        {"section_label": "LBL_LISTENING", "interaction_type": "QT_SEL", "response_mode": "REQ_RADIO"},
        {"section_label": "LBL_WRITING", "interaction_type": "QT_PROD", "response_mode": "REQ_DUAL"},
        {"section_label": "LBL_SPEAKING", "interaction_type": "QT_PROD", "response_mode": "REQ_REC"}
    ]
    return {
        "requires_api_stimulus": True,
        "prompt_func": "generate_languages_stimuli_prompt",
        "skeleton": skeleton,
        "itinerary": itinerary,
        "target_lang": target_lang
    }

def generate_languages_stimuli_prompt(content_text, subject_name, **kwargs):
    target_lang = get_target_language(subject_name)
    return f"""ACT AS AN ACADEMIC EXAMINER (UGR). 
Generate Reading/Listening stimuli for {target_lang}.

PEDAGOGICAL RULES (CRITICAL):
1. Detect Level from subject: "{subject_name}".
2. If MINOR (A1-B2): 'ui_labels' MUST be bilingüal ("{{Target}} / Castellano").
3. If MAIOR (C1-C2): 'ui_labels' MUST be 100% in {target_lang}.

JSON SCHEMA:
{{
  "reading_stimulus": "Markdown content in {target_lang}",
  "listening_transcript": "Transcript for TTS in {target_lang}",
  "cefr_level": "Level",
  "ui_labels": {{
    "LBL_READING": "Reading Label",
    "LBL_LISTENING": "Listening Label",
    "LBL_WRITING": "Writing Label",
    "LBL_SPEAKING": "Speaking Label",
    "submit_button": "Submit Text",
    "write_placeholder": "Placeholder Text"
  }}
}}"""

def generate_item_prompt(content_text, question_obj, **kwargs):
    target_lang = kwargs.get("target_lang", "English")
    itinerary = kwargs.get("itinerary", "MINOR")
    already_covered = kwargs.get("already_covered", [])
    instr_lang = "Spanish" if itinerary == "MINOR" else target_lang
    forbidden = "\n".join([f"- {p[:60]}" for p in already_covered])
    
    return f"""ACT AS AN EXPERT PROFESSOR (UGR). TARGET: {target_lang}.
TASK: Generate ONE exercise for '{question_obj.section_label}'.

STRICT RULES:
1. CONTENT: The exercise/sentence MUST BE 100% in {target_lang}. NO Spanish/English words.
2. INSTRUCTIONS: Place brief technical instruction at the start in {instr_lang}.
3. NO REPETITION: Do not repeat concepts from:
{forbidden}

JSON SCHEMA:
{{
  "question_text": "Instruction in {instr_lang}.\\n\\nExercise in {target_lang}.",
  "options": ["opt1", "opt2", "opt3", "opt4"],
  "model_answer": "Answer"
}}"""

def get_ui_labels(subject_name, **kwargs):
    target_lang = get_target_language(subject_name)
    return {
        "LBL_READING": f"{target_lang} / Lectura",
        "LBL_LISTENING": f"{target_lang} / Escucha",
        "LBL_WRITING": f"{target_lang} / Escritura",
        "LBL_SPEAKING": f"{target_lang} / Grabación",
        "submit_button": "Entregar Evaluación",
        "write_placeholder": "Escribe aquí..."
    }

def generate_correction_prompt(question_text, model_answer, student_answer):
    return f"Grade this: Q:{question_text} Model:{model_answer} Student:{student_answer}. Feedback in Spanish."
