def generate_sciences_prompt(content_text: str, subject_name: str = "Asignatura Técnica") -> str:
    """
    ESTRATEGIA CIENCIAS (LOGIC_AND_TECH): Emulación de Exámenes UGR (Ingeniería y Matemáticas).
    Se adapta al formato real de la Universidad de Granada, distinguiendo entre Ciencias Básicas y Tecnología.
    """
    
    # Detección de contexto: ¿Es "Cacharreo" (Tech) o "Pizarra" (Math/Physics)?
    subject_lower = subject_name.lower()
    tech_keywords = ['programación', 'algoritmos', 'datos', 'software', 'computación', 'inteligencia', 'informática', 'sistemas', 'redes', 'servidores']
    is_computing = any(x in subject_lower for x in tech_keywords)
    
    if is_computing:
        # FORMATO UGR INGENIERÍA INFORMÁTICA (Mix Teoría Aplicada + Práctica)
        role_instruction = (
            "Actúa como Profesor del ETSIIT (Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación) de la UGR.\n"
            "Vas a generar un EXAMEN MIXTO (Teoría Aplicada + Práctica de Código)."
        )
        structure_instruction = (
            "*** ESTRUCTURA DEL EXAMEN (MODELO ETSIIT) ***\n\n"
            "PREGUNTA 1: ANÁLISIS Y TRAZA (Teoría Aplicada)\n"
            "- Objetivo: Presenta un fragmento de código breve o un algoritmo y pide al alumno que deduzca su salida exacta o su complejidad (Big O).\n"
            "- Formato: 'Deduce la salida del siguiente código...' o 'Analiza la complejidad de...'.\n\n"
            "PREGUNTA 2: CONCEPTOS DE INGENIERÍA\n"
            "- Objetivo: Pregunta corta sobre conceptos de diseño, patrones o estructuras de memoria.\n"
            "- Formato: 'Explica la diferencia entre...' o 'Justifica la elección de la estructura de datos para...'.\n\n"
            "PREGUNTA 3: IMPLEMENTACIÓN ALGORÍTMICA (Coding)\n"
            "- Objetivo: Resolución de un problema mediante código.\n"
            "- Formato: 'Implementa una función en Python/C++ que resuelva...'. Exige gestión de errores.\n\n"
            "PREGUNTA 4: DISEÑO DE SISTEMAS / MODIFICACIÓN\n"
            "- Objetivo: Plantea un escenario o un código base y pide una modificación funcional o un diseño de clases.\n"
            "- Formato: 'Diseña las clases necesarias para...' o 'Modifica el algoritmo anterior para soportar...'."
        )
        tool_instruction = "- **CÓDIGO OBLIGATORIO:** Las respuestas deben incluir bloques de código Markdown."
        
    else:
        # FORMATO UGR CIENCIAS (Matemáticas / Física / Ingeniería Civil)
        role_instruction = (
            "Actúa como Catedrático de la Facultad de Ciencias de la UGR.\n"
            "Vas a generar un EXAMEN CLÁSICO DE DESARROLLO (Teoría + Problemas)."
        )
        structure_instruction = (
            "*** ESTRUCTURA DEL EXAMEN (MODELO UGR CIENCIAS) ***\n\n"
            "PREGUNTA 1: DEFINICIONES FORMALES (Teoría)\n"
            "- Objetivo: Evaluar el rigor matemático/físico.\n"
            "- Formato: 'Define rigurosamente el concepto de [Concepto Clave]...' o 'Enuncia las condiciones de...'.\n\n"
            "PREGUNTA 2: TEOREMAS Y DEMOSTRACIONES (Teoría)\n"
            "- Objetivo: Evaluar la capacidad deductiva.\n"
            "- Formato: 'Enuncia y demuestra el Teorema de...' o 'Demuestra que si X entonces Y...'.\n\n"
            "PREGUNTA 3: PROBLEMA DE CÁLCULO/APLICACIÓN\n"
            "- Objetivo: Resolución práctica directa.\n"
            "- Formato: 'Calcula la integral...', 'Resuelve la ecuación diferencial...' o 'Determina la carga máxima...'.\n\n"
            "PREGUNTA 4: PROBLEMA COMPLEJO DE MODELADO\n"
            "- Objetivo: Aplicación de la teoría a un escenario no trivial.\n"
            "- Formato: Plantea un escenario físico o geométrico que requiera modelar matemáticamente la solución."
        )
        tool_instruction = "- **LATEX OBLIGATORIO:** Usa formato LaTeX para todas las expresiones matemáticas (\\( ... \\))."

    return f"""
{role_instruction}
ASIGNATURA: '{subject_name}'

FUENTE DE CONOCIMIENTO:
{content_text[:45000]}

{structure_instruction}

*** REGLAS DE FORMATO ***
{tool_instruction}
- Genera 4 preguntas de tipo 'open_ended'.
- El tono debe ser formal, académico y exigente, típico de la Universidad de Granada.

*** FORMATO DE SALIDA (JSON ESTRICTO) ***
{{
  "questions": [
    {{
      "question_text": "Enunciado P1...",
      "question_type": "open_ended",
      "model_answer": "Respuesta modelo..."
    }},
    {{
      "question_text": "Enunciado P2...",
      "question_type": "open_ended",
      "model_answer": "Respuesta modelo..."
    }},
    {{
      "question_text": "Enunciado P3...",
      "question_type": "open_ended",
      "model_answer": "Respuesta modelo..."
    }},
    {{
      "question_text": "Enunciado P4...",
      "question_type": "open_ended",
      "model_answer": "Respuesta modelo..."
    }}
  ]
}}
"""