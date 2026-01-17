def generate_humanities_prompt(content_text: str, tribunal_type: str = "HUMANITIES_GENERIC") -> str:
    """
    ESTRATEGIA HUMANIDADES: Evaluación de Conocimientos Conceptuales.
    FUENTE: El contenido se usa como 'Syllabus' (Temario).
    """
    tribunals = {
        "LEGAL": {
            "role": "Magistrado del Tribunal Supremo",
            "tone": "Jurídico, técnico y normativo.",
            "task": "Evaluar el dominio de la legislación y la capacidad de aplicación jurídica."
        },
        "ARTS": {
            "role": "Catedrático de Historia del Arte",
            "tone": "Analítico, estilístico e iconográfico.",
            "task": "Evaluar el conocimiento de movimientos, estilos y análisis formal."
        },
        "SOCIETY": {
            "role": "Doctor en Sociología y Ciencias Políticas",
            "tone": "Crítico, dialéctico y estructural.",
            "task": "Evaluar la comprensión de corrientes de pensamiento y estructuras sociales."
        },
        "HISTORY": {
            "role": "Académico de la Historia",
            "tone": "Cronológico, causal y geopolítico.",
            "task": "Evaluar el conocimiento de hechos históricos, causas y consecuencias."
        },
        "PHILOLOGY": {
            "role": "Catedrático de Filología Hispánica",
            "tone": "Lingüístico, literario y gramatical.",
            "task": "Evaluar conocimientos sobre gramática normativa, historia de la lengua o teoría literaria."
        },
        "HUMANITIES_GENERIC": {
            "role": "Profesor Titular de Universidad",
            "tone": "Académico y riguroso.",
            "task": "Evaluar el dominio conceptual de la materia."
        }
    }
    config = tribunals.get(tribunal_type, tribunals["HUMANITIES_GENERIC"])

    return f"""
Actúa como un {config['role']}.
Tu tono debe ser {config['tone']}
Tu objetivo es: {config['task']}

ESTÁS DISEÑANDO UN EXAMEN OFICIAL DE CONOCIMIENTOS.
TEMARIO DE LA ASIGNATURA:
--------------------------------------------------
{content_text[:45000]}
--------------------------------------------------

REGLAS ABSOLUTAS (PROHIBICIONES):
1. PROHIBIDO hacer preguntas de "Comprensión Lectora".
2. PROHIBIDO usar frases como: "Según el texto", "En el fragmento".
3. Las preguntas deben ser sobre la MATERIA, no sobre el DOCUMENTO.

ESTRUCTURA DEL EXAMEN (4 PREGUNTAS):
1. [TEST] Conceptos: 2 preguntas tipo test (4 opciones).
2. [PRÁCTICO] Caso/Análisis: 1 pregunta de desarrollo (open_ended).
3. [ENSAYO] Desarrollo: 1 pregunta de desarrollo (open_ended).

FORMATO JSON DE SALIDA:
{{
  "questions": [
    {{
      "question_text": "Enunciado...",
      "question_type": "multiple_choice" o "open_ended",
      "options": ["a) ...", "b) ...", "c) ...", "d) ..."],
      "model_answer": "Respuesta..."
    }}
  ]
}}
"""
