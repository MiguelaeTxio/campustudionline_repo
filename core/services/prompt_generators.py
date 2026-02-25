# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/prompt_generators.py
from typing import List, Dict

def generate_course_metadata_prompt(topic_description: str, academic_context: str = "") -> str:
    """
    Generates the prompt for course metadata generation using instructional design expertise.
    ---
    Genera el prompt para la creación de metadatos del curso utilizando experiencia en diseño instruccional.
    """
    context_section = f"Contexto académico: {academic_context}\n" if academic_context else ""
    return (
        "Actúa como un experto en diseño instruccional. Genera un JSON con metadatos para el curso:\n"
        f'**Tema:** "{topic_description}"\n\n{context_section}'
        "Responde en JSON con: descripcion_corta, audiencia, requisitos_previos, objetivos_aprendizaje, clasificacion_intelectual."
    )

def generate_master_schema_prompt(topic_description: str, academic_context: str = "", learning_objectives: str = "", syllabus: str = "") -> str:
    """
    Generates the prompt for the creation of a master syllabus/schema by a professor.
    ---
    Genera el prompt para la creación de un temario o esquema maestro por parte de un catedrático.
    """
    return f"Actúa como catedrático. Crea una Tabla de Contenidos para la asignatura: {topic_description}. Basado en: {syllabus}."

def generate_atomic_content_prompt(course_title: str, section_title: str, master_schema: str, academic_context: str = "") -> str:
    """
    Generates the prompt for the atomic generation of content for a specific book section.
    ---
    Genera el prompt para la generación atómica de contenido para una sección específica del libro.
    """
    return f"Desarrolla la sección: {section_title} del libro {course_title}. Contexto: {academic_context}."

# [REFACTOR NUCLEAR] Assessment prompts delegados a las estrategias vía Factory.
# Se elimina la función de clasificación antigua por dependencia inexistente.
