"""
ESTRATEGIA DE EVALUACIÓN: HUMANITIES_ARTS (MODELO UGR)
------------------------------------------------------
Emula el formato de examen de las Facultades de Filosofía y Letras, e Historia de la UGR.
El núcleo de la evaluación es el COMENTARIO (de texto, de imagen o histórico) y el desarrollo ensayístico.
"""

def generate_humanities_prompt(content_text: str, subject_name: str, subject_type: str = "HUMANITIES_GENERIC") -> str:
    # 1. Configuración del Rol y Foco según el subtipo
    role = "Catedrático de Humanidades"
    practical_focus = "Comentario de Texto Académico"
    
    if subject_type == "ARTS":
        role = "Catedrático de Historia del Arte"
        practical_focus = "Comentario de Lámina/Obra de Arte (Análisis Formal, Iconográfico y Contextual)"
    elif subject_type == "HISTORY":
        role = "Catedrático de Historia"
        practical_focus = "Comentario de Texto Histórico, Mapa o Gráfico"
    elif subject_type == "SOCIETY": # Filosofía/Sociología
        role = "Profesor de Filosofía y Pensamiento"
        practical_focus = "Comentario de Texto Filosófico (Tesis, Argumentación y Vigencia)"
    elif subject_type == "PHILOLOGY":
        role = "Filólogo y Lingüista"
        practical_focus = "Comentario Filológico y Literario"

    role_description = (
        f"Actúa como un {role} de la Universidad de Granada (UGR). "
        "Tu nivel de exigencia es alto. Valoras la capacidad de síntesis, la riqueza de vocabulario, "
        "la estructuración lógica de las ideas y la capacidad de relacionar conceptos (pensamiento crítico)."
    )

    # Estructura del Examen UGR (Humanidades)
    exam_structure = (
        f"ESTRUCTURA OBLIGATORIA DEL EXAMEN (MODELO UGR - {subject_type}):\n"
        "1. [CONCEPTOS] Definiciones Precisas (2 preguntas): Preguntas tipo test (multiple_choice) con 4 opciones. "
        "Evalúan la precisión terminológica (ej: definir 'Renacimiento', 'Plusvalía', 'Metáfora').\n"
        "2. [ENSAYO] Desarrollo Temático (1 pregunta): Pregunta de desarrollo (open_ended). "
        "Solicita exponer un tema teórico con profundidad, contexto y autores relevantes.\n"
        f"3. [PRÁCTICA] {practical_focus} (1 pregunta): Pregunta de desarrollo (open_ended).\n"
        "   - DEBES seleccionar o inventar un BREVE fragmento de texto, descripción de una obra o escenario histórico relacionado con el temario.\n"
        "   - Pide al alumno que realice un análisis siguiendo la metodología académica (Contexto, Análisis, Conclusión).\n"
        "   - La 'model_answer' debe ser un ejemplo de comentario académico perfecto."
    )

    prompt = f"""
{role_description}

Estás diseñando un Examen Oficial para la asignatura: "{subject_name}".

FUENTE DE CONOCIMIENTO:
--------------------------------------------------
{content_text[:50000]}
--------------------------------------------------

{exam_structure}

REGLAS DE ORO PARA LA RESPUESTA MODELO:
1. EXPRESIÓN: La redacción debe ser culta, fluida y académicamente rigurosa (Estilo UGR).
2. ESTRUCTURA: Obligatorio usar estructura de ensayo académico: Introducción (Hipótesis), Desarrollo (Argumentación) y Conclusión (Síntesis).
3. RIGOR: Es MANDATORIO citar autores, obras, fechas clave o corrientes historiográficas/filosóficas específicas en la respuesta modelo.

FORMATO JSON DE SALIDA (ESTRICTO):
{{
  "questions": [
    {{
      "question_text": "Enunciado...",
      "question_type": "multiple_choice" | "open_ended",
      "options": ["a)...", "b)...", "c)...", "d)..."] (SOLO si es multiple_choice),
      "model_answer": "Respuesta modelo..."
    }}
  ]
}}
"""
    return prompt
