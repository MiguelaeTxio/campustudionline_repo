# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 09/11/2025 (CSO)

**Objetivo:** Refactorizar la lógica de propagación de estados de las autoevaluaciones (`badges`) en los directorios jerárquicos.

**Progreso y Descubrimientos Clave:**

1.  **Refactorización a Anotación Contextual:** La hipótesis inicial de un simple error de sintaxis del ORM se demostró incorrecta. El análisis de los modelos (`academic_structure`, `contents`, `assessment`) reveló la necesidad de abandonar la función de anotación genérica. Se implementó una solución de refactorización atómica, reemplazando la utilidad `annotate_with_assessment_states` por tres funciones especializadas y contextuales: una para el directorio académico, una para el contenido libre y otra para la sala de estudio.

2.  **Diagnóstico de Causa Raíz en la Capa de Presentación:** La implementación de las nuevas utilidades seguía sin mostrar los `badges`. La investigación empírica, a través del análisis de `tracebacks` (`VariableDoesNotExist`), reveló que el fallo no estaba en las vistas, sino en la capa de presentación. Se identificó un `templatetag` (`render_assessment_indicators`) que actuaba como intermediario y mantenía un contrato de datos obsoleto (`iv_data`), rompiendo la comunicación entre las vistas y la plantilla final del `badge`.

**Estado Final:** La sesión concluye con la corrección exitosa del `templatetag` `assessment_tags.py`. Con este cambio, la cadena de renderizado completa (vista -> `templatetag` -> plantilla de `badge`) quedó sincronizada. Los `badges` de estado de evaluación, incluido el de `'FAILED'`, ahora se muestran correctamente en todas las vistas de agregación. Sin embargo, al realizar la prueba final del flujo completo, se descubrió un nuevo fallo crítico.

## Hoja de Ruta para la Próxima Sesión

1.  **Diagnosticar el Fallo Inmediato en la Generación de Evaluaciones:**
    *   **Problema:** Al solicitar una nueva evaluación, esta pasa a un estado `'FAILED'` de forma casi instantánea.
    *   **Acción:** La primera acción será realizar una trazabilidad desde la base de datos. Se solicitará una evaluación y, acto seguido, se ejecutará un script en la `shell` de Django para inspeccionar el objeto `Assessment` recién creado. Se analizará su estado, `timestamps`, y cualquier posible mensaje de error asociado.
    *   **Acción Secundaria:** En paralelo, se analizarán los logs del worker de Celery para identificar cualquier excepción que ocurra durante la ejecución de la tarea de generación de la evaluación.

2.  **Verificación Empírica Integral:**
    *   Una vez solucionado el fallo de generación, se realizará una prueba completa del ciclo de vida de una evaluación para asegurar que todos los estados (`PENDING`, `PROCESSING`, `COMPLETED`, `RESULTS_AVAILABLE`, etc.) se propagan y visualizan correctamente en todas las vistas agregadas.
