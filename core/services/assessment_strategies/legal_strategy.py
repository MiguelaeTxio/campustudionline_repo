"""
ESTRATEGIA DE EVALUACIÓN: SOCIO_LEGAL (MODELO UGR)
--------------------------------------------------
Emula el formato de examen de la Facultad de Derecho de la Universidad de Granada.
Estructura típica (Fuente: Guías Docentes UGR):
1. Test Teórico.
2. Desarrollo Teórico (Epígrafes del temario).
3. Supuesto Práctico (Hechos + Cuestiones + Fundamentación).
"""

def generate_legal_prompt(content_text: str, subject_name: str = "Derecho") -> str:
    # Definición del Rol UGR
    role_description = (
        "Actúa como un Magistrado y Catedrático de la Facultad de Derecho de la Universidad de Granada (UGR). "
        "Tu nivel de exigencia es máximo. Valoras el rigor terminológico, la capacidad de síntesis y, "
        "sobre todo, la FUNDAMENTACIÓN JURÍDICA (cita de leyes, artículos y sentencias)."
    )

    # Estructura del Examen UGR (Adaptada a 4 preguntas para el sistema)
    exam_structure = (
        "ESTRUCTURA OBLIGATORIA DEL EXAMEN (MODELO UGR - 4 CUESTIONES):\n"
        "1. [TEST] Conceptos Jurídicos (2 preguntas): Preguntas tipo test (multiple_choice) con 4 opciones. "
        "Deben versar sobre la naturaleza jurídica de las instituciones o definiciones legales estrictas.\n"
        "2. [TEORÍA] Desarrollo de Epígrafe (1 pregunta): Pregunta de desarrollo (open_ended) que solicite explicar "
        "un concepto teórico complejo (ej: 'Naturaleza y requisitos de X', 'Diferencias entre A y B'). "
        "NO es un ensayo de opinión, es una exposición técnica.\n"
        "3. [PRÁCTICA] Caso Práctico (1 pregunta): Pregunta de desarrollo (open_ended). \n"
        "   - DEBES inventar un 'Supuesto de Hecho' breve pero detallado.\n"
        "   - DEBES formular una cuestión jurídica sobre dicho supuesto.\n"
        "   - En la 'model_answer', ES OBLIGATORIO incluir la 'Fundamentación Jurídica' (Artículos aplicables)."
    )

    prompt = f"""
{role_description}

Estás diseñando un Examen Oficial para la asignatura: "{subject_name}".

FUENTE DE DERECHO (TEMARIO OFICIAL):
--------------------------------------------------
{content_text[:50000]}
--------------------------------------------------

{exam_structure}

REGLAS DE ORO PARA LA RESPUESTA MODELO (SOLUCIONARIO):
1. En las preguntas de DESARROLLO y PRÁCTICA, la respuesta debe ser técnica.
2. CITAS LEGALES: Siempre que sea posible, la respuesta debe indicar el artículo o ley que sustenta la solución (ej: "según el art. 1902 del CC...").
3. LENGUAJE: Usa terminología jurídica precisa (ej: 'demandante' no 'el que denuncia', 'inmueble' no 'casa').

FORMATO JSON DE SALIDA (ESTRICTO):
{{
  "questions": [
    {{
      "question_text": "Enunciado...",
      "question_type": "multiple_choice" | "open_ended",
      "options": ["a)...", "b)...", "c)...", "d)..."] (SOLO si es multiple_choice),
      "model_answer": "Respuesta modelo con fundamentación jurídica..."
    }}
  ]
}}
"""
    return prompt
