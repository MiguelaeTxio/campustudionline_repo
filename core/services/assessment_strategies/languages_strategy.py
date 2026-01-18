def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    """
    Generador de Estímulos para IDIOMAS (Estrategia Segregada).
    Prompt endurecido + Modelo UGR (Listening = Diálogo).
    """
    return f"""
Actúa como un Examinador Pedagogo Senior experto en la enseñanza de lenguas extranjeras.

OBJETIVO: Generar material base para un examen de la asignatura: '{subject_name}'.

*** INSTRUCCIONES DE SEGURIDAD (CRÍTICAS) ***
1. **DETECCIÓN DE IDIOMA:** Identifica el idioma que se enseña en '{subject_name}' (ej: Francés, Inglés, Alemán).
2. **RESTRICCIÓN DE IDIOMA:** TODO el contenido generado (reading y listening) DEBE escribirse EXCLUSIVAMENTE en el idioma detectado.
   - ADVERTENCIA: El temario abajo está en ESPAÑOL, pero tú **TIENES PROHIBIDO** generar la respuesta en Español.

*** INSTRUCCIONES DE CREACIÓN DE MATERIAL ***
1. **TEMA DEL READING (CULTURA):** Elige un tema de CULTURA GENERAL o ACTUALIDAD (ej: Viajes, Tecnología, Historia) alejado de la gramática.
2. **FORMATO DEL LISTENING (DIÁLOGO):** El guion de audio ('listening_transcript') debe ser una **CONVERSACIÓN** o **ENTREVISTA** entre dos personas sobre un tema cotidiano o relacionado con el Reading, pero con un registro oral natural.
3. **APLICACIÓN GRAMATICAL:** Inyecta las estructuras gramaticales del temario (ej: Pasados, Futuros) en ambos textos de forma natural.
4. **NIVEL:** Adapta estrictamente el vocabulario al nivel (A1-C2) de la asignatura.

*** FORMATO DE SALIDA (JSON) ***
{{
  "reading_stimulus": "Texto del artículo o historia (300 palabras) en el IDIOMA EXTRANJERO...",
  "listening_transcript": "Guion de diálogo (Speaker A / Speaker B) en el IDIOMA EXTRANJERO..."
}}

-------------------------------------------------------------------------
CONTEXTO GRAMATICAL (SOLO REFERENCIA):
{content_text[:15000]}
-------------------------------------------------------------------------
"""

def generate_languages_exam_prompt(reading_text: str, listening_text: str) -> str:
    """
    Generador de Preguntas para IDIOMAS.
    Modelo UGR: Speaking = Entrevista Personal.
    """
    return f"""
Actúa como Tribunal de Examen Oficial de Idiomas.

MATERIAL DE EXAMEN (En el idioma extranjero):
TEXTO READING:
{reading_text[:4000]}

TRANSCRIPT LISTENING:
{listening_text[:4000]}

Genera un examen en 4 SECCIONES en el MISMO IDIOMA que los textos:

1. **SECCIÓN READING:** 4 preguntas 'multiple_choice' para comprobar la comprensión del Texto.
2. **SECCIÓN LISTENING:** 2 preguntas 'multiple_choice' sobre detalles específicos del DIÁLOGO (Transcript).
3. **SECCIÓN WRITING:** 1 tarea de redacción (open_ended) pidiendo una opinión sobre el tema del texto.
4. **SECCIÓN SPEAKING (ENTREVISTA PERSONAL):**
   - No pidas resumir el texto.
   - Genera una lista de **3 PREGUNTAS ABIERTAS** dirigidas al alumno.
   - Las preguntas deben ser sobre su vida, opiniones o situaciones hipotéticas (Trivial/Conversacional).
   - Deben obligar al alumno a usar la gramática implícita del nivel (ej: Si es nivel pasado, preguntar "¿Qué hiciste ayer?").
   - **IMPORTANTE:** Incluye el marcador [---RECORDING-REQUIRED---] al final.

FORMATO JSON ESTRICTO:
{{
  "questions": [
    {{
      "question_text": "Enunciado en el idioma extranjero...", 
      "question_type": "multiple_choice" o "open_ended",
      "options": ["a)...", "b)...", "c)...", "d)..."],
      "model_answer": "Respuesta modelo..."
    }}
  ]
}}
"""