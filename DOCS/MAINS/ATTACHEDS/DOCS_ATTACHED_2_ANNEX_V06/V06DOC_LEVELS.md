# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_LEVELS.md
# V06DOC_LEVELS - MATRIZ DE INTERSECCIÓN PEDAGÓGICA (V1.0)

Este documento define el cerebro pedagógico del emulador y las reglas de ajuste del motor de IA.

## 1. NIVELES DE DOMINIO ACADÉMICO (TAXONOMÍA UGR)

*   LVL_A (Acceso / Fundamentos):
    *   Enfoque: Identificación, descripción y reproducción de conceptos nucleares.
    *   Rigor: Descriptivo. Tolerancia media a la imprecisión terminológica.
*   LVL_B (Independiente / Aplicación):
    *   Enfoque: Resolución de problemas estándar y análisis funcional de casos.
    *   Rigor: Procedimental. Exigencia de coherencia lógica y técnica.
*   LVL_C (Maestro / Crítico):
    *   Enfoque: Evaluación de excepciones, síntesis de fuentes y creación original.
    *   Rigor: Epistemológico. Tolerancia cero a errores en conceptos base; exigencia de matiz.

## 2. REGLAS DE INTERSECCIÓN (ITINERARIO + NIVEL)

*   ITIN_MINOR + LVL_A:
    *   Rigor Engine: x0.8.
    *   Configuración: Vocabulario estándar, distractores obvios, feedback de apoyo (Rol Tutor).
*   ITIN_MINOR + LVL_B / ITIN_GEN:
    *   Rigor Engine: x1.0.
    *   Configuración: Aplicación práctica, terminología técnica básica, evaluación funcional.
*   ITIN_MAIOR + LVL_B / ITIN_PROF:
    *   Rigor Engine: x1.3.
    *   Configuración: Foco en la especialidad, rigor normativo, precisión técnica absoluta.
*   ITIN_MAIOR + LVL_C / ITIN_INV:
    *   Rigor Engine: x1.6.
    *   Configuración: Densidad técnica máxima, casos límite/ambiguos, evaluación de la crítica (Rol Catedrático).

## 3. PARÁMETROS DE EMULACIÓN DE "INDISTINGUIBILIDAD"

*   DENSITY_INDEX: Cantidad de tecnicismos por cada 100 palabras en el enunciado (Bajo en LVL_A | Máximo en LVL_C).
*   DISTRACTOR_QUALITY: Nivel de plausibilidad de las opciones erróneas (Lógica de error común en LVL_C).
*   GRADING_BIAS: Sesgo punitivo (Constructivo en Minor | Punitivo/Selectivo en Maior).
