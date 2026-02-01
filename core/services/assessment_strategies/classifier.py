# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/core/services/assessment_strategies/classifier.py

def generate_classifier_prompt(subject_name: str, branch_name: str, rejected_archetypes: list = None) -> str:
    """
    [HITO 6] Clasificador Rector UGR (Texto Validado - Versión 4804ad0a).
    """
    exclusion_clause = ""
    if rejected_archetypes and len(rejected_archetypes) > 0:
        exclusion_list = ", ".join(rejected_archetypes)
        exclusion_clause = (
            f"\n\nREGLA DE HIERRO (EXCLUSIONES): NO puedes clasificar la asignatura bajo los siguientes arquetipos "
            f"porque ya han sido rechazados previamente: [{exclusion_list}]. "
            "Debes elegir la siguiente mejor opción lógica."
        )

    return (
        f"Actúa como Rector de la Universidad de Granada. Debes clasificar la asignatura '{subject_name}' "
        "en uno de los 5 Departamentos de Evaluación según su núcleo competitivo:\n\n"
        "1. LOGIC_AND_TECH: Pensamiento formal, cálculo, algoritmos y principios físicos/técnicos.\n"
        "2. CEFR_LANGUAGES: Entrenamiento para el uso práctico, oral y escrito de una lengua extranjera (Niveles A1-C2).\n"
        "3. SOCIO_LEGAL: Marcos regulatorios, derecho, leyes estatales y sistemas de justicia. (Derecho, Jurisprudencia).\n"
        "4. HEALTH_SCIENCES: Intervención clínica, protocolos de salud, patologías y seguridad del paciente.\n"
        "5. HUMANITIES_ARTS: Análisis dialéctico, crítica de fuentes, historia, arte y estudios lingüísticos/teóricos de la lengua (Filología).\n\n"
        "REGLA DE ORO DE LENGUAS (SISTEMA DE FILTRADO):\n" "   * CEFR_LANGUAGES: Aprendizaje instrumental. Busca palabras clave EXACTAS [\bword\b]: 'Idioma', 'Nivel', 'Inicial', 'Intermedio', 'Avanzado', 'Lengua Moderna', 'Minor', 'Maior', 'I, II, III, IV'.\n" "   * HUMANITIES_ARTS: Estudio académico/teórico. Busca palabras clave EXACTAS [\bword\b]: 'Historia', 'Literatura', 'Cultura', 'Cine', 'Filología', 'Pensamiento', 'Geografía', 'Norma y Uso'.\n" "   Ejemplo Crítico: 'Idioma Francés I' -> CEFR_LANGUAGES. 'El español actual: norma y uso' -> HUMANITIES_ARTS."
        f"{exclusion_clause}\n\n"
        "Responde ÚNICAMENTE con el nombre del Arquetipo (etiqueta en mayúsculas)."
    )
