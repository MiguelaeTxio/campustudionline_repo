# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_LEVELS.md
# V06DOC_LEVELS - MATRIZ DE INTERSECCIÓN PEDAGÓGICA (V1.2 - REFACTORIZACIÓN UGR)

Este documento define el cerebro pedagógico del emulador y las reglas de ajuste del motor de IA.

## 1. NIVELES DE DOMINIO ACADÉMICO (TAXONOMÍA UGR / CLM)

*   LVL_A (Acceso / Fundamentos - A1/A2):
    *   Enfoque: Identificación, descripción y reproducción de conceptos nucleares. Comprensión de frases aisladas y expresiones de uso frecuente.
    *   Rigor: Descriptivo. Tolerancia media a la imprecisión terminológica si el mensaje comunicativo es claro.
*   LVL_B (Independiente / Aplicación - B1/B2):
    *   Enfoque: B1 (Resolución de problemas estándar, descripciones simples). B2 (Análisis funcional, comprensión de ideas principales en textos complejos, argumentación técnica básica).
    *   Rigor: Procedimental. Exigencia de coherencia lógica, fluidez y corrección gramatical operativa.
*   LVL_C (Maestro / Crítico - C1/C2):
    *   Enfoque: C1 (Evaluación de excepciones, inferencia implícita, uso flexible del idioma). C2 (Maestría, matices finos de significado, fluidez espontánea absoluta).
    *   Rigor: Epistemológico. Tolerancia cero a errores en conceptos base; exigencia máxima de matiz y adecuación de registro (formal/académico).

## 2. REGLAS DE INTERSECCIÓN (ITINERARIO + NIVEL)

*   ITIN_MINOR + LVL_A:
    *   Rigor Engine: x0.8.
    *   Configuración: Vocabulario estándar, distractores obvios, feedback de apoyo (Rol Tutor).
*   ITIN_MINOR + LVL_B / ITIN_GEN:
    *   Rigor Engine: x1.0.
    *   Configuración: Aplicación práctica, terminología técnica básica, evaluación funcional CertAcles.
*   ITIN_MAIOR + LVL_B / ITIN_PROF:
    *   Rigor Engine: x1.3.
    *   Configuración: Foco en la especialidad, rigor normativo, precisión técnica absoluta y uso de metalenguaje.
*   ITIN_MAIOR + LVL_C / ITIN_INV / ITIN_PROF (TRA-TECH):
    *   Rigor Engine: x1.6 (General) | x1.7 (NORM) | x1.8 (PHILO / TRA-TECH).
    *   Configuración: [ACTUALIZADO 2026] Exigencia máxima de precisión terminológica y adecuación al Skopos profesional.
    *   Rigor Engine: x1.6 (General) | **x1.7 (Específico NORM UGR)** | **x1.8 (Específico Philo UGR)**.
    *   Configuración: Densidad técnica máxima, casos límite/ambiguos, evaluación de la crítica (Rol Catedrático). Exigencia de fundamentación bibliográfica en el feedback (DCECH, Blecua, NGLE, CORPES XXI).

## 3. PARÁMETROS DE EMULACIÓN DE "INDISTINGUIBILIDAD"

*   **DENSITY_INDEX (Índice de Densidad Epistemológica):**
    - **LVL_A:** 2-3 tecnicismos por cada 100 palabras.
    - **LVL_B:** 5-7 tecnicismos por cada 100 palabras.
    - **LVL_C (Philo / Norm UGR):** >12 tecnicismos por cada 100 palabras. Uso obligatorio de metalenguaje científico (archifonema, lenición, metafonía, yod, ecdoquización, diatopía, diafasía).
*   **DISTRACTOR_QUALITY:** Plausibilidad científica basada en errores de evolución fonética comunes (Philo) o dudas lingüísticas reales documentadas en el DPD y CORPES XXI (Norm).
*   **GRADING_BIAS (Sesgo de Calificación):**
    - **Constructivo (Minor):** Feedback de apoyo y refuerzo positivo.
    - **Punitivo/Selectivo (Maior Philo / Norm UGR):** Rigor eliminatorio. La imprecisión técnica o la falta de rigor formal en Nivel C supone la anulación total del ítem.

## 4. PROTOCOLO DE IDIOMA DE EVALUACIÓN (NORMATIVA UGR/CLM)

### 4.1. Arquetipo de Lenguas (ARCH_LANG)
*   **Nivel A (A1/A2):**
    *   **Itinerario MINOR / INSTR / INTRO:** Castellano (Obligatorio para garantizar la comprensión absoluta de la tarea y seguridad jurídica según normativa UGR).
    *   **Itinerario MAIOR:** Bilingüe (Inmersión progresiva con glosario de apoyo).
