<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_METADATA.md -->
# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_METADATA.md
# V06DOC_METADATA - MATRIZ DE ETIQUETADO Y DIAGNÓSTICO PEDAGÓGICO (V1.0)

## 6. METADATOS ESPECÍFICOS NORM (UGR - NORMA Y USO)
*   **DOMAIN_NORM:** [MORPH_ANTINORM | LEX_ANTINORM | CORPUS_VAL | PANHISPANIC_NORM].
*   **CORPUS_REF:** Referencia obligatoria a CORPES XXI o CREA para validación de uso.
*   **DICT_CONSULT:** Uso de herramientas de consulta (DPD, RAE, Diccionarios de Estilo).
*   **NORM_VS_USE:** Marcador de discrepancia entre prescripción académica y uso social.


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


## 5. METADATOS ESPECÍFICOS UGR (ACREDITACIÓN CERTACLES) [REFACTORIZADO SUBATÓMICO]
*   **THRESHOLD_SKILL:** 0.60 (Umbral del 60% exigido por la UGR por cada destreza de forma independiente).
*   **FAIL_LOGIC:** FATAL (La caída por debajo de THRESHOLD_SKILL en cualquier sección anula la acreditación global sin compensación).
*   **WORD_COUNT_RANGE:**
    - `WRIT_T1`: [120, 150] (Rango para interacción funcional).
    - `WRIT_T2`: [150, 180] (Rango para producción académica).
*   **PENALTY_OOB:** Penalización de -0.5 puntos por cada tramo de 10 palabras de desviación del rango.

## 6. METADATOS ESPECÍFICOS PHILO (UGR)
*   **DOMAIN_PHILO:** [PHONO | MORPH_DIAC | LEX_DIAC | ECDO].
*   **DIAC_PRECISION:** Nivel de exactitud en la reconstrucción de la ley fonética (0.0 a 1.0).
*   **SOURCE_AUTHENTICITY:** Marcador para el análisis de variantes en crítica textual.
