import re

with open("/home/MiguelAeTxio/SWAP/languages_strategy_atomic.py.prop", "r") as f:
    content = f.read()

# 1. Corregir Clasificador (Prioridad Minor)
old_skeleton = r"def get_strategy_skeleton\(content_text, subject_name, \*\*kwargs\):.*?if itinerary == \"MINOR\":"
new_skeleton = """def get_strategy_skeleton(content_text, subject_name, **kwargs):
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

    if itinerary == "MINOR":"""

content = re.sub(old_skeleton, new_skeleton, content, flags=re.DOTALL)

# 2. Reemplazar la generación masiva por la generación Atómica (1:1)
# Eliminamos la función antigua y añadimos la nueva
old_exam_func_pattern = r"def generate_languages_exam_prompt\(.*?\).*?JSON OUTPUT:.*?\}\"\"\""
new_atomic_func = """def generate_languages_item_prompt(reading_text: str, listening_transcript: str, cefr_level: str, target_lang: str, question_obj) -> str:
    \"\"\"Genera el prompt para rrellenar UN SOLO objeto Question (Flujo Atómico).\"\"\"
    section = question_obj.section_label
    q_type = question_obj.interaction_type
    
    return f\"\"\"ACT AS: Expert Language Teacher ({target_lang}) for Spanish students.
TASK: Generate the pedagogical content for ONE specific exam item.

[REFERENCE_TEXT]
{reading_text if question_obj.source_type == 'SRC_TXT' else listening_transcript}
[/REFERENCE_TEXT]

ITEM METADATA:
- Section: {section}
- Interaction Type: {q_type}
- Level: {cefr_level}

MANDATORY RULES:
1. LANGUAGE: Instructions ('question_text') MUST be in SPANISH. Content and options MUST be in {target_lang}.
2. CLOZE: If type is QT_CLZ_OPT or QT_CLZ_OPN, 'question_text' must be a sentence in {target_lang} with a [...] gap, preceded by the instruction in Spanish.
3. NO NUMBERING: Do not include question numbers or technical tags.

JSON OUTPUT FORMAT:
{{
  "question_text": "Spanish instruction + Content",
  "interaction_type": "{q_type}",
  "options": ["Option1 in {target_lang}", "Option2", "Option3", "Option4"],
  "model_answer": "Correct answer in {target_lang}"
}}\"\"\""""

content = re.sub(old_exam_func_pattern, new_atomic_func, content, flags=re.DOTALL)

with open("/home/MiguelAeTxio/SWAP/languages_strategy_atomic.py.prop", "w") as f:
    f.write(content)
