def generate_classifier_prompt(subject_name: str, branch_name: str) -> str:
    """
    Clasificador de Arquetipos (8 Tipos).
    """
    return (
        f"Analiza la asignatura '{subject_name}' ({branch_name}).\n"
        "Clasifícala en uno de estos ARQUETIPOS:\n\n"
        "1. EXACT_SCIENCES\n2. LANGUAGES\n3. LEGAL\n4. ARTS\n5. SOCIETY\n6. HISTORY\n7. PHILOLOGY\n8. HUMANITIES_GENERIC\n\n"
        "Responde SOLO con la palabra clave."
    )
