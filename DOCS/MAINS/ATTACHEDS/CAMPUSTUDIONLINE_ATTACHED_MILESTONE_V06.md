### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

**Nota para el cierre (`PCS`):** Esta sección debe ser copiada textualmente en la "Hoja de Ruta para la Siguiente Sesión" para garantizar la persistencia de la Ley.

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (IMPLEMENTACIÓN DEL ESTÁNDAR UGR)

1.  **Tarea 1 (Arquitectura): Implementar el "Strategy Factory Pattern"**
    *   **Objetivo:** Eliminar la llamada hardcodeada a `languages_strategy.py` y hacer que el sistema sea verdaderamente polimórfico.
    *   **Acción:**
        *   Crear el archivo `core/services/assessment_strategies/factory.py`.
        *   Dentro de la factory, crear un diccionario que mapee cada `archetype` (ej: `"CEFR_LANGUAGES"`) a su módulo de estrategia correspondiente.
        *   Modificar `orchestrator/tasks.py` para que, en lugar de importar `languages_strategy`, importe la `factory`. La tarea llamará a `factory.get_strategy(assessment.archetype)` para obtener dinámicamente el módulo correcto.

2.  **Tarea 2 (Modelo de Datos): Especializar el Itinerario Lingüístico**
    *   **Objetivo:** Permitir que la base de datos distinga entre exámenes de lenguas "Maior" y "Minor".
    *   **Acción:**
        *   En `assessment/models.py`, añadir al modelo `Assessment` el campo: `language_itinerary = models.CharField(max_length=10, choices=[('MAIOR', 'Maior'), ('MINOR', 'Minor')], null=True, blank=True)`.
        *   Generar y aplicar la migración de base de datos correspondiente.

3.  **Tarea 3 (Lógica de Clasificación Lingüística):**
    *   **Objetivo:** Automatizar la detección del itinerario "Maior" o "Minor".
    *   **Acción:**
        *   En `orchestrator/tasks.py`, dentro de `generate_assessment_from_content_task`, justo después de obtener el `subject_name`, implementar una lógica que analice el nombre y determine si es "Maior" o "Minor", guardando el resultado en el nuevo campo `assessment.language_itinerary`.

4.  **Tarea 4 (Refactorización de la Estrategia de Idiomas):**
    *   **Objetivo:** Implementar los esqueletos de alta densidad definidos en el documento de arquetipos.
    *   **Acción:**
        *   En `languages_strategy.py`, la función `get_strategy_skeleton` se convertirá en un despachador que leerá el `language_itinerary` del assessment.
        *   Crear dos funciones privadas: `_build_maior_skeleton()` y `_build_minor_skeleton()`, cada una devolviendo la estructura de bloques y la densidad de ítems especificada en `CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`.
