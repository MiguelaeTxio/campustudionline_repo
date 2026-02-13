# V06DOC_LOGIC_MAPPING - ALGORITMO DE DEDUCCIÓN ACADÉMICA (V1.1)

Este documento define las reglas heurísticas para deducir los parámetros de evaluación basándose en patrones estructurales y no en listas finitas.

## 1. DEDUCCIÓN DE ARQUETIPO (ARCH_*)

**Regla Maestra:** Análisis de Patrones en el Nombre de la Asignatura (Case Insensitive).

1.  **Arquetipo LENGUAS (`ARCH_LANG`):**
    *   Si `Subject.name` contiene patrones regex: `(lengua|idioma|language)`.
    *   *Ejemplo:* "Lengua Moderna Minor Checo" -> `ARCH_LANG`.
    *   *Ejemplo:* "Idioma Moderno: Inglés" -> `ARCH_LANG`.

2.  **Arquetipo HUMANIDADES (`ARCH_HUM`):**
    *   Si no es Lengua, y `Branch` contiene "Artes" o "Humanidades".

3.  **Resto de Arquetipos:**
    *   Mapeo directo por `Branch` (Salud, Ingeniería, Sociales).

## 2. DEDUCCIÓN DE ITINERARIO (ITIN_*)

1.  **Detección Explícita (Regex):**
    *   Si `Subject.name` contiene `\bmaior\b` -> `ITIN_MAI`.
    *   Si `Subject.name` contiene `\bminor\b` -> `ITIN_MIN`.

2.  **Deducción por Tipo (Fallback):**
    *   Troncal/Obligatoria -> `ITIN_MAI`.
    *   Optativa -> `ITIN_MIN`.

## 3. DEDUCCIÓN DE NIVEL PEDAGÓGICO (LVL_*)

Prioridad: Semántica del Nombre > Año Académico.

1.  **Detección Semántica (Regex):**
    *   **Nivel A (Acceso):** `(inicial|básico|basico|a1|a2|intro)`.
    *   **Nivel B (Independiente):** `(intermedio|b1|b2)`.
    *   **Nivel C (Competente):** `(avanzado|superior|c1|c2)`.

2.  **Deducción por Curso (Fallback):**
    *   1º y 2º Año -> `LVL_A`.
    *   3º Año -> `LVL_B`.
    *   4º+ Año -> `LVL_C`.
