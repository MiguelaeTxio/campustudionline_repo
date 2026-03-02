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

ACADEMIC_CLASSIFICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "archetype_id": {
            "type": "string",
            "enum": ["ARCH_LANG", "ARCH_HEALTH", "ARCH_TECH", "ARCH_SOC", "ARCH_HUM", "ARCH_SCI"],
            "description": "El arquetipo principal de la asignatura."
        },
        "sub_archetype_id": {
            "type": "string",
            "enum": [
                # LENGUAS
                "SUB-LIN-INSTR", "SUB-LIN-MINOR", "SUB-LIN-PHILO", "SUB-LIN-NORM", "SUB-LIN-TRA-TECH", "SUB-LIN-TRA-LIT",
                # SALUD
                "SUB-SAN-MED-CLIN", "SUB-SAN-MED-BASIC", "SUB-SAN-ODON", "SUB-SAN-FISIO", "SUB-SAN-CUID", 
                "SUB-SAN-LAB", "SUB-SAN-PSY-CLIN", "SUB-SAN-PSY-EXP", "SUB-SAN-VET", "SUB-SAN-NUT",
                # SOCIALES
                "SUB-SOC-LAW-PROC", "SUB-SOC-LAW-DICT", "SUB-SOC-ECON-QUAN", "SUB-SOC-ECON-MGMT", "SUB-SOC-EDU-KIDS", 
                "SUB-SOC-EDU-SEC", "SUB-SOC-COMM-JOUR", "SUB-SOC-COMM-AV", "SUB-SOC-GEOG", "SUB-SOC-WORK",
                # TÉCNICAS
                "SUB-TEC-SOFT", "SUB-TEC-CIVIL", "SUB-TEC-INDUS", "SUB-TEC-CHEM", "SUB-TEC-PROJ", "SUB-TEC-CONS", "SUB-TEC-PURE",
                # HUMANIDADES
                "SUB-HUM-HIST", "SUB-HUM-PHIL", "SUB-HUM-ART-HIST", "SUB-HUM-ART-CREA", "SUB-HUM-MUS", "SUB-HUM-ANTH",
                # CIENCIAS PURAS
                "SUB-SCI-BIO", "SUB-SCI-CHEM", "SUB-SCI-PHYS", "SUB-SCI-GEOL", "SUB-SCI-ENV", "SUB-SCI-DATA"
            ],
            "description": "El ID técnico de especialidad (Ref: V06DOC_SUBARCHETYPES)."
        },
        "target_language_code": {
            "type": "string",
            "description": "Código ISO 639-1 del idioma objetivo si es ARCH_LANG (ej: 'en', 'fr', 'ja'). 'es' para el resto."
        },
        "localized_sections": {
            "type": "object",
            "description": "Traducción de títulos e instrucciones al idioma objetivo (solo para ARCH_LANG).",
            "properties": {
                "SD_READ": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_LIST": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_WRIT": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_SPEAK": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_MEDI": {"type": "array", "items": {"type": "string"}, "description": "[Título, Instrucción]"},
                "SD_THEO": {"type": "array", "items": {"type": "string"}},
                "SD_CALC": {"type": "array", "items": {"type": "string"}}
            }
        }
    },
    "required": ["archetype_id", "sub_archetype_id", "target_language_code", "localized_sections"]
}

# [HITO 6] Esquema Universal de Ítem de Evaluación
# Resuelve incidencias 2 (widget_id prohibido), 3 (block_type prohibido), 
# 4 (feedback obligatorio), 5 (minItems 4), 6 (Enums etiquetas) y 7 (Parámetros).

EXAM_ITEM_CONTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "string", "description": "El UUID del ítem proporcionado en el esqueleto."},
                    "content": {
                        "type": "object",
                        "properties": {
                            "stem": {
                                "type": "string", 
                                "description": "El enunciado, pregunta o estímulo principal del ítem."
                            },
                            "options": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "text": {"type": "string"},
                                        "is_correct": {"type": "boolean"},
                                        "feedback": {"type": "string", "description": "Explicación específica para esta opción."}
                                    },
                                    "required": ["id", "text", "is_correct", "feedback"]
                                },
                                "minItems": 4, # [INCIDENCIA 5] Validación mínima de opciones
                                "description": "Lista de opciones de respuesta (Mínimo 4)."
                            },
                            # Soporte para otros widgets (Cloze, Matching, etc.)
                            "text_fragments": {"type": "array", "items": {"type": "string"}},
                            "gaps": {"type": "array", "items": {"type": "string"}},
                            "pairs_left": {"type": "array", "items": {"type": "string"}},
                            "pairs_right": {"type": "array", "items": {"type": "string"}},
                            "rubric": {"type": "string", "description": "Rúbrica de corrección (Solo para Open-Ended)."},
                            "sample_answer": {"type": "string", "description": "Respuesta modelo (Solo para Open-Ended)."}
                        },
                        "required": ["stem"] 
                    },
                    "grading_logic": {
                        "type": "object",
                        "properties": {
                            "feedback_justification": {
                                "type": "string",
                                "description": "[INCIDENCIA 4] Explicación pedagógica detallada de la solución correcta."
                            },
                            "correct_answer_id": {"type": "string"}
                        },
                        "required": ["feedback_justification"]
                    },
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "competency_tag": {
                                "type": "string",
                                "enum": ["COMP_SEMANTIC", "COMP_GRAMMAR", "COMP_PRAGMATIC", "COMP_CLINICAL", "COMP_LEGAL", "COMP_CALC", "COMP_CRITICAL"],
                                "description": "[INCIDENCIA 57] Etiqueta de competencia evaluada (Enum cerrado)."
                            },
                            "cognitive_level": {
                                "type": "string",
                                "enum": ["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE", "CREATE"],
                                "description": "[INCIDENCIA 57] Nivel de la taxonomía de Bloom (Enum cerrado)."
                            },
                            "difficulty_index": {
                                "type": "number",
                                "description": "Índice de dificultad estimado (0.0 a 1.0)."
                            },
                            # [INCIDENCIA 7] Parámetros Técnicos
                            "technical_density": {
                                "type": "string",
                                "enum": ["LOW", "MEDIUM", "HIGH"],
                                "description": "Densidad de conceptos técnicos en el ítem."
                            },
                            "linguistic_quality": {
                                "type": "string",
                                "enum": ["STANDARD", "ACADEMIC", "NATIVE_PROFESSIONAL"],
                                "description": "Registro lingüístico utilizado."
                            },
                            "bias_check": {
                                "type": "boolean",
                                "description": "Confirmación de que el ítem ha sido revisado contra sesgos."
                            }
                        },
                        "required": ["competency_tag", "cognitive_level", "difficulty_index", "technical_density", "linguistic_quality", "bias_check"]
                    }
                },
                "required": ["content", "grading_logic", "metadata"]
            }
        },
        # [INCIDENCIA 2 y 3] Bloqueo explícito: No pedimos widget_id ni block_type aquí.
        # [HITO 6] Soporte para estímulo de sección compartido (Reading/Case Study)
        "section_stimulus": {
            "type": "string",
            "description": "Texto, caso clínico o lectura compartida para toda la sección (opcional)."
        }
    },
    "required": ["items"]
}
