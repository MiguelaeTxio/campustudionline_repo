# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 17/11/2025 (PCS - EXITOSA)

**Objetivo Estratégico Alcanzado:** Se ha diagnosticado y resuelto una migración incompleta de la arquitectura de tareas asíncronas, unificando toda la lógica en el módulo `orchestrator` y resolviendo los conflictos que impedían el procesamiento de las evaluaciones.

**Desarrollo y Solución:**

1.  **Diagnóstico del Problema de Prioridad:** Se identificó que las tareas de `assessment` no se ejecutaban debido a una lógica de priorización incorrecta en el `global_orchestrator_task` y a una dependencia obsoleta de un interruptor de motor (`is_running`) específico de la app `assessment`.

2.  **Consolidación de la Lógica de Tareas:**
    *   Se migró toda la lógica de `content_automation/tasks.py` y `assessment/tasks.py` al archivo centralizado `orchestrator/tasks.py`.
    *   Se eliminaron los archivos de tareas obsoletos para prevenir conflictos.

3.  **Actualización de Referencias y Configuración:**
    *   Se corrigieron todas las importaciones en las vistas (`views.py`) y paneles de administración (`admin.py`) que llamaban a las tareas migradas.
    *   Se actualizó la configuración estática de `CELERY_BEAT_SCHEDULE` en `core/settings.py` para que todas las tareas periódicas apunten al módulo `orchestrator`.

4.  **Unificación del Interruptor Maestro:**
    *   Se eliminó la dependencia del interruptor `is_running` de `AssessmentSettings`, haciendo que todas las tareas asíncronas (contenido y evaluaciones) obedezcan al interruptor global y único en `AutomationSettings`.

5.  **Corrección de Bug de Estado (`AttributeError`):**
    *   Se resolvió un `AttributeError` en la tarea `generate_assessment_from_content_task` añadiendo una llamada a `assessment.refresh_from_db()` para asegurar que el objeto en memoria estuviera sincronizado con la base de datos antes de leer el campo `last_error`.

**Estado Actual:** La arquitectura de tareas está completamente centralizada y funcional. El orquestador global ahora procesa correctamente la cola de trabajo según la prioridad definida. Sin embargo, se ha detectado que las tareas de generación de `assessment`, aunque se inician, no finalizan. El último log indica que la tarea se omite con el mensaje `'Tarea omitida. Estado actual: Generando Cuestionario.'`, sugiriendo un posible problema de concurrencia o de gestión de estados.

## Hoja de Ruta para la Próxima Sesión (Estabilización de `assessment`)

**Objetivo Estratégico:** Diagnosticar y resolver la causa por la cual la tarea `generate_assessment_from_content_task` no completa su ejecución, quedando en un estado de "reintento" o siendo omitida.

**Plan de Acción Atómico:**

1.  **Auditoría de la Lógica de Estado:** Revisar la tarea `generate_assessment_from_content_task` en `orchestrator/tasks.py` para analizar las condiciones de entrada y las transiciones de estado (`status`) del modelo `Assessment`.
2.  **Análisis Empírico de Logs:** Examinar en detalle los logs del `worker` de Celery para rastrear el ciclo de vida completo de una tarea de `assessment` desde que es encolada hasta que es omitida, buscando el punto exacto donde la lógica diverge del comportamiento esperado.
3.  **Verificación en Base de Datos:** Consultar directamente el estado del objeto `Assessment` en la base de datos durante el ciclo de vida de la tarea para verificar si los cambios de estado se persisten correctamente y si coinciden con lo que la tarea espera encontrar.
