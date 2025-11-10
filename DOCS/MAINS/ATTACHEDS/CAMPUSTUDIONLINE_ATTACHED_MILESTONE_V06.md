# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 10/11/2025 (MAMC)

**Objetivos:** Refactorizar el sistema de autoevaluaciones para centrarlo en el modelo `ContentCopy` y reubicar la lógica de indicadores de estado (badges) exclusivamente en la Sala de Estudio.

**Progreso y Descubrimientos Clave:**

1.  **Migración de Base de Datos:** Se generó y aplicó con éxito la migración `0009_alter_assessment_content.py`, que anula el campo `content` del modelo `Assessment`, formalizando la transición a `content_copy` como única fuente de verdad.
2.  **Refactorización del Backend:** Se refactorizaron los siguientes archivos para eliminar por completo la dependencia del campo `content` y utilizar `content_copy`:
    *   `assessment/tasks.py`: Modificada la tarea `generate_assessment_from_content_task` para obtener el material de estudio a través de `content_copy`.
    *   `assessment/views.py`: Adaptadas todas las vistas para operar con `content_copy` y `copy_pk`.
    *   `assessment/urls.py`: Actualizada la ruta `generate_ai_assessment` para usar `copy_pk`.
    *   `assessment/admin.py`: Actualizada la interfaz de administración para reflejar la nueva estructura.
3.  **Implementación de Lógica de Descarte:** Se implementó la mecánica de "visto/no visto" para las notificaciones:
    *   Se refactorizó `core/context_processors.py` para que los contadores de la barra de navegación solo muestren avisos de evaluaciones cuyo flag `was_viewed` es `False`.
    *   Se implementó en `contents/study_room_views.py` la lógica que marca automáticamente como "vistas" (`was_viewed=True`) las evaluaciones fallidas al acceder a la `edit_copy` correspondiente.
4.  **Desmantelamiento de Indicadores Públicos:** Siguiendo la nueva directiva, se inició la eliminación de los indicadores de estado de todas las vistas de directorios públicos. Se limpiaron las siguientes plantillas:
    *   `academic_directory/templates/academic_directory/academic_level_detail.html`
    *   `search/templates/search/search_home.html`
    *   `search/templates/search/category_detail.html`
    *   `contents/templates/contents/partials/_folder_nodes.html`
    *   `core/templates/core/partials/_navbar_indicators.html` fue modificado para aplicar la lógica condicional, aunque el plan fue re-refinado posteriormente.

**Estado Final:** La refactorización del backend está completa y la lógica de descarte de notificaciones ha sido implementada. Se ha completado el desmantelamiento de los indicadores en las plantillas de los directorios públicos. La sesión se detuvo antes de purgar el código Python obsoleto y verificar la implementación final en la Sala de Estudio.

## Hoja de Ruta para la Próxima Sesión

1.  **Fase 1: Purgado de Código Obsoleto:**
    *   Eliminar el template tag `render_assessment_indicators` de `assessment/templatetags/assessment_tags.py`.
    *   Eliminar las funciones de anotación obsoletas (`annotate_academic_queryset_with_assessment_states`, etc.) de `assessment/utils.py`.
2.  **Fase 2: Verificación y Refinamiento en Sala de Estudio:**
    *   Verificar que la vista de lista de la Sala de Estudio (`_copy_list_partial.html`) muestra correctamente los indicadores de estado para cada `ContentCopy`.
    *   Realizar pruebas funcionales para confirmar que los contadores de la barra de navegación reflejan únicamente los estados de la Sala de Estudio y que la lógica de descarte funciona como se espera al ver resultados o fallos.
