# ESPECIFICACIÓN TÉCNICA DEL SISTEMA DE EVALUACIONES (ESTÁNDAR UGR)
# Versión: 3.0 (Consolidación Total - Realidad UGR/CLM/ETSIIT)

## 1. ARQUITECTURA NUCLEAR: BLOQUES COMPETENCIALES
El sistema debe operar bajo una arquitectura de Bloques de Alta Densidad, prohibiendo el modelo atómico 1:1.

*   **Relación 1:N (Estímulo-Batería):** Un único `reading_stimulus` o `listening_stimulus` debe servir como base para una batería de múltiples `Question Objects` (mínimo 5-8 ítems).
*   **Aislamiento de Bloques:** Las preguntas deben agruparse por competencia (Reading, Listening, etc.) a nivel de base de datos y de renderizado.

## 2. DUALIDAD DE MODALIDADES DE EXAMEN
El sistema debe ser capaz de generar dos tipos de evaluación distintos:

*   **Modalidad "Acreditación (Simulacro)":** Emula un examen oficial del CLM (CertAcles). Activa esqueletos de alta carga (30-40 ítems), reglas de inmersión total y puntuación por bloques.
*   **Modalidad "Prueba de Nivel (Ejercicio)":** Evalúa el progreso de un curso. Activa esqueletos de menor carga (10-15 ítems) enfocados en el syllabus.

## 3. REGLAS TRANSVERSALES DE CUMPLIMIENTO OBLIGATORIO

*   **Regla de Inmersión Lingüística (CLM):** Para exámenes de idiomas, todo el contenido visible por el usuario (instrucciones, enunciados, opciones, etiquetas de sección) DEBE estar en el idioma objeto.
*   **Regla de Rigor (ETSIIT):** Para arquetipos de ciencias e ingeniería, el sistema DEBE soportar y renderizar correctamente formulación LaTeX/MathJax.
*   **Estándar Cassette UGR:** El reproductor de audio debe tener botones físicos PLAY/STOP. La grabadora debe incluir REC/STOP/PLAY/SAVE. El STOP reinicia el audio a 0.

## 4. FLUJO DE PROGRAMACIÓN Y LÓGICA DE CONTROL

*   **Strategy Factory Pattern:** La tarea `generate_assessment_from_content_task` no debe llamar a estrategias hardcodeadas. Debe usar un despachador ("Factory") que, basado en el `assessment.archetype`, importe y ejecute la estrategia correcta (`languages_strategy`, `legal_strategy`, etc.).
*   **Clasificación Previa:** Antes de llamar a la estrategia, se debe determinar si una lengua es "Maior" o "Minor" y guardar este estado para que la Factory pueda despachar al sub-esqueleto correcto.
*   **Self-Healing (Auto-Reparación):** El motor de tareas DEBE incluir una capa de saneamiento que fuerce el formato Cloze (`[...]`) si la IA falla en generarlo, y que limpie prefijos ("a)", "1.") de las opciones de respuesta.
