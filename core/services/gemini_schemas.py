# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/gemini_schemas.py
# [V4 - CLEANUP HITO 6] Eliminación de esquemas de evaluación obsoletos. Preservación de esquemas de automatización.

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

ACADEMIC_CLASSIFICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "archetype_id": {
            "type": "string",
            "enum": ["ARCH_LANG", "ARCH_HEALTH", "ARCH_TECH", "ARCH_SOC", "ARCH_HUM"],
            "description": "El arquetipo principal de la asignatura."
        },
        "sub_archetype_id": {
            "type": "string",
            "enum": [
                "SUB-LIN-CERT", "SUB-LIN-PROF", "SUB-LIN-LIT",
                "SUB-SAN-MED", "SUB-SAN-CUID", "SUB-SAN-BIO", "SUB-SAN-PSY", "SUB-SAN-VET",
                "SUB-TEC-SOFT", "SUB-TEC-CIVIL", "SUB-TEC-INDUS", "SUB-TEC-PURE", "SUB-TEC-CHEM",
                "SUB-SOC-JUR", "SUB-SOC-ECON", "SUB-SOC-BEHAV", "SUB-SOC-COMM",
                "SUB-HUM-HIST", "SUB-HUM-PHIL", "SUB-HUM-EDU", "SUB-ART-CREA", "SUB-ART-MUS"
            ],
            "description": "El ID técnico de especialidad (Ref: V06DOC_SUBARCHETYPES)."
        },
        "target_language_code": {
            "type": "string",
            "description": "Código ISO 639-1 del idioma objetivo si es ARCH_LANG (ej: 'en', 'fr', 'de'). 'es' para el resto."
        },
        "localized_sections": {
            "type": "object",
            "description": "Traducción de títulos e instrucciones al idioma objetivo (solo para ARCH_LANG).",
            "properties": {
                "SD_READ": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_LIST": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_WRIT": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_SPEAK": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_MEDI": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"}
            }
        },

    },
    "required": ["archetype_id", "sub_archetype_id", "target_language_code", "localized_sections"]
}
