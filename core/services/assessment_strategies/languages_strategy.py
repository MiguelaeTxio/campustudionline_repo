def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    """
    Generador de Estímulos para IDIOMAS.
    Crea el texto base (Reading) y el guion de diálogo (Listening).
    """
    return f"""
Actúa como un Examinador Oficial de Certificación de Idiomas (modelo CertAcles/UGR).

OBJETIVO: Generar material base para un examen de la asignatura: '{subject_name}'.

*** PASO 1: DETECCIÓN DE IDIOMA ***
Identifica el idioma objetivo de la asignatura (ej: Francés, Inglés, Alemán).
Todo el contenido generado debe ser en ese idioma estricto.

*** PASO 2: GENERACIÓN DE MATERIAL ***
1. **READING (Texto Cultural):** Genera un texto de 350-450 palabras sobre un tema de actualidad o cultura del país del idioma.
   - Nivel: Acorde a la asignatura (A1-C2).
   
2. **LISTENING TRANSCRIPT (Solo Texto Hablado):**
   - Genera un guion para un audio de 3 a 5 minutos.
   - Formato: Diálogo natural o Monólogo.
   - **IMPORTANTE:** Escribe SOLO el texto que debe ser leído por el locutor/TTS. 
   - **PROHIBIDO:** No incluyas nombres de personajes ("Juan:", "Maria:"), ni acotaciones ("(Risas)", "(Entra música)"), ni instrucciones en inglés. SOLO EL TEXTO HABLADO SEGUIDO.

*** FORMATO DE SALIDA (JSON PURO) ***
{{
  "detected_language": "Idioma detectado...",
  "reading_stimulus": "Texto completo del reading...",
  "listening_transcript": "Texto plano y limpio para ser locutado..."
}}

-------------------------------------------------------------------------
CONTEXTO (SOLO PARA NIVEL Y VOCABULARIO):
{content_text[:15000]}
-------------------------------------------------------------------------
"""

def generate_languages_exam_prompt(reading_text: str, listening_transcript: str) -> str:
    """
    Generador del Examen Completo de Idiomas.
    Estrictamente en el idioma objetivo.
    """
    return f"""
Actúa como un Tribunal de Examen de Idiomas (Modelo UGR/CertAcles).

MATERIAL DE EXAMEN (READING):
{reading_text[:4000]}

MATERIAL DE EXAMEN (LISTENING - TRANSCRIPCIÓN OCULTA):
{listening_transcript[:4000]}

*** INSTRUCCIONES CRÍTICAS DE FORMATO ***
1. **IDIOMA:** Todo el examen (enunciados, opciones, títulos) debe estar en el IDIOMA DEL TEXTO (ej: si es Francés, usa "Compréhension Écrite", no "Reading").
2. **NO USAR INGLÉS NI ESPAÑOL:** Bajo ninguna circunstancia.

*** ESTRUCTURA DEL EXAMEN (4 Destrezas) ***

SECCIÓN 1: COMPRENSIÓN LECTORA (Reading)
- Título: [Nombre de la destreza en el idioma, ej: Leseverstehen]
- Contenido: 2 preguntas tipo test sobre el texto.

SECCIÓN 2: COMPRENSIÓN AUDITIVA (Listening)
- Título: [Nombre de la destreza en el idioma, ej: Hörverstehen]
- Contenido: 2 preguntas sobre el audio.
- **FORMATO VISUAL:** Cada pregunta debe llevar un botón de play. Para ello, inicia el enunciado con la etiqueta **[---AUDIO-REQUIRED---]**.
- Ejemplo: "[---AUDIO-REQUIRED---] Quelle est la profession de...?"

SECCIÓN 3: EXPRESIÓN ESCRITA (Writing)
- Título: [Nombre de la destreza en el idioma]
- Contenido: 1 redacción corta (100-150 palabras).

SECCIÓN 4: EXPRESIÓN ORAL (Speaking)
- Título: [Nombre de la destreza en el idioma]
- Contenido: 1 pregunta de entrevista o monólogo.
- **FORMATO VISUAL:** Inicia el enunciado con la etiqueta **[---RECORDING-REQUIRED---]**.
- La duración de la grabación será gestionada por la plataforma (Automático + 15s), no lo menciones en el texto.

*** FORMATO DE SALIDA (JSON) ***
{{
  "questions": [
    {{
      "question_text": "Título Sección 1 (en idioma)\\n\\nEnunciado pregunta...",
      "question_type": "multiple_choice",
      "options": ["Opción A", "Opción B", ...],
      "model_answer": "Respuesta correcta..."
    }},
    {{
      "question_text": "Título Sección 2 (en idioma)\\n\\n[---AUDIO-REQUIRED---] Enunciado...",
      "question_type": "multiple_choice",
      "options": ["Opción A", ...],
      "model_answer": "..."
    }},
    {{
      "question_text": "Título Sección 4 (en idioma)\\n\\n[---RECORDING-REQUIRED---] Enunciado de la entrevista...",
      "question_type": "open_ended",
      "model_answer": "Criterios de evaluación..."
    }}
  ]
}}
"""
