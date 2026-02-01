# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/prompt_generators.py
from typing import List, Dict

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
    from core.services.assessment_strategies.classifier import generate_classifier_prompt
    return generate_classifier_prompt(subject_name, branch_name)

# [REFACTOR NUCLEAR] Assessment prompts delegados a las estrategias vía Factory
