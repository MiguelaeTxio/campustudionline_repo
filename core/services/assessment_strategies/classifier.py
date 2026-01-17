def generate_classifier_prompt(subject_name: str, branch_name: str) -> str:
    """
    Clasificador de Arquetipos (Rol Rector).
    """
    return (
        f"ACTÚA COMO: El Rector de la Universidad. Tienes la autoridad absoluta para definir la naturaleza de la evaluación.\n"
        f"OBJETIVO: Asigna la asignatura '{subject_name}' ({branch_name}) a uno de los tres Departamentos de Evaluación.\n\n"
        "DEPARTAMENTOS DISPONIBLES:\n"
        "1. LANGUAGES (Dpto. de Lenguas Extranjeras): EXCLUSIVO para el aprendizaje instrumental de idiomas NO NATIVOS (Inglés, Chino, Italiano, etc.). Si el objetivo es aprender a hablar/escuchar, va aquí.\n"
        "2. SCIENCES (Dpto. de Ciencias Exactas): Matemáticas, Física, Ingeniería. Cálculo y lógica.\n"
        "3. HUMANITIES (Dpto. de Humanidades y Teoría): Todo lo teórico. Historia, Arte, Derecho y FILOLOGÍA (Estudio de la lengua materna/español).\n\n"
        "ORDEN RECTORAL: Asignaturas como 'Italiano', 'Chino', 'Alemán' pertenecen al Dpto. LANGUAGES. Asignaturas de 'Español' o 'Literatura' pertenecen al Dpto. HUMANITIES.\n"
        "Responde ÚNICAMENTE con el nombre del departamento: LANGUAGES, SCIENCES o HUMANITIES."
    )