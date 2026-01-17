def generate_languages_stimuli_prompt(content_text: str, subject_name: str) -> str:
    """
    Generador de Estímulos para IDIOMAS.
    """
    return f"""
Actúa como un Examinador de Cambridge/Trinity/EOI.
ASIGNATURA: {subject_name}
CONTEXTO:
{content_text[:10000]}

TAREA: Generar material original.
1. 'reading_stimulus': Texto de 300-400 palabras.
2. 'listening_transcript': Guion de diálogo/monólogo.

FORMATO JSON:
{{
  "reading_stimulus": "Texto...",
  "listening_transcript": "Texto..."
}}
"""

def generate_languages_exam_prompt(reading_text: str, listening_text: str) -> str:
    """
    Generador de Preguntas para IDIOMAS (4 Destrezas).
    """
    return f"""
Actúa como Tribunal de Examen de Idiomas.
TEXTO READING:
{reading_text[:3000]}
TRANSCRIPT LISTENING:
{listening_text[:3000]}

Genera un examen completo (Total 8 preguntas):
1. READING: 4 preguntas 'multiple_choice'.
2. LISTENING: 2 preguntas 'multiple_choice'.
3. WRITING: 1 tarea de redacción (open_ended).
4. SPEAKING: 1 tarea de monólogo (open_ended). AÑADE '[---RECORDING-REQUIRED---]'.

FORMATO JSON:
{{
  "questions": [
    {{
      "question_text": "...", 
      "question_type": "...",
      "options": [...],
      "model_answer": "..."
    }}
  ]
}}
"""
