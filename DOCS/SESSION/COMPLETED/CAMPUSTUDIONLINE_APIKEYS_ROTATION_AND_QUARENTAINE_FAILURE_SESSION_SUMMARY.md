# Sumario de Sesión Temporal: APIKEYS_ROTATION_AND_QUARENTAINE_FAILURE

## Diagnóstico

Se identificaron dos causas raíz interrelacionadas para el fallo del sistema de automatización:

1.  **Conflicto de Responsabilidades Arquitectónico:** La capa de servicio (`core/services/gemini_service.py`) gestionaba de forma autónoma la selección y cuarentena de `API Keys`, ignorando el estado global definido en `AutomationSettings` y entrando en conflicto con la lógica de orquestación de la capa de tareas (`content_automation/tasks.py`). Esto provocaba que el sistema se detuviera al encontrar una clave en cuarentena en el estado global, aunque existieran otras válidas.
2.  **Ruta de Worker Obsoleta:** El comando de inicio del worker de Celery en las "Always-on tasks" de PythonAnywhere apuntaba a un `working_directory` incorrecto (`/home/MiguelAeTxio/CampuStudiOnline`) tras la refactorización de la estructura de directorios del proyecto, impidiendo que el worker se iniciara.

## Solución Implementada

La solución se ejecutó en dos fases, restaurando la coherencia arquitectónica y corrigiendo la configuración del entorno:

1.  **Refactorización del Servicio (`gemini_service.py`):** Se modificó el servicio para convertirlo en un componente "sin estado" (stateless). Ahora requiere que la `ApiKey` a utilizar sea pasada explícitamente como parámetro y propaga las excepciones de cuota (`ResourceExhausted`) a la capa superior en lugar de manejarlas internamente.
2.  **Adaptación de la Tarea (`tasks.py`):** Se ajustó la tarea Celery `generate_full_course_task` para que pase el objeto `ApiKey` (obtenido del estado global `AutomationSettings`) al servicio. La lógica de captura de excepciones y rotación de claves (`_rotate_to_next_active_key`) ahora funciona como la única fuente de verdad para la gestión del ciclo de vida de las claves.
3.  **Corrección de la Tarea Programada:** Se proporcionó al usuario el comando corregido para la "Always-on task" de Celery, actualizando el `working_directory` a la nueva ruta `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline`.

Esta intervención ha centralizado la gestión de estado, resuelto el conflicto de capas y asegurado que el entorno de ejecución sea el correcto, restaurando la funcionalidad y resiliencia del sistema de automatización.
