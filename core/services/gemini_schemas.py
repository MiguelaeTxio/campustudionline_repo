# /home/MiguelAeTxio/CampuStudiOnline/core/services/gemini_schemas.py
# [V3 - METADATA_SCHEMA FIX] Se corrige la estructura de METADATA_SCHEMA para que sea una FunctionDeclaration válida, resolviendo el error crítico en la inicialización de tareas.

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


# --- Schemas for Assessment ---

ASSESSMENT_QUESTIONS_SCHEMA = {
    "name": "generate_assessment_questions",
    "description": "Genera una lista de preguntas y respuestas modelo basadas en un texto.",
    "parameters": {
        "type": "object",
        "properties": {
            "preguntas": {
                "type": "array",
                "description": "La lista de preguntas de autoevaluación generadas.",
                "items": {
                    "type": "object",
                    "properties": {
                        "pregunta": {
                            "type": "string",
                            "description": "El texto de la pregunta.",
                        },
                        "respuesta_modelo": {
                            "type": "string",
                            "description": "Una respuesta detallada y bien explicada que sirva como modelo.",
                        },
                    },
                    "required": ["pregunta", "respuesta_modelo"],
                },
            }
        },
        "required": ["preguntas"],
    },
}

ASSESSMENT_CORRECTION_SCHEMA = {
    "name": "correct_user_answer",
    "description": "Evalúa la respuesta de un usuario y proporciona puntuación y feedback.",
    "parameters": {
        "type": "object",
        "properties": {
            "puntuacion": {
                "type": "integer",
                "description": "Un entero de 0 a 100 que representa la calidad de la respuesta del usuario.",
            },
            "feedback": {
                "type": "string",
                "description": "Una explicación constructiva y detallada sobre la respuesta, destacando aciertos y áreas de mejora.",
            },
        },
        "required": ["puntuacion", "feedback"],
    },
}
