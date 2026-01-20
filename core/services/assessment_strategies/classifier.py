def generate_classifier_prompt(subject_name: str, branch_name: str) -> str:
    """
    [HITO 6] Clasificador Rector UGR (Texto Validado).
    """
    return (
        f"Actúa como Rector de la Universidad de Granada. Debes clasificar la asignatura '{subject_name}' "
        "en uno de los 5 Departamentos de Evaluación según su núcleo competitivo:\n\n"
        "1. LOGIC_AND_TECH: Pensamiento formal, cálculo, algoritmos y principios físicos/técnicos.\n"
        "2. CEFR_LANGUAGES: Entrenamiento para el uso práctico, oral y escrito de una lengua extranjera (Niveles A1-C2).\n"
        "3. SOCIO_LEGAL: Marcos regulatorios, derecho, leyes estatales y sistemas de justicia. (Derecho, Jurisprudencia).\n"
        "4. HEALTH_SCIENCES: Intervención clínica, protocolos de salud, patologías y seguridad del paciente.\n"
        "5. HUMANITIES_ARTS: Análisis dialéctico, crítica de fuentes, historia, arte y estudios lingüísticos/teóricos de la lengua (Filología).\n\n"
        "Regla de Oro: El estudio teórico/histórico de la lengua va a HUMANITIES_ARTS. El entrenamiento para hablar/escribir una lengua va a CEFR_LANGUAGES. El derecho y la justicia van a SOCIO_LEGAL.\n\n"
        "Responde ÚNICAMENTE con el nombre del Arquetipo (etiqueta en mayúsculas)."
    )
