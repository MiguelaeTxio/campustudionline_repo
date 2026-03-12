from pydantic import BaseModel, Field
from typing import List, Optional

# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/gemini_schemas.py
# [V5 - HITO 6 REPAIR] Inclusión de esquemas estrictos de evaluación (Incidencias 2-7)

# --- Schema for Content Automation ---

SYLLABUS_SCHEMA = {
    "name": "generate_syllabus",
    "description": "Genera un temario estructurado para un curso a partir de un prompt.",
    "parameters": {
        "type": "object",
        "properties": {
            "descripcion_corta": {
                "type": "string",
                "description": "Una descripción concisa del curso en un párrafo (máximo 200 caracteres).",
            },
            "audiencia": {
                "type": "string",
                "description": "El público objetivo al que se dirige el curso.",
            },
            "requisitos_previos": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Una lista de conocimientos o habilidades recomendados.",
            },
            "objetivos_aprendizaje": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Una lista de lo que el estudiante será capaz de hacer al finalizar el curso.",
            },
            "clasificacion_intelectual": {
                "type": "object",
                "properties": {
                    "categoria_general": {
                        "type": "string",
                        "description": "La categoría principal a la que pertenece el curso.",
                    },
                    "subcategoria": {
                        "type": "string",
                        "description": "Una subcategoría más específica.",
                    },
                    "palabras_clave": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Una lista de palabras clave relevantes.",
                    },
                },
                "required": [
                    "categoria_general",
                    "subcategoria",
                    "palabras_clave",
                ],
            },
            "temario_detallado": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "unidad": {
                            "type": "string",
                            "description": "El título de la unidad o módulo.",
                        },
                        "temas": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Una lista de los temas específicos de la unidad.",
                        },
                    },
                    "required": ["unidad", "temas"],
                },
                "description": "La estructura detallada del curso.",
            },
            "fuentes_bibliografia": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Una lista de 5 a 10 fuentes y libros de referencia reales y relevantes.",
            },
        },
        "required": [
            "descripcion_corta",
            "audiencia",
            "requisitos_previos",
            "objetivos_aprendizaje",
            "clasificacion_intelectual",
            "temario_detallado",
            "fuentes_bibliografia",
        ],
    },
}

METADATA_SCHEMA = {
    "name": "generate_course_metadata",
    "description": "Genera los metadatos básicos y la clasificación intelectual para un curso.",
    "parameters": {
        "type": "object",
        "properties": {
            "descripcion_corta": {
                "type": "string",
                "description": "Una descripción concisa y atractiva del curso en un párrafo (máximo 250 caracteres).",
            },
            "audiencia": {
                "type": "string",
                "description": "El público objetivo específico al que se dirige el curso.",
            },
            "requisitos_previos": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Una lista de conocimientos o habilidades recomendados para el estudiante.",
            },
            "objetivos_aprendizaje": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Una lista de lo que el estudiante será capaz de hacer al finalizar el curso.",
            },
            "clasificacion_intelectual": {
                "type": "object",
                "properties": {
                    "categoria_general": {
                        "type": "string",
                        "description": "La categoría principal a la que pertenece el curso (ej: 'Ciencias de la Salud').",
                    },
                    "subcategoria": {
                        "type": "string",
                        "description": "Una subcategoría más específica (ej: 'Anatomía Patológica').",
                    },
                    "palabras_clave": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Una lista de 5 a 7 palabras clave o 'tags' relevantes para la búsqueda.",
                    },
                },
                "required": ["categoria_general", "subcategoria", "palabras_clave"],
            },
        },
        "required": [
            "descripcion_corta",
            "audiencia",
            "requisitos_previos",
            "objetivos_aprendizaje",
            "clasificacion_intelectual",
        ],
    }
}

# --- Schema for Academic Assessment (Milestone 6) ---

# --- Pydantic Schemas for Academic Assessment (Milestone 6) ---
# Sustituyen a los antiguos diccionarios para habilitar Structured Outputs nativos

class LocalizedSectionsSchema(BaseModel):
    SD_READ: Optional[List[str]] = Field(default=None, description="[Título, Instrucción]")
    SD_LIST: Optional[List[str]] = Field(default=None, description="[Título, Instrucción]")
    SD_WRIT: Optional[List[str]] = Field(default=None, description="[Título, Instrucción]")
    SD_SPEAK: Optional[List[str]] = Field(default=None, description="[Título, Instrucción]")
    SD_MEDI: Optional[List[str]] = Field(default=None, description="[Título, Instrucción]")
    SD_THEO: Optional[List[str]] = Field(default=None)
    SD_CALC: Optional[List[str]] = Field(default=None)

class AcademicClassificationSchema(BaseModel):
    archetype_id: str = Field(description="El arquetipo principal de la asignatura.")
    sub_archetype_id: str = Field(description="El ID técnico de especialidad (Ref: V06DOC_SUBARCHETYPES).")
    target_language_code: str = Field(description="Código ISO 639-1 del idioma objetivo si es ARCH_LANG (ej: 'en', 'fr', 'ja'). 'es' para el resto.")
    localized_sections: LocalizedSectionsSchema = Field(description="Traducción de títulos e instrucciones al idioma objetivo (solo para ARCH_LANG).")

class OptionSchema(BaseModel):
    id: str = Field(description="Identificador de la opción (ej: 'A', 'B', 'C', 'D').")
    text: str = Field(description="Texto de la opción.")
    is_correct: bool = Field(description="Indica si esta es la opción correcta.")
    feedback: str = Field(description="Explicación específica para esta opción.")

class ContentSchema(BaseModel):
    stem: str = Field(description="El enunciado, pregunta o estímulo principal del ítem.")
    options: Optional[List[OptionSchema]] = Field(default=None, description="Lista de opciones de respuesta (Mínimo 4 para W-OBJ-STRIKE).")
    media_assets: Optional[List[str]] = Field(default=None, description="URLs de recursos multimedia opcionales.")
    text_with_gaps: Optional[str] = Field(default=None, description="Texto continuo con huecos (Obligatorio para W-TXT-CLOZE).")

class PairSchema(BaseModel):
    izquierdo: str = Field(description="Elemento izquierdo del par.")
    derecho: str = Field(description="Elemento derecho del par vinculado.")

class GradingLogicSchema(BaseModel):
    feedback_justification: str = Field(description="Explicación pedagógica detallada de la solución correcta.")
    correct_answer: Optional[str] = Field(default=None, description="Solución correcta genérica (texto).")
    gap_solutions: Optional[List[str]] = Field(default=None, description="Soluciones en orden para los huecos de W-TXT-CLOZE.")
    pairs: Optional[List[PairSchema]] = Field(default=None, description="Pares de vinculación para W-MIX-MATCH.")

class MetadataSchema(BaseModel):
    competency_tag: str = Field(description="Etiqueta de competencia evaluada (ej: COMP_GEN, COMP_TRA, COMP_ESP, COMP_PROF).")
    cognitive_level: str = Field(description="Nivel de la taxonomía de Bloom (ej: COG_REM, COG_UND, COG_APP, COG_ANA, COG_EVAL, COG_CREA).")

class ExamItemSchema(BaseModel):
    item_id: str = Field(description="El UUID del ítem proporcionado en el esqueleto.")
    content: ContentSchema
    grading_logic: GradingLogicSchema
    metadata: MetadataSchema

class ExamSectionSchema(BaseModel):
    items: List[ExamItemSchema]
    section_stimulus: Optional[str] = Field(default=None, description="Texto, caso clínico o lectura compartida para toda la sección (opcional).")