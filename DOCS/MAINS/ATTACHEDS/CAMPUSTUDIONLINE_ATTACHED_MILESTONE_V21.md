# Hito 21: Refactorización del Orquestador de Tareas Asíncronas y Resiliencia del Sistema (EN PROGRESO)

## Visión General y Justificación

Durante la depuración del Hito 6, se ha detectado una debilidad arquitectónica fundamental en la gestión de tareas asíncronas de la aplicación `assessment`. A diferencia del sistema resiliente de `content_automation`, `assessment` carece de un mecanismo de orquestación centralizado, lo que provoca que los fallos de la API se expongan al usuario final y no se gestionen de forma automática.

Este hito tiene como objetivo solucionar esta deuda técnica mediante una refactorización estratégica que centralizará toda la lógica de orquestación de tareas de fondo en una nueva aplicación dedicada, `orchestrator`.

## Resumen de la Sesión Actual

*   Se creó la aplicación `orchestrator`.
*   Se movieron los modelos `ApiKey` y `AutomationSettings` de `content_automation` a `orchestrator`.
*   Se generaron y modificaron manualmente las migraciones para mover los modelos de forma segura, preservando los datos existentes.
*   Se migró la lógica de la tarea `automation_main_loop_task` a `orchestrator.tasks.global_orchestrator_task`.
*   Se actualizó la configuración de Celery Beat en `settings.py` para apuntar a la nueva tarea del orquestador.
*   Se amplió `global_orchestrator_task` para incluir la lógica de rescate de tareas de `assessment` fallidas.
*   Se inició la refactorización de la app `assessment`. **Se detuvo el proceso** tras detectar un error de diseño en la propuesta de modificación del modelo `Assessment` (eliminación incorrecta de estados de fallo) y una posterior violación de PEP8 en la propuesta de corrección.

## Hoja de Ruta para la Próxima Sesión

La sesión se reanudará en el punto de interrupción, con el objetivo de completar la refactorización de la aplicación `assessment`.

1.  **Corregir el error de diseño:** La primera acción será proponer una modificación correcta para `assessment/models.py`. Esta modificación **DEBE** preservar los estados `GENERATION_FAILED_RETRYABLE` y `CORRECTION_FAILED_RETRYABLE`, ya que son los que el orquestador utiliza para identificar las tareas que necesita rescatar.
2.  **Generar la migración:** Una vez modificado el modelo, se generará una nueva migración para `assessment` si fuera necesario.
3.  **Refactorizar `assessment/tasks.py`:** Se modificará el archivo para eliminar la lógica de reintentos (`self.retry()`) en la gestión de errores de API. La tarea debe simplemente fallar, estableciendo el estado del `Assessment` a `..._FAILED_RETRYABLE` para que el orquestador pueda detectarlo y actuar.
4.  **Verificación Final:** Realizar una revisión general y aplicar las migraciones pendientes antes de finalizar la implementación.