*   **Nivel B (B1/B2):**
    *   **Itinerario MINOR / INSTR:** Bilingüe (Instrucciones en castellano y en el idioma objetivo para garantizar comprensión inequívoca del encargo. La Guía del Candidato CLM-UGR confirma que las instrucciones de las tareas de producción escrita se entregan en la lengua del candidato para garantizar la comprensión del encargo sin que ello interfiera en la evaluación de la competencia lingüística).
    *   **Itinerario MAIOR:** Inmersión Total (Idioma Objetivo Dinámico).
*   **Nivel C (C1/C2):**
    *   **Todos los Itinerarios:** Inmersión Total (Idioma Objetivo Dinámico). La IA genera títulos e instrucciones en el idioma detectado para garantizar integridad absoluta. Prohibición de castellano en feedback.
*   **Criterio de Superación INSTR (CLM-UGR — ACTUALIZADO v5.0):** La superación de cada destreza en SUB-LIN-INSTR no se rige por un umbral fijo del 60%. Los puntos de corte B1 y B2 son variables por convocatoria, fijados siguiendo las pautas del Consejo de Europa mediante análisis estadístico. El alumno debe alcanzar el nivel objetivo en las cuatro destrezas de forma independiente. Si suspende una única destreza, puede repetirla en convocatoria posterior en un plazo máximo de un año.

### 4.2. Resto de Arquetipos (TECH, HEALTH, SOC, HUM)
*   **Idioma Vehicular:** Castellano obligatorio por seguridad jurídica, salvo excepciones internacionales documentadas.

### 4.3. Regla Especial Norma y Uso (UGR) [ACTUALIZADO V1.2]
*   **ITIN_MAIOR (NORM) + LVL_C:**
    *   **Rigor Engine:** x1.7.
    *   **Idioma:** Castellano Académico Obligatorio (Uso de metalenguaje filológico).
    *   **Configuración:** Exigencia de corrección absoluta. El error en la justificación normativa basada en el DPD o la confusión de fenómenos antinormativos (ej. confundir queísmo con dequeísmo) anula la puntuación del ítem (FAIL_LOGIC: FATAL).

### 4.4. Política de Tolerancia Cero Ortográfica (MAIOR Philo / Norm UGR) [ACTUALIZADO v5.0 - UNIFICADO]
En cumplimiento de la normativa de los departamentos de Filología de la UGR para niveles de excelencia (LVL_C). Los umbrales aquí definidos son coherentes con los declarados en V06DOC_BLOCKS.md y V06DOC_SUBARCHETYPES.md:
1.  **Penalización Sistemática (MAIOR Philo / Norm):** Descuento de **0.5 puntos** por cada falta de ortografía y **0.2 puntos** por cada error en tildes o signos de puntuación técnica (incluyendo puntuación ortotipográfica). Este baremo es más severo que el de INSTR dada la exigencia de LVL_C.
2.  **Penalización Sistemática (INSTR — CLM-UGR):** Descuento de **0.1 puntos** por cada falta de ortografía y **0.05 puntos** por cada error ortotipográfico (tildes, puntuación). Véase V06DOC_BLOCKS.md sección FORM_PEN.
3.  **Barrera de Exclusión Unificada:** La presencia de **más de 5 faltas de ortografía** en una sección de producción escrita o de comentario crítico conlleva el **Suspenso Automático** de la sección con nota **0.0 (FAIL_LOGIC: FATAL)**. Este umbral de 5 faltas aplica de forma transversal a todos los subarquetipos de la Rama Lenguas (INSTR, MINOR, PHILO, NORM, TRA-TECH, TRA-LIT) con los baremos de penalización por falta ajustados al rigor de cada subarquetipo.
4.  **Ortografía Técnica y Paleográfica (MAIOR Philo):** Se consideran faltas eliminatorias el uso incorrecto de grafemas medievales en transcripciones críticas y la mala aplicación del Alfabeto Fonético Internacional (IPA). Cada falta de este tipo computa como 1 falta a efectos del umbral de exclusión.

### 4.5. Regla Especial Philo (UGR)
*   **ITIN_MAIOR (PHILO) + LVL_C:**
    *   **Rigor Engine:** x1.8 (Máxima exigencia académica).
    *   **Configuración:** Evaluación de la etiología del cambio lingüístico. Tolerancia cero a errores en la reconstrucción formal y en la cronología relativa (CHRONO_STRICT). El alumno debe demostrar una capacidad de razonamiento diacrónico equivalente a un egresado de Grado de la UGR.
