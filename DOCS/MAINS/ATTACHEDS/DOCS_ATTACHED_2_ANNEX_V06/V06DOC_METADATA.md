<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_METADATA.md -->
# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_METADATA.md
# V06DOC_METADATA - MATRIZ DE ETIQUETADO Y DIAGNÓSTICO PEDAGÓGICO (V1.0)

# V06DOC_METADATA - MATRIZ DE ETIQUETADO Y DIAGNÓSTICO PEDAGÓGICO (V2.0 - FIDELIDAD 100% UGR)

Este documento define el lenguaje de marcado para la generación de ítems y la corrección automatizada.

## 1. DOMINIOS DE COMPETENCIA (COMPETENCY_DOMAIN)
*   COMP_GEN: Competencias Genéricas (Síntesis, expresión, organización).
*   COMP_TRA: Competencias Transversales (Pensamiento crítico, TIC, ética).
*   COMP_ESP: Competencias Específicas (Conocimiento técnico nuclear de la materia).
*   COMP_PROF: Competencias Profesionales (Resolución de problemas reales y toma de decisiones).

## 2. TAXONOMÍA COGNITIVA (COGNITIVE_TAXONOMY)
*   COG_REM: Recordar (Identificación de conceptos y datos).
*   COG_UND: Comprender (Explicación e interpretación).
*   COG_APP: Aplicar (Uso de información en casos prácticos).
*   COG_ANA: Analizar (Relación lógica entre componentes).
*   COG_EVAL: Evaluar (Justificación de posturas y crítica).
*   COG_CREA: Crear (Generación de propuestas originales).

## 3. ATRIBUTOS TÉCNICOS DEL ÍTEM (ITEM_ATTRIBUTES)
*   LEVEL_REQUISITE: [Mandatory | Optional | Advanced].
*   WEIGHT_FACTOR: Peso relativo (0.1 a 1.0).
*   ESTIMATED_TIME: Tiempo de resolución esperado (segundos).
*   FAIL_LOGIC: [PENALTY | FATAL | PARTIAL].

## 4. TAXONOMÍA DE FEEDBACK (FEEDBACK_TAXONOMY)
*   FB_CONCEPT: Error conceptual por falta de base teórica.
*   FB_FORMAL: Error de registro, sintaxis o corrección formal.
*   FB_PROCEDURAL: Error en el método o secuencia lógica.
*   FB_SAFETY: Violación de protocolos críticos o de seguridad.

## 5. METADATOS ESPECÍFICOS UGR (ACREDITACIÓN CERTACLES) [REFACTORIZADO v5.0 - FIDELIDAD 100% UGR]
*   **SCORING_MECHANISM:** Puntos de corte variables por convocatoria, fijados siguiendo las pautas del Consejo de Europa y el MCERL. No existe un umbral fijo del 60%: el punto de corte B1 y el punto de corte B2 se establecen mediante análisis estadístico de la distribución de respuestas de cada convocatoria.
*   **PASS_CONDITION:** El alumno debe alcanzar el nivel B1 o B2 (según su objetivo) en las CUATRO destrezas evaluadas de forma independiente. La compensación entre destrezas no está permitida.
*   **FAIL_LOGIC_INSTR:** PARTIAL_RETRY — Si el alumno no alcanza el nivel en una única destreza, podrá examinarse de esa sola destreza en una convocatoria posterior en un plazo máximo de un año. Si son dos o más destrezas suspendidas, debe repetir el examen completo.
*   **WORD_COUNT_RANGE:**
    - `WRIT_T1`: [200, 250] (Rango oficial CLM-UGR para Tarea 1 — Nivel B1).
    - `WRIT_T2`: [250, 300] (Rango oficial CLM-UGR para Tarea 2 — Nivel B2).
*   **PENALTY_OOB:** Penalización de -0.5 puntos por cada tramo de 10 palabras de desviación del rango establecido.
*   **NO_NEGATIVE_MARKING:** Las respuestas incorrectas en las destrezas de Comprensión de Lectura y Comprensión Auditiva NO restan puntuación. El motor PRM-STRIKE (penalización por azar) queda DESACTIVADO para el subarquetipo SUB-LIN-INSTR.
*   **AUDIO_PLAYS_LIMIT:** 2 reproducciones por pista de audio en SD_LIST. Bloqueo hermético tras la segunda reproducción completa.

## 6. METADATOS ESPECÍFICOS PHILO (UGR)
*   **DOMAIN_PHILO:** [PHONO | MORPH_DIAC | LEX_DIAC | ECDO].
*   **DIAC_PRECISION:** Nivel de exactitud en la reconstrucción de la ley fonética (0.0 a 1.0).
*   **SOURCE_AUTHENTICITY:** Marcador para el análisis de variantes en crítica textual.

## 7. METADATOS ESPECÍFICOS NORM (UGR - NORMA Y USO)
*   **DOMAIN_NORM:** [MORPH_ANTINORM | LEX_ANTINORM | CORPUS_VAL | PANHISPANIC_NORM].
*   **CORPUS_REF:** Referencia obligatoria a CORPES XXI o CREA para validación de uso real frente a prescripción académica.
*   **DICT_CONSULT:** Uso obligatorio de herramientas de consulta de la RAE/ASALE (DPD, DLE, NGLE, diccionarios de estilo).
*   **NORM_VS_USE:** Marcador de discrepancia entre prescripción académica (norma panhispánica culta) y uso social documentado en corpus.
