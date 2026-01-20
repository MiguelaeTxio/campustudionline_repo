def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    """
    Generador de Estímulos para IDIOMAS.
    El texto base SIEMPRE es en el idioma objetivo.
    """
    return f"""
Actúa como un Examinador Oficial de Certificación de Idiomas (modelo CertAcles/UGR).
Tu misión es crear material de comprensión para la asignatura: '{subject_name}'.

*** PASO 1: ANÁLISIS DE NIVEL Y LENGUA ***
1. Identifica el idioma objetivo (ej: Chino, Alemán).
2. Identifica el nivel según el nombre de la asignatura (ej: 'Iniciación' = A1/A2, 'Intermedio' = B1/B2).

*** PASO 2: GENERACIÓN DE ESTÍMULOS (SIEMPRE EN IDIOMA OBJETIVO) ***
1. **READING:** Genera un texto de 350-450 palabras sobre cultura o actualidad del país de origen.
   - **OBLIGATORIO:** El texto debe estar ÍNTEGRAMENTE en el idioma objetivo.
2. **LISTENING TRANSCRIPT:** Guion de audio de 3-5 minutos (diálogo o monólogo).
   - **OBLIGATORIO:** Solo el texto hablado, ÍNTEGRAMENTE en el idioma objetivo.

*** FORMATO DE SALIDA (JSON ESTRICTO) ***
{{
  "detected_language": "Idioma detectado",
  "cefr_level": "A1, A2, B1, B2, C1 o C2",
  "reading_stimulus": "Texto en idioma objetivo",
  "listening_transcript": "Transcripción en idioma objetivo"
}}

-------------------------------------------------------------------------
CONTEXTO TÉCNICO:
{content_text[:15000]}
-------------------------------------------------------------------------
"""

def generate_languages_exam_prompt(reading_text: str, listening_transcript: str, cefr_level: str = "B1") -> str:
    """
    Generador de Examen Adaptativo. 
    Usa el nivel detectado para decidir el idioma de las instrucciones.
    """
    # Lógica de decisión de idioma de instrucciones (instrucción para el LLM)
    instruction_language_rule = (
        "Como el nivel detectado es A1 o A2 (Básico/Iniciación), usa el ESPAÑOL para los títulos de sección "
        "y los enunciados de las preguntas. Las opciones y respuestas modelo deben ir en el idioma del examen."
        if cefr_level in ["A1", "A2"] else
        "Como el nivel detectado es B1 o superior (Intermedio/Avanzado), utiliza EXCLUSIVAMENTE el "
        "idioma del examen para todo (títulos, enunciados, opciones y respuestas). Inmersión total."
    )

    return f"""
Actúa como un Tribunal de Examen de la UGR. 
Nivel de la evaluación: {cefr_level}.

MATERIAL DE REFERENCIA (EN IDIOMA OBJETIVO):
- READING: {reading_text[:4000]}
- LISTENING: {listening_transcript[:4000]}

*** REGLA DE IDIOMA PARA EL EXAMEN ***
{instruction_language_rule}

*** ESTRUCTURA DEL EXAMEN (4 Destrezas) ***
1. COMPRENSIÓN LECTORA: 2 preguntas multiple_choice.
2. COMPRENSIÓN AUDITIVA: 2 preguntas multiple_choice con etiqueta [---AUDIO-REQUIRED---].
3. EXPRESIÓN ESCRITA: 1 redacción (100-150 palabras).
4. EXPRESIÓN ORAL: 1 monólogo/entrevista con etiqueta [---RECORDING-REQUIRED---].

*** FORMATO DE SALIDA (JSON ESTRICTO) ***
{{
  "questions": [
    {{
      "question_text": "Título\\n\\nEnunciado (en el idioma decidido por la regla)...",
      "question_type": "multiple_choice" | "open_ended",
      "options": ["Opción A", "Opción B", ...],
      "model_answer": "Respuesta correcta (SIEMPRE en el idioma objetivo)"
    }}
  ]
}}
"""
