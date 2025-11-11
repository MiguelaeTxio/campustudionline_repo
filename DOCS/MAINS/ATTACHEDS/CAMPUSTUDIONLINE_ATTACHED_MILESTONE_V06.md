# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 11/11/2025 (EDC)

**Objetivo Inicial:** Investigar por qué las evaluaciones se quedaban permanentemente en estado `PROCESSING`.

**Desarrollo y Descubrimientos Clave:**
La sesión fue inmediatamente interrumpida por un error crítico `NoReverseMatch` que impedía la carga de la "Sala de Estudio". La depuración siguió un riguroso proceso empírico:

1.  **Diagnóstico Inicial y Corrección Fallida:** Se identificó una llamada a `reverse()` con `pk=None` en `assessment/utils.py`. La corrección aplicada en este archivo resultó ser insuficiente, ya que el error persistía.
2.  **Investigación Empírica Ampliada:** Se utilizó `grep` para localizar de forma inequívoca **todas** las invocaciones a la URL `take_assessment`. Esta búsqueda reveló una segunda llamada no contemplada en la plantilla `assessment/templates/assessment/partials/_assessment_indicator_badge.html`.
3.  **Corrección de `NoReverseMatch`:** Se añadió una guarda `{% if latest_assessment_pk %}` en `_assessment_indicator_badge.html`, solucionando definitivamente el `NoReverseMatch`.
4.  **Diagnóstico de Regresión Visual:** La solución anterior provocó que los `badges` de estado desaparecieran de los directorios de nivel superior. La investigación de `contents/study_room_views.py` reveló que se utilizaban dos métodos distintos e incompatibles para anotar el estado de las evaluaciones. El método para directorios no proporcionaba el `latest_assessment_pk` necesario.
5.  **Refactor y Corrección de Regresión:** Se refactorizó `study_room_views.py` para utilizar un método de anotación unificado, restaurando la visibilidad de los `badges` en los directorios.
6.  **Diagnóstico y Corrección de UX:** El `refactor` expuso un problema de HTML inválido (enlaces `<a>` anidados) que causaba una mala experiencia de usuario. Se corrigió convirtiendo los `badges` en elementos `<span>` no interactivos, resolviendo el conflicto.

**Estado Final:** La aplicación es estable y funcional. Los errores críticos y las regresiones visuales han sido solucionados. La navegación y la visualización de estados en la "Sala de Estudio" operan como se espera.

## Hoja de Ruta para la Próxima Sesión

1.  **Fase 1: Corrección del Temporizador de Evaluaciones (UX).**
    *   **Objetivo:** Investigar por qué el temporizador en la vista de edición de copia (`edit_copy`) muestra un valor estático (`--:--:--`) en lugar de la cuenta regresiva.
    *   **Plan:**
        *   Analizar el código Javascript responsable de inicializar y actualizar los temporizadores en las plantillas `assessment/partials/assessment_status_block.html` y `assessment/view_results.html`.
        *   Verificar que los datos `data-end-time` se estén pasando correctamente desde el contexto de Django a la plantilla.
        *   Depurar el script para asegurar que el cálculo de la diferencia de tiempo y la actualización del DOM se realizan correctamente.

2.  **Fase 2: Diagnóstico del Bucle de Procesamiento (Objetivo Original).**
    *   **Objetivo:** Retomar la investigación original para determinar por qué las evaluaciones se quedan permanentemente en estado `PROCESSING`.
    *   **Plan:**
        *   Revisar la tarea Celery `assessment/tasks.py`.
        *   Inspeccionar los logs de Celery.
        *   Realizar una prueba de generación de evaluación monitorizando la BBDD y los logs.
