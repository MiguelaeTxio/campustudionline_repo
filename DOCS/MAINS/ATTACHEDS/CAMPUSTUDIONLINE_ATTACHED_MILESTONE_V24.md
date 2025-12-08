# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Estado:** **IMPLEMENTACIÓN DE RESILIENCIA COMPLETADA - PENDIENTE DE VERIFICACIÓN**

## Bitácora de Sesión (08/12/2025)
*   **Actividad:** Implementación de Modelo de Datos Blindado y Refactorización del Orquestador.
*   **Resumen de Implementación:**
    1.  **Modelos (`orchestrator/models.py`):**
        *   Se han añadido los campos de resiliencia (`global_actuation_count`, `consecutive_api_errors`, `last_api_error_at`, `last_error_api_key`, `current_step`, `last_heartbeat`) al modelo `PendingContentTask`.
        *   Se han añadido los umbrales de configuración (`max_task_actuations`, `max_consecutive_api_errors`, `zombie_task_threshold_hours`) al modelo `AutomationSettings` para permitir su ajuste desde el panel de administración.
    2.  **Migraciones:** Se ha estabilizado por completo el sistema de migraciones del proyecto, resolviendo conflictos históricos en las aplicaciones `contenttypes`, `auth`, `admin` y `sites`, y aplicando los nuevos cambios en `orchestrator`. El sistema se encuentra ahora en un estado consistente.
    3.  **Administración (`orchestrator/admin.py`):** Se ha corregido la interfaz de administración para `AutomationSettings`, asegurando que los nuevos parámetros de resiliencia sean visibles y editables, y solucionando errores de visualización del objeto.
    4.  **Tareas Celery (`orchestrator/tasks.py`):**
        *   Se ha refactorizado la tarea `generate_full_course_task` para utilizar los nuevos campos, implementando la lógica de fusible (`global_actuation_count`), reanudación de progreso (`current_step`) y gestión de errores de API basada en base de datos.
        *   Se ha diagnosticado y corregido un fallo crítico en `global_orchestrator_task` causado por un estado de objeto obsoleto en memoria. Se ha forzado la recarga del estado de la `active_api_key` desde la base de datos (`refresh_from_db()`) para garantizar que la lógica de rotación de claves funcione con datos reales.
*   **Diagnóstico Final:** A pesar de la implementación de múltiples correcciones lógicas y de estado, el sistema sigue sin operar como se esperaba, indicando un fallo subyacente que no ha sido resuelto.

## Hoja de Ruta (Siguiente Sesión)

### 1. ANÁLISIS FORENSE DE LOGS Y CÓDIGO
*   **Objetivo:** Determinar la causa raíz del fallo persistente del orquestador.
*   **Pasos:**
    1.  **Solicitud de Evidencia:** Solicitar el archivo de log de Celery (`/var/log/{username}_celery_worker.log`) y el código actual de `orchestrator/tasks.py`.
    2.  **Análisis Exhaustivo:** Realizar una auditoría cruzada entre los mensajes de error del log y el flujo de ejecución del código para identificar la discrepancia o el punto exacto del fallo.
    3.  **Hipótesis y Verificación:** Formular una hipótesis verificable basada en la evidencia y proponer un plan de acción empírico para confirmarla.
    4.  **Implementación de Corrección:** Una vez confirmada la causa raíz, implementar la solución definitiva.
