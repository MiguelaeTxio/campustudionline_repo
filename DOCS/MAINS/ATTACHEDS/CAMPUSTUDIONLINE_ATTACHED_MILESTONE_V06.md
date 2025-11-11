# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 11/11/2025 (EDC)

**Objetivo:** Implementar la visualización jerárquica de los indicadores de estado de las evaluaciones (`badges`) en la "Sala de Estudio", asegurando que los niveles de directorio superiores (Áreas, Disciplinas) reflejen un estado agregado de las `ContentCopy` que contienen.

**Progreso y Descubrimientos Clave:**

1.  **Diagnóstico del Problema:** Se confirmó empíricamente que la implementación anterior no mostraba los indicadores en los niveles jerárquicos. La causa raíz se localizó en la vista `contents/study_room_views.py`, que no anotaba los `QuerySets` de los directorios con la información de estado necesaria.
2.  **Primer Intento de Corrección Fallido:** Se implementó una lógica de subconsultas en la vista que resultó ser defectuosa, provocando un `Internal Server Error` (`AttributeError: IN_PROGRESS`) al recargar la página.
3.  **Investigación Empírica:** Siguiendo el protocolo `PEO`, se solicitó y analizó el modelo `assessment/models.py`. Se descubrió que el estado para "en progreso" estaba definido como `PROCESSING`, y no `IN_PROGRESS` como se había supuesto. Este fue el único punto de fallo.
4.  **Implementación Definitiva:** Se corrigió el nombre del estado en la subconsulta de la vista `contents/study_room_views.py`. Tras aplicar el cambio, la funcionalidad fue restaurada con éxito.

**Estado Final:** El sistema es estable. Los indicadores de estado de las evaluaciones ahora se muestran correctamente en toda la jerarquía de la Sala de Estudio, reflejando el estado de mayor prioridad de las copias contenidas.

## Hoja de Ruta para la Próxima Sesión

1.  **Fase 1: Diagnóstico del Bucle de Procesamiento:**
    *   **Objetivo:** Investigar por qué las evaluaciones se quedan permanentemente en estado `PROCESSING` y nunca transicionan a `COMPLETED` o `FAILED`.
    *   **Plan:**
        *   Revisar la tarea Celery responsable de generar las evaluaciones (`assessment/tasks.py`).
        *   Inspeccionar los logs de Celery en busca de errores silenciosos o bucles infinitos.
        *   Verificar la comunicación con la API de IA y el manejo de sus respuestas.
        *   Realizar una prueba de generación de evaluación de principio a fin, monitorizando el estado en la base de datos y los logs en tiempo real.
