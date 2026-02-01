### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md
2.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE DE AUDITORÍA Y RE-ALINEACIÓN UGR)

## 1. RESUMEN TÉCNICO ACUMULADO (SESIÓN ACTUAL)
- **Diagnóstico Forense:** Se auditó la evaluación #319 ("Chino Intermedio 1") y se confirmó que la BBDD del proyecto es rica en datos académicos (`learning_objectives`, `course_content_outline`). El fallo de calidad no se debe a la falta de datos, sino a que la estrategia de generación (`languages_strategy.py`) es "ciega" y no los utiliza, aplicando un nivel "Beginner" hardcodeado.
- **Distinción Metodológica Crítica:** Se estableció que el objetivo no es emular un examen de "Acreditación" (CertAcles), sino la metodología de evaluación de un "Grado Académico" de la UGR (Lenguas Modernas y sus Literaturas), que se basa en la gramática, el vocabulario y la sintaxis del temario.
- **Estabilización de UX:** Se implementó un modal de advertencia en la Sala de Estudio para informar a los usuarios de las inconsistencias durante el proceso de mejora.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 0: RE-ALINEACIÓN DOCUMENTAL (OBLIGATORIO)
- **Tarea:** Ejecutar un `PMA` sobre `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`.
- **Objetivo:** Reflejar la distinción entre "Acreditación (CertAcles)" y "Grado Académico (UGR)". Definir que nuestro emulador sigue el modelo de Grado, con sus bloques de Vocabulario, Gramática y Sintaxis Aplicada, y añadir el requerimiento de una capa de "Familia de Grafías" (Latina, Logográfica, Cirílica, RTL) para activar reglas específicas de evaluación (ej: caligrafía).

### PASO 1: AUDITORÍA FORENSE DEL FLUJO DE DATOS
- **Tarea:** Iniciar la sesión con un `PVR` para solicitar los tres archivos que gobiernan el flujo completo del selector de temario.
- **Archivos a solicitar:**
    1. `assessment/views.py`: Para auditar cómo se procesa la selección del usuario.
    2. `assessment/templates/assessment/configure_assessment.html`: Para ver cómo se presenta el `course_content_outline` al usuario.
    3. `orchestrator/tasks.py`: Para trazar cómo el `selection_range` viaja desde el modelo `Assessment` hasta la llamada a la estrategia.

### PASO 2: REFACTORIZACIÓN DE LA ESTRATEGIA DE IDIOMAS
- **Tarea:** Una vez completada la auditoría, ejecutar un `PMA` sobre `core/services/assessment_strategies/languages_strategy.py`.
- **Objetivos de la Refactorización:**
    1. **Conexión de Datos:** Modificar la firma de `get_strategy_skeleton` y `generate_languages_item_prompt` para que acepten el objeto `Subject` completo y el `selection_range`.
    2. **Inyección de Contexto:** El prompt dejará de ser "Beginner" y se construirá dinámicamente usando los `learning_objectives` y el `course_content_outline` filtrado por `selection_range`.
    3. **Calibración de Nivel:** La IA recibirá el temario exacto que el usuario seleccionó, garantizando que el nivel de la pregunta es el correcto.
    4. **Localización del `section_label`:** Corregir el esquema JSON para que la IA devuelva la cabera traducida.
