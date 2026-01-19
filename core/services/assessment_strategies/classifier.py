def generate_classifier_prompt(subject_name: str, branch_name: str) -> str:
    """
    Clasificador de Arquetipos (Rol Rector UGR).
    Determina a qué Departamento de Evaluación pertenece la asignatura.
    """
    return f"""
ACTÚA COMO: El Rector de la Universidad de Granada (UGR), experto en taxonomía académica.
OBJETIVO: Clasificar la asignatura '{subject_name}' (Rama: {branch_name}) según las competencias UGR.

*** INSTRUCCIONES DE CLASIFICACIÓN (DEPARTAMENTOS) ***

1. **LOGIC_AND_TECH**: Asignaturas de Ingeniería, Matemáticas, Física o Informática. 
   - Foco: Lógica, algoritmos, cálculo y resolución de problemas técnicos.
   - Ejemplo: Algorítmica, Criptografía, Cálculo, Electrónica.

2. **CEFR_LANGUAGES**: Aprendizaje instrumental de idiomas (Centro de Lenguas Modernas).
   - Foco: Las 4 destrezas (Listening, Speaking, Reading, Writing).
   - Ejemplo: Francés Inicial, Inglés Técnico, Chino.

3. **SOCIO_LEGAL**: Derecho, Economía, Políticas y Gestión.
   - Foco: Aplicación de normas a casos prácticos y análisis socio-económico.
   - Ejemplo: Derecho Informático, Creación de Empresas, Macroeconomía.

4. **HEALTH_SCIENCES**: Medicina, Enfermería y Biociencias.
   - Foco: Razonamiento clínico, anatomía y protocolos de salud.
   - Ejemplo: Anatomía, Bioquímica Clínica, Enfermería Comunitaria.

5. **HUMANITIES_ARTS**: Historia, Arte, Filosofía y Diseño.
   - Foco: Análisis crítico de fuentes, estética y dialéctica histórica.
   - Ejemplo: Historia de España, Animación (como arte), Ética.

*** FORMATO DE SALIDA (JSON ESTRICTO) ***
Responde ÚNICAMENTE con este JSON:
{{"classification": "NOMBRE_DEL_DEPARTAMENTO"}}
"""
