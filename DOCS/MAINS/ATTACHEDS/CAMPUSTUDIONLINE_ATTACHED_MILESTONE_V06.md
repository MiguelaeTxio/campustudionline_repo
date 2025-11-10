# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 10/11/2025 (CSO-DGF-IA)

**Objetivos:** Diagnosticar y corregir el fallo inmediato en la generación de evaluaciones y la disrupción en el sistema de prioridades de tareas asíncronas.

**Progreso y Descubrimientos Clave:**

1.  **Diagnóstico de Fallo en Cascada:** Se identificó una cadena de fallos críticos. El problema inicial no era un simple error de lógica, sino un fallo total en la inicialización del worker de Celery en el entorno de la tarea `always-on` de PythonAnywhere.
2.  **Causa Raíz - Proliferación de Procesos:** La investigación empírica demostró que el comando del worker, al incluir el scheduler (`-B`) y usar el pool `prefork` por defecto, entraba en conflicto con el entorno de la tarea `always-on`, provocando una proliferación incontrolada de procesos huérfanos que bloqueaban cualquier nuevo inicio.
3.  **Solución de Estabilidad (Concurrencia):** Se solucionó el problema de raíz forzando a Celery a operar en un único proceso mediante la directiva `CELERY_WORKER_CONCURRENCY = 1` en `core/settings.py`.
4.  **Corrección de Errores Secundarios:** Durante el proceso se corrigió un `TypeError` en la configuración de `TEMPLATES` y se restauró la lógica de prioridades de las colas de Celery, tanto en `settings.py` (`CELERY_BEAT_SCHEDULE`) como en el comando de la tarea `always-on`.
5.  **Inicio del Refactor Arquitectónico:** Con el sistema estable, se inició el refactor para encapsular las evaluaciones. Se completó la Fase 1, modificando el modelo `assessment.models.Assessment` para que la `ContentCopy` sea la única fuente de verdad, preparando el terreno para las migraciones y la refactorización de la lógica de negocio.

**Estado Final:** El sistema de tareas asíncronas vuelve a ser estable y funcional, con la lógica de prioridades restaurada. El refactor arquitectónico del sistema de evaluaciones ha comenzado con éxito.

## Hoja de Ruta para la Próxima Sesión

1.  **Generar y Aplicar Migraciones:** El primer paso será generar el archivo de migración para los cambios realizados en `assessment/models.py` y aplicarlo a la base de datos.
2.  **Fase 2 del Refactor - Lógica de la Tarea:** Modificar la tarea `generate_assessment_from_content_task` en `assessment/tasks.py` para que obtenga el contenido y las asignaturas asociadas a través de `assessment.content_copy`, eliminando toda dependencia directa de `assessment.content`.
3.  **Fase 3 del Refactor - Lógica de las Vistas:** Auditar `assessment/views.py` para asegurar que la creación y gestión de las evaluaciones se alinea completamente con la nueva arquitectura centrada en `ContentCopy`.
4.  **Refinamiento de UX/UI (Badges):** Abordar la mejora de la experiencia de usuario de los `badges` de estado de la evaluación, centralizándolos exclusivamente en la vista de la Sala de Estudio (`edit_copy.html`).

