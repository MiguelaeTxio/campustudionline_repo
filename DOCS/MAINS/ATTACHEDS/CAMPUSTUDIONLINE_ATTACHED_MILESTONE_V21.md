# Hito 21: Refactorización del Orquestador de Tareas Asíncronas y Resiliencia del Sistema (EN PROGRESO)

## Visión General y Justificación

Durante la depuración del Hito 6, se ha detectado una debilidad arquitectónica fundamental en la gestión de tareas asíncronas de la aplicación `assessment`. A diferencia del sistema resiliente de `content_automation`, `assessment` carece de un mecanismo de orquestación centralizado, lo que provoca que los fallos de la API se expongan al usuario final y no se gestionen de forma automática.

Este hito tiene como objetivo solucionar esta deuda técnica mediante una refactorización estratégica que centralizará toda la lógica de orquestación de tareas de fondo en una nueva aplicación dedicada, `orchestrator`. Esta refactorización no solo solucionará los problemas de resiliencia de `assessment`, sino que establecerá una base arquitectónica robusta y escalable para futuras automatizaciones y la gestión centralizada de recursos críticos como las `API Keys`.

## Hoja de Ruta para la Próxima Sesión

La sesión comenzará con la implementación de la nueva arquitectura de orquestación. Los pasos a seguir son:

1.  **Crear la nueva aplicación `orchestrator`** y añadirla a `INSTALLED_APPS`.
2.  **Mover los modelos `ApiKey` y `AutomationSettings`** de `content_automation` a `orchestrator`, generando y aplicando las migraciones correspondientes.
3.  **Crear `orchestrator/tasks.py`** y migrar la lógica de `automation_main_loop_task` a una nueva tarea centralizada: `global_orchestrator_task`.
4.  **Actualizar la configuración de Celery Beat** para que apunte a la nueva tarea `global_orchestrator_task`.
5.  **Ampliar `global_orchestrator_task`** para que también gestione el rescate y re-encolado de tareas fallidas de la aplicación `assessment`.
6.  **Refactorizar `assessment/models.py` y `assessment/tasks.py`** para que adopten el nuevo sistema de estados y deleguen la lógica de reintentos al orquestador.
