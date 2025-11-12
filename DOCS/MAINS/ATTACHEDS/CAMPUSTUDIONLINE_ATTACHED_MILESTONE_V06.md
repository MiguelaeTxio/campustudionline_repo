# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 12/11/2025 (MAMC)

**Objetivo:** Implementar un sistema de resiliencia para el módulo de autoevaluaciones, eliminando el estado `FAILED` y añadiendo un mecanismo de reintentos automáticos para las tareas Celery, similar al del módulo `content_automation`.

**Desarrollo y Solución Empírica:**
La implementación se realizó de forma atómica y auditada, abordando los siguientes puntos:
1.  **Refactorización del Modelo:** Se modificó `assessment/models.py`, reemplazando los estados de fallo genéricos por `FAILED_RETRYABLE` y `FAILED_FATAL`, y se añadió un campo `last_error` para el registro de trazas.
2.  **Implementación de Resiliencia en Tareas:** Se refactorizaron las tareas en `assessment/tasks.py`, aplicando el patrón de resiliencia con `bind=True`, `acks_late=True` y lógica de reintentos `self.retry()` ante excepciones.
3.  **Corrección de Errores Empírica:**
    *   Se diagnosticó y solucionó un `OperationalError` (columna desconocida) mediante la generación y aplicación de la migración de base de datos omitida.
    *   Se diagnosticó y solucionó un `AttributeError` posterior mediante el uso de `grep` para localizar y corregir todas las referencias obsoletas al antiguo estado `FAILED` en `contents/study_room_views.py` y `assessment/utils.py`.
4.  **Ajuste de la Interfaz de Usuario:** Se actualizaron `core/context_processors.py` y la plantilla `_assessment_legend.html` para eliminar las referencias visuales al estado de fallo y reasignar los iconos, alineando la UI con la nueva lógica del backend.

**Estado Final:** El sistema de autoevaluaciones es ahora más robusto y resiliente ante fallos de la API. Las regresiones introducidas durante el proceso han sido identificadas y corregidas de manera metódica.

## Hoja de Ruta para la Próxima Sesión

1.  **Diagnóstico y Corrección de Caducidad de Resultados:**
    *   **Problema:** Se ha detectado una contradicción visual y funcional: el panel de la Sala de Estudio muestra un temporizador de expiración para los resultados de una autoevaluación, pero al acceder a ellos, un mensaje indica que "la corrección para esta respuesta ha caducado y ha sido eliminada".
    *   **Hipótesis:** La tarea periódica `purge_and_penalize_corrections` o la lógica de visualización en las plantillas/vistas está actuando de forma prematura o incorrecta, creando una inconsistencia entre la fecha de expiración (`results_expiration_date`) y el estado real de los datos.
    *   **Plan de Acción Empírico:**
        1.  Auditar la lógica de la tarea `purge_and_penalize_corrections` en `assessment/tasks.py`.
        2.  Revisar el modelo `UserAnswer` para entender cómo se purgan los campos `score` y `feedback`.
        3.  Analizar la vista `view_results` y la plantilla correspondiente para verificar cómo se renderiza el mensaje de caducidad.
        4.  Proponer una solución atómica que garantice que el estado visualizado al usuario sea coherente en todo el flujo.
