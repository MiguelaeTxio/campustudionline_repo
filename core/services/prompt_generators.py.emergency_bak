from typing import List, Dict
from core.services.assessment_strategies import (
    generate_sciences_prompt,
    generate_legal_prompt,
    generate_health_prompt,
    generate_humanities_prompt,
    generate_languages_stimuli_prompt,
    generate_classifier_prompt
)

def generate_course_metadata_prompt(topic_description: str, academic_context: str = "") -> str:
    context_section = f"Contexto académico: {academic_context}\n" if academic_context else ""
    return (
        "Actúa como un experto en diseño instruccional. Genera un JSON con metadatos para el curso:\n"
        f'**Tema:** "{topic_description}"\n\n{context_section}'
        "Responde en JSON con: descripcion_corta, audiencia, requisitos_previos, objetivos_aprendizaje, clasificacion_intelectual."
    )

def generate_master_schema_prompt(topic_description: str, academic_context: str = "", learning_objectives: str = "", syllabus: str = "") -> str:
    return f"Actúa como catedrático. Crea una Tabla de Contenidos para la asignatura: {topic_description}. Basado en: {syllabus}."

def generate_atomic_content_prompt(course_title: str, section_title: str, master_schema: str, academic_context: str = "") -> str:
    return f"Desarrolla la sección: {section_title} del libro {course_title}. Contexto: {academic_context}."

def generate_classification_prompt(subject_name: str, branch_name: str) -> str:
    return generate_classifier_prompt(subject_name, branch_name)

def generate_assessment_prompt(content_text: str, subject_type: str = "HUMANITIES_ARTS", segment_info: str = "Evaluación Global", learning_objectives: str = "", subject_name: str = "Asignatura General") -> str:
    if subject_type == "LOGIC_AND_TECH":
        return generate_sciences_prompt(content_text, subject_name=subject_name)
    if subject_type == "CEFR_LANGUAGES":
        return generate_languages_stimuli_prompt(content_text, subject_name)
    if subject_type == "SOCIO_LEGAL":
        return generate_legal_prompt(content_text, subject_name=subject_name)
    if subject_type == "HEALTH_SCIENCES":
        return generate_health_prompt(content_text, subject_name=subject_name)
    return generate_humanities_prompt(content_text, subject_name=subject_name, subject_type=subject_type)

def generate_ugr_questions_prompt(reading_text: str, listening_text: str, subject_type: str = "HUMANITIES") -> str:
    from core.services.assessment_strategies import generate_languages_exam_prompt
    return generate_languages_exam_prompt(reading_text, listening_text)

# --- WRAPPER DE COMPATIBILIDAD (Para orchestrator/tasks.py) ---
def generate_stimulus_creation_prompt(content_source: str, subject_name: str, subject_type: str = "HUMANITIES") -> str:
    """
    Wrapper para mantener compatibilidad con llamadas antiguas desde orchestrator.
    Redirige a la estrategia moderna de idiomas.
    """
    return generate_languages_stimuli_prompt(content_source, subject_name)
