# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 09/11/2025 (CSO)

**Objetivo:** Refactorizar la lógica de propagación de estados de las autoevaluaciones (`badges`) en los directorios jerárquicos.

**Progreso y Descubrimientos Clave:**

1.  **Implementación de Nueva Utilidad:** Se reemplazó la función obsoleta `get_latest_active_assessment_subqueries` por una nueva, `annotate_with_assessment_states`, diseñada para agregar correctamente los estados descendientes. La nueva utilidad fue integrada en las vistas de `academic_directory`, `search` y `contents`.

2.  **Diagnóstico de Causa Raíz a través de Fallos Múltiples:** La verificación empírica de la implementación falló repetidamente, revelando una comprensión incorrecta de cómo el ORM de Django maneja las expresiones de consulta complejas:
    *   **Primer Fallo (`TypeError`):** Se intentó comparar un objeto `Subquery` con un entero, lo cual no es soportado.
    *   **Segundo Fallo (`TypeError`):** Se intentó comparar un objeto `Coalesce` con un entero, demostrando el mismo error conceptual.
    *   **Tercer Fallo (`FieldError`):** El uso de sintaxis de `lookup` por palabra clave (`kwarg=value`) con un objeto de expresión (`Coalesce`) fue interpretado incorrectamente por el ORM como un `lookup` de campo, resultando en un error de campo no encontrado.

**Estado Final:** La sesión concluye sin resolver el problema funcional, pero con un diagnóstico empírico y definitivo de la causa raíz. El error no es de lógica, sino de sintaxis en la construcción de consultas complejas. La solución correcta, validada mediante investigación de la documentación, requiere el uso explícito de clases de `lookup` de Django (ej. `GreaterThan`, `Exact`) para encapsular **todas** las operaciones de comparación que involucren objetos de expresión.

## Hoja de Ruta para la Próxima Sesión

La próxima sesión tiene un único objetivo atómico y de máxima prioridad:

1.  **Implementar la Corrección Definitiva:**
    *   Modificar el archivo `assessment/utils.py` para importar `GreaterThan` y `Exact` desde `django.db.models.lookups`.
    *   Reescribir las condiciones `When` dentro de la función `annotate_with_assessment_states` para usar estas clases, eliminando así la sintaxis de `lookup` por palabra clave y los `TypeError`.
    *   **Ejemplo:** `When(coalesced_subquery=1, ...)` se convertirá en `When(Exact(coalesced_subquery, Value(1)), ...)`.

2.  **Verificación Empírica:**
    *   Tras aplicar el parche y recargar el servidor, se procederá a una verificación exhaustiva en los tres directorios afectados para confirmar la erradicación del `FieldError` y el correcto funcionamiento de los `badges`.
