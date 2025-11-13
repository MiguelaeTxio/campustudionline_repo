# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 13/11/2025 (CSO)

**Objetivo:** Diagnosticar y erradicar la causa raíz de un bucle de fallos en la generación de autoevaluaciones que dejaba las tareas en un estado de reintento perpetuo.

**Desarrollo y Resultado Empírico:**
La sesión aplicó un riguroso método empírico, utilizando logs de Celery y scripts en la `shell` de Django como únicas fuentes de verdad para el diagnóstico.
1.  **Diagnóstico Inicial:** Se identificó un `AttributeError` en `assessment/tasks.py` debido a una discrepancia entre el nombre de un estado de fallo en el código (`FAILED_RETRYABLE`) y su definición en el modelo (`GENERATION_FAILED_RETRYABLE`).
2.  **Primera Corrección y Nuevo Hallazgo:** Tras corregir el primer error, las pruebas empíricas revelaron un `TypeError` análogo en la misma tarea, donde el constructor del modelo `Question` recibía un argumento `question` en lugar del esperado `question_text`.
3.  **Segunda Corrección y Hallazgo Final:** La corrección del segundo `TypeError` destapó un tercer error de consistencia: la tarea de corrección (`correct_assessment_task`) también llamaba a `generate_text_content` sin el argumento `api_key` requerido, provocando un nuevo `TypeError`.
4.  **Validación Final:** Tras corregir los tres errores de programación en `assessment/tasks.py`, se ejecutó con éxito un ciclo de vida completo (generación, simulación de respuestas y corrección) desde la `shell` de Django, validando empíricamente que el sistema es ahora funcional y robusto.

**Estado Final:** El sistema de autoevaluaciones ha sido reparado y validado. No obstante, se han detectado nuevas incidencias de navegación no relacionadas que se abordarán a futuro.

## Hoja de Ruta para la Próxima Sesión

El objetivo será diagnosticar y corregir dos comportamientos anómalos en la navegación de la Sala de Estudio.

1.  **Incidencia 1: Error `Not Found` Transitorio.**
    *   **Síntoma:** Al crear una `ContentCopy` y navegar a ella por primera vez, el sistema devuelve un error `Not Found`. En un segundo intento de navegación, la URL se resuelve correctamente.
    *   **Hipótesis:** Posible problema de caché, resolución de URL diferida o una condición de carrera en la vista que muestra la copia.
    *   **Plan:** Replicar el error y analizar la vista responsable de renderizar la `ContentCopy` (`study_room:edit_copy`) y su lógica de obtención de objetos.

2.  **Incidencia 2: Navegación Cruzada por `ContentHashFamily`.**
    *   **Síntoma:** Una `ContentCopy` creada para un `ContentMaterial` asociado a un grado (ej. "Lenguas Modernas") aparece también listada bajo otro grado (ej. "Estudios Franceses") si ambos comparten la misma `ContentHashFamily`.
    *   **Hipótesis:** La vista que lista las `ContentCopy` de un usuario para un grado o materia específicos está filtrando incorrectamente, basándose en la `ContentHashFamily` en lugar de la jerarquía académica estricta.
    *   **Plan:** Analizar y corregir la lógica de filtrado en las vistas de la Sala de Estudio para asegurar que la presentación de copias respete la estructura académica del `academic_directory`.
