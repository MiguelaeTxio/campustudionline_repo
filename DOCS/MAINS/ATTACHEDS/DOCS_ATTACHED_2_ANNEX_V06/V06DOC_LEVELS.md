<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_LEVELS.md -->
# V06DOC_LEVELS - MATRIZ DE INTERSECCIÓN PEDAGÓGICA (V1.2)

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
*   ITIN_MAIOR + LVL_C / ITIN_INV:
    *   Rigor Engine: x1.6.
    *   Configuración: Densidad técnica máxima, casos límite/ambiguos, evaluación de la crítica (Rol Catedrático).

## 3. PARÁMETROS DE EMULACIÓN DE "INDISTINGUIBILIDAD"

*   DENSITY_INDEX: Cantidad de tecnicismos/modismos por cada 100 palabras en el enunciado (Bajo en LVL_A | Máximo en LVL_C).
*   DISTRACTOR_QUALITY: Nivel de plausibilidad de las opciones erróneas (Lógica de error común de L1 en B2/C1).
*   GRADING_BIAS: Sesgo punitivo (Constructivo en Minor | Punitivo/Selectivo en Maior).

## 4. PROTOCOLO DE IDIOMA DE EVALUACIÓN (NORMATIVA UGR/CLM)

La determinación del idioma en las instrucciones y títulos de sección (interfaz del examen) se rige por la normativa oficial de la UGR y el CLM:

### 4.1. Arquetipo de Lenguas (ARCH_LANG)
*   **Nivel A (A1/A2):**
    *   **Itinerario MINOR / INSTR:** Castellano (Para garantizar la comprensión de la tarea).
    *   **Itinerario MAIOR:** Bilingüe (Inmersión progresiva).
*   **Nivel B (B1/B2):**
    *   **Itinerario MINOR / INSTR:** Bilingüe (Instrucciones duales para garantizar comprensión de la tarea, ej. pruebas de mediación).
    *   **Itinerario MAIOR:** Inmersión Total (Idioma Objetivo Dinámico).
*   **Nivel C (C1/C2):**
    *   **Todos los Itinerarios:** Inmersión Total (Idioma Objetivo Dinámico). La IA genera títulos e instrucciones en el idioma detectado para garantizar integridad absoluta. Prohibición de castellano en feedback.

### 4.2. Resto de Arquetipos (TECH, HEALTH, SOC, HUM)
*   **Idioma Vehicular:** Castellano obligatorio por seguridad jurídica, salvo excepciones internacionales documentadas.
