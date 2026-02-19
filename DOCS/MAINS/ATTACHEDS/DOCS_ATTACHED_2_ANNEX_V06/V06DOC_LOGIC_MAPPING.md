<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_LOGIC_MAPPING.md -->
# V06DOC_LOGIC_MAPPING - PROTOCOLO DE CLASIFICACIÓN ACADÉMICA (V1.3)

Este documento define el procedimiento híbrido para la clasificación de asignaturas y su protocolo de resiliencia.

## 1. FASE IA: IDENTIFICACIÓN DE NATURALEZA (COGNITIVA)

Se utiliza `gemini-2.5-flash-lite` exclusivamente para resolver la ambigüedad semántica del catálogo de asignaturas (>20.000 registros).

### 1.1. Entrada del Clasificador
*   `Subject.name`, `Branch.name`, `Degree.name`.

### 1.2. Salida de la IA (Contrato JSON)
La IA solo debe proporcionar la identidad técnica:
*   `archetype_id`: [ARCH_LANG | ARCH_HEALTH | ARCH_TECH | ARCH_SOC | ARCH_HUM].
*   `sub_archetype_id`: ID técnico de especialidad (Ref: V06DOC_SUBARCHETYPES).

## 2. FASE PYTHON: DEDUCCIÓN DE PARÁMETROS (DETERMINISTA)

El servidor aplica las reglas de negocio de la plataforma para garantizar la consistencia pedagógica y legal.

### 2.1. Deducción de Itinerario (ITIN_*)
1.  **Detección por Nombre:** Regex `\bmaior\b` -> `ITIN_MAI` | `\bminor\b` -> `ITIN_MIN`.
2.  **Detección por Tipo (Fallback):**
    *   Si `Subject.subject_type` es `MANDATORY` o `CORE` -> `ITIN_MAI`.
    *   Si `Subject.subject_type` es `OPTIONAL` -> `ITIN_MIN`.
3.  **Mapeo por Rama:** Ramas de Salud activan `ITIN_ROT` y ramas Técnicas activan `ITIN_PROF`.

### 2.2. Deducción de Nivel Pedagógico (LVL_*)
Se calcula según el año académico del objeto `Subject`:
*   1º y 2º Año -> `LVL_A`.
*   3º Año -> `LVL_B`.
*   4º Año o Superior -> `LVL_C`.

### 2.3. Modo de Inmersión (IMMERSION_*)
Se aplica la Matriz UGR de `V06DOC_LEVELS.md` cruzando el `archetype_id` (IA) con el `itinerary_id` y `pedagogical_level` (Python).

## 3. PROTOCOLO DE RESILIENCIA Y FALLO DE API

Queda prohibida la clasificación por defecto en caso de error de conectividad.

1.  **Reintentos:** Ante un fallo de la API, el sistema ejecutará hasta 3 reintentos automáticos con un intervalo de 10 minutos entre ellos.
2.  **Notificación de Aborto:** Si tras el tercer reintento la API persiste en el error:
    *   Se detiene el proceso de generación del examen.
    *   Se notifica al usuario vía **Correo Electrónico** y **Notificación Push**.
    *   Mensaje: "Servicio de Clasificación no disponible temporalmente. Por favor, inténtelo de nuevo más tarde."
