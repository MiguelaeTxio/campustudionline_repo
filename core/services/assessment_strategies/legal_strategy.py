import json

def generate_item_prompt(content_text, question_obj, **kwargs):
    already_covered = kwargs.get("already_covered", [])
    objectives = kwargs.get("learning_objectives", {})
    syllabus = kwargs.get("syllabus", [])

    memory_context = ""
    if already_covered:
        memory_context = "\nDO NOT REPEAT these legal issues:\n" + "\n".join([f"- {p[:80]}" for p in already_covered])

    prompt = f"""ACT AS A LAW PROFESSOR (UGR). 
SYLLABUS: {json.dumps(syllabus)}
SOURCE (Case Study): {content_text}
{memory_context}

TASK: Generate ONE (1) legal question for "{question_obj.section_label}".
Type: {question_obj.interaction_type}.

RULES:
1. Force use of precise legal terminology.
2. If QT_SEL: 4 UNIQUE options citing articles if possible.
3. If QT_PROD: Request a legal opinion (dictamen). Tell the student to take a PHOTO of their handwritten draft.
JSON SCHEMA: {{"question_text": "...", "options": ["opt1", "opt2", "opt3", "opt4"], "model_answer": "Legal grounds"}}"""
    return prompt

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'section_label': 'Identificación Normativa', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'},
            {'section_label': 'Fundamentación Jurídica', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'},
            {'section_label': 'Dictamen Final', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'}
        ]
    }
