# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 10/11/2025 (MAMC)

**Objetivos:** Refactorizar el sistema de autoevaluaciones, centralizar la lógica de indicadores de estado (badges) en la Sala de Estudio y diagnosticar y corregir una cascada de errores de importación (`ImportError`).

**Progreso y Descubrimientos Clave:**

1.  **Refactorización del Backend:** Se completó la refactorización para centrar la lógica en `ContentCopy`. Se modificaron `tasks.py`, `views.py`, `urls.py`, y `admin.py` de la app `assessment`, y se aplicó la migración `0009`.
2.  **Implementación de Lógica de Descarte:** Se implementó la mecánica de "visto/no visto" para las notificaciones:
    *   Se refactorizó `core/context_processors.py` para que los contadores de la barra de navegación solo muestren avisos de evaluaciones cuyo flag `was_viewed` es `False`.
    *   Se implementó en `contents/study_room_views.py` la lógica que marca automáticamente como "vistas" las evaluaciones fallidas al acceder a la `edit_copy` correspondiente.
3.  **Desmantelamiento de Indicadores Públicos:** Se eliminaron los indicadores de estado de todas las plantillas de los directorios públicos (`academic_directory`, `search`, etc.) para centralizar la funcionalidad.
4.  **Diagnóstico y Corrección de Errores en Cascada:** El intento de purgar el código obsoleto reveló un fallo sistémico en la auditoría de dependencias, provocando una cascada de tres `ImportError` consecutivos que interrumpieron el cierre de sesión. Se diagnosticó y corrigió empíricamente cada error, eliminando las importaciones y llamadas a funciones obsoletas en:
    *   `contents/study_room_views.py`
    *   `search/views.py`
    *   `academic_directory/views.py`

**Estado Final:** El sistema se encuentra estable. La refactorización del backend y la limpieza de plantillas están completas. La lógica de descarte de notificaciones está implementada. Queda pendiente el purgado final del código Python obsoleto.

## Hoja de Ruta para la Próxima Sesión

1.  **Fase 1: Purgado Final de Código Obsoleto:**
    *   Eliminar el template tag `render_assessment_indicators` de `assessment/templatetags/assessment_tags.py`.
    *   Eliminar la plantilla parcial `assessment/templates/assessment/partials/_assessment_indicator_badge.html` que quedó sin crear.
2.  **Fase 2: Verificación Funcional en Sala de Estudio:**
    *   Confirmar que la vista de lista de la Sala de Estudio (`_copy_list_partial.html`) muestra correctamente los indicadores de estado para cada `ContentCopy` utilizando su propia lógica, ahora que el tag global ha sido eliminado.
    *   Realizar pruebas para verificar que los contadores de la barra de navegación reflejan únicamente los estados de la Sala de Estudio y que la lógica de descarte de notificaciones (`was_viewed`) funciona correctamente.
