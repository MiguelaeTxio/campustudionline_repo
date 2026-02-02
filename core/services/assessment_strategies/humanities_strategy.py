import json

def generate_item_prompt(content_text, question_obj, **kwargs):
    already_covered = kwargs.get("already_covered", [])
    objectives = kwargs.get("learning_objectives", {})
    syllabus = kwargs.get("syllabus", [])
    
    memory_context = ""
    if already_covered:
        memory_context = "\nCRITICAL: DO NOT REPEAT these previous topics:\n" + "\n".join([f"- {p[:80]}" for p in already_covered])

    prompt = f"""ACT AS A HUMANITIES CHAIR (UGR). 
PEDAGOGICAL CONTEXT: {json.dumps(objectives)} | SYLLABUS: {json.dumps(syllabus)}
SOURCE MATERIAL: {content_text}
{memory_context}

TASK: Generate ONE (1) question for "{question_obj.section_label}".
Type: {question_obj.interaction_type}.

RULES:
1. Instructions and content MUST be in Spanish.
2. If Type is QT_SEL: Provide 4 UNIQUE and plausible options.
3. If Type is QT_PROD: Ask for an academic essay or critical analysis. Tell the student to take a PHOTO of their work.
JSON SCHEMA: {{"question_text": "...", "options": ["opt1", "opt2", "opt3", "opt4"], "model_answer": "..."}}"""
    return prompt

def get_strategy_skeleton(content_text, subject_name, **kwargs):
    return {
        'skeleton': [
            {'section_label': 'Contextualización', 'interaction_type': 'QT_SEL', 'response_mode': 'REQ_RADIO'},
            {'section_label': 'Comentario de Fuente', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'},
            {'section_label': 'Ensayo Dialéctico', 'interaction_type': 'QT_PROD', 'response_mode': 'REQ_DUAL'}
        ]
    }
