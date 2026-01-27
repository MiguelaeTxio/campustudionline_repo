# REGISTRO DE ARQUETIPOS DE EVALUACIÓN (UGR)
# Versión 3.0 - Especificación Granular por Centro/Facultad

## I. ARQUETIPO: CEFR_LANGUAGES (Centro de Lenguas Modernas)
Este arquetipo se divide en dos itinerarios con esqueletos y lógicas distintas.

### A. ITINERARIO "MAIOR" (Especialidad Filológica / Acreditación B1-C2)
*   **Densidad Total: 36 ítems.**
*   **Inmersión:** 100% Idioma Objetivo (Instrucciones incluidas).
*   **Estructura:** Reading (10) + Use of English (15) + Listening (8) + Writing (2) + Speaking (1).

### B. ITINERARIO "MINOR" (Idioma Moderno / Lengua C / Niveles A1-A2)
*   **Densidad Total: 17 ítems.**
*   **Inmersión:** Híbrida (Instrucciones en CASTELLANO).
*   **Estructura:** Reading (5) + Grammar/Cloze (10) + Writing (2).
*   **Bloque 1: Comprensión Lectora (10 ítems):**
    *   Tarea 1.1: Selección Múltiple (5 ítems sobre Texto A). `interaction_type: QT_SEL`.
    *   Tarea 1.2: Emparejamiento Título-Párrafo (5 ítems sobre Texto A). `interaction_type: QT_MATCH`.
*   **Bloque 2: Uso de la Lengua (15 ítems):**
    *   Tarea 2.1: Multiple Choice Cloze (10 huecos en un solo párrafo). `interaction_type: QT_CLZ_OPT`.
    *   Tarea 2.2: Keyword Transformation (5 frases). `interaction_type: QT_TRF`.
*   **Bloque 3: Comprensión Auditiva (8 ítems):**
    *   Tarea 3.1: Selección Múltiple (8 ítems sobre Audio A). `interaction_type: QT_SEL`.
*   **Bloque 4: Expresión Escrita (2 ítems):**
    *   Tarea 4.1: Interacción (Email/Nota, 100-120 palabras). `interaction_type: QT_PROD`.
    *   Tarea 4.2: Expresión (Ensayo/Artículo, 180-220 palabras). `interaction_type: QT_PROD`.
*   **Bloque 5: Expresión Oral (1 ítem):**
    *   Tarea 5.1: Monólogo o Diálogo Simulado. `interaction_type: QT_PROD`, `response_mode: REQ_REC`.

### B. ITINERARIO "MINOR" (Modelo HSK/JLPT: Chino, Japonés, Árabe)
*   **Bloque 1: Comprensión y Gramática (15 ítems):**
    *   Tarea 1.1: Comprensión Lectora (5 ítems sobre Texto A). `QT_SEL`.
    *   Tarea 1.2: Ordenación de Frases (5 ítems). `QT_ORDER`.
    *   Tarea 1.3: Rellenar Huecos con Palabra Exacta (5 ítems). `QT_CLZ_OPN`.
*   **Bloque 2: Producción y Caligrafía (2 ítems):**
    *   Tarea 2.1: Redacción de Frases con Caracteres Dados (100 caracteres). `QT_PROD`.
    *   Tarea 2.2: Ejercicio de Caligrafía/Trazos. `QT_PROD`, `response_mode: REQ_DUAL` (para subir imagen del manuscrito).

## II. ARQUETIPO: LOGIC_AND_TECH (ETSIIT / Ciencias)
*   **Bloque 1: Test Teórico (15 ítems):**
    *   Preguntas de selección simple sobre conceptos fundamentales (Algoritmia, Cálculo, etc.). `QT_SEL`.
*   **Bloque 2: Resolución de Problemas (3 ítems):**
    *   3 problemas de desarrollo. `QT_PROD`. El `question_text` y `model_answer` deben usar formato LaTeX.

## III. ARQUETIPO: SOCIO_LEGAL (Derecho)
*   **Estímulo:** Un único "Supuesto de Hecho" (caso práctico) de 500-700 palabras.
*   **Bloque Único (5 ítems):**
    *   Tarea 1: Identificación de la Norma Aplicable (Respuesta corta). `QT_TRF`.
    *   Tarea 2-4: Fundamentación Jurídica (3 preguntas de desarrollo). `QT_PROD`.
    *   Tarea 5: Redacción de Dictamen Final (Ensayo). `QT_PROD`.

## IV. ARQUETIPO: HEALTH_SCIENCES (Medicina - ECOE)
*   **Estímulo:** Caso Clínico (informe de paciente, resultados de analítica, imagen de radiografía).
*   **Bloque Único - Estaciones (5 ítems):**
    *   Estación 1: Anamnesis y Sospecha Diagnóstica. `QT_PROD`.
    *   Estación 2: Pruebas a Solicitar. `QT_SEL`.
    *   Estación 3: Diagnóstico Diferencial. `QT_MATCH`.
    *   Estación 4: Plan Terapéutico. `QT_PROD`.
    *   Estación 5: Comunicación con el Paciente (Simulado). `QT_PROD`.

## V. ARQUETIPO: HUMANITIES_ARTS (Filosofía y Letras)
*   **Estímulo:** Fuente primaria (texto histórico/filosófico) o imagen de una obra de arte.
*   **Bloque Único - Comentario de Fuente (3 ítems):**
    *   Tarea 1: Fase Descriptiva/Contextual. `QT_PROD`.
    *   Tarea 2: Fase Analítica (Análisis formal/estilístico). `QT_PROD`.
    *   Tarea 3: Fase Crítica/Sintética (Conclusiones). `QT_PROD`.
