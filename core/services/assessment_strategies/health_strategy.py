def generate_health_prompt(content_text: str, subject_name: str = "Ciencias de la Salud") -> str:
    """
    ESTRATEGIA CIENCIAS DE LA SALUD (HEALTH_SCIENCES): Modelo UGR (Enfermería/Medicina/Psicología).
    Adapta el formato ECOE (Evaluación Clínica Objetiva Estructurada) a texto.
    """
    
    role_description = (
        "Actúa como un Profesor de la Facultad de Ciencias de la Salud de la UGR evaluando una ECOE (Evaluación Clínica Objetiva Estructurada). "
        "Tu prioridad es el RAZONAMIENTO CLÍNICO y la SEGURIDAD DEL PACIENTE. "
        "Valoras la capacidad de integrar síntomas (Anamnesis) con datos objetivos (Constantes/Pruebas) para emitir un juicio."
    )

    structure_instruction = (
        "*** ESTRUCTURA DEL EXAMEN (MODELO ECOE/CASOS) ***\n\n"
        "PREGUNTA 1: FUNDAMENTOS TEÓRICOS (Test)\n"
        "- Tipo: multiple_choice\n"
        "- Objetivo: Evaluar fisiopatología, farmacología o anatomía base.\n\n"
        "PREGUNTA 2: PROCEDIMIENTOS Y TÉCNICAS (Test)\n"
        "- Tipo: multiple_choice\n"
        "- Objetivo: Evaluar la ejecución de protocolos (ej: RCP, Sondaje, Vía Aérea) o valores normales.\n\n"
        "PREGUNTA 3: SIMULACIÓN CLÍNICA - JUICIO DIAGNÓSTICO (Desarrollo)\n"
        "- Tipo: open_ended\n"
        "- Contexto: Presenta un 'Caso Clínico Breve' (Paciente X, edad, motivo consulta, constantes vitales).\n"
        "- Tarea: Solicita el Juicio Clínico, Diagnóstico Diferencial o Diagnósticos Enfermeros (NANDA) prioritarios.\n\n"
        "PREGUNTA 4: SIMULACIÓN CLÍNICA - PLAN DE ACTUACIÓN (Desarrollo)\n"
        "- Tipo: open_ended\n"
        "- Contexto: Basado en el caso anterior o una situación de urgencia.\n"
        "- Tarea: Describe el Plan Terapéutico, Intervenciones (NIC) o algoritmo de actuación (ABCDE) paso a paso."
    )

    return f"""
{role_description}

ASIGNATURA: "{subject_name}"

FUENTE DE CONOCIMIENTO (EVIDENCIA CLÍNICA):
--------------------------------------------------
{content_text[:50000]}
--------------------------------------------------

{structure_instruction}

REGLAS DE ORO PARA LA RESPUESTA MODELO:
1. **TERMINOLOGÍA:** Uso estricto de lenguaje médico/sanitario.
2. **SEGURIDAD:** Penaliza acciones que pongan en riesgo al paciente (ej: no comprobar alergias).
3. **EVIDENCIA:** Basa las intervenciones en guías clínicas actuales.

FORMATO JSON DE SALIDA (ESTRICTO):
{{
  "questions": [
    {{
      "question_text": "Enunciado P1...",
      "question_type": "multiple_choice",
      "options": ["a)...", "b)...", "c)...", "d)..."],
      "model_answer": "Respuesta fundamentada..."
    }},
    {{
      "question_text": "Enunciado P2...",
      "question_type": "multiple_choice",
      "options": ["a)...", "b)...", "c)...", "d)..."],
      "model_answer": "Respuesta fundamentada..."
    }},
    {{
      "question_text": "CASO CLÍNICO: [Descripción del Paciente y Constantes]\\n\\nPregunta: ¿Cuál es el juicio clínico...",
      "question_type": "open_ended",
      "model_answer": "Análisis del caso y diagnóstico..."
    }},
    {{
      "question_text": "PLAN DE ACTUACIÓN: Ante la situación anterior... (o nueva situación urgente)",
      "question_type": "open_ended",
      "model_answer": "1. Valoración... 2. Intervención... 3. Evaluación..."
    }}
  ]
}}
"""
