# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Estado:** **PLANIFICACIÓN DE RESILIENCIA COMPLETADA**

## Bitácora de Sesión (08/12/2025)
*   **Actividad:** Auditoría Forense y Análisis Arquitectónico (Sesión de Análisis Lógico).
*   **Diagnóstico Final:**
    *   **Fallo de Disco Lleno:** Causado por bucles infinitos en tareas sin un límite duro de "intentos de arranque" persistente (`global_actuation_count`).
    *   **Muerte de API Keys:** Causada por una lógica de "rencor acumulativo" que sumaba errores antiguos a los nuevos tras reintentos largos, sin contexto temporal (`last_api_error_at`) y sin distinguir qué clave falló (`last_error_api_key`).
    *   **Zombies/Silent Crashes:** Tareas que mueren por reinicios (se va la luz) y quedan en `PROCESSING` sin dejar rastro, o se reinician eternamente porque el contador de reintentos en memoria de Celery se pierde.
*   **Solución Definida:** Reingeniería del modelo de datos `PendingContentTask` para dotarlo de memoria y contexto, implementando "Write-Ahead Logging" y abandonando la lógica ingenua de `sleeps` y contadores en JSON.

## Hoja de Ruta (Siguiente Sesión)

### 1. IMPLEMENTACIÓN DEL MODELO DE DATOS BLINDADO
*   **Objetivo:** Modificar `orchestrator/models.py` para incluir los nuevos campos de control.
*   **Nuevos Campos:**
    1.  `global_actuation_count` (Integer): Fusible físico. Se incrementa al *inicio* de la ejecución (Write-Ahead). Si > 20, abortar.
    2.  `consecutive_api_errors` (Integer): Contador de strikes explícito y atómico.
    3.  `last_api_error_at` (DateTime): Para aplicar "amnistía" a errores viejos (ej: >5min).
    4.  `last_error_api_key` (FK): Para no heredar culpas de claves anteriores.
    5.  `current_step` (Integer): Puntero de progreso para reanudación precisa.
    6.  `last_heartbeat` (DateTime): Para detectar y purgar tareas muertas ("Silent Crashes").

### 2. REFACTORIZACIÓN DEL ORQUESTADOR
*   **Objetivo:** Reescribir `orchestrator/tasks.py` para usar la nueva lógica.
*   **Lógica Clave:**
    *   Incrementar `global_actuation_count` antes de cualquier operación.
    *   Actualizar `last_heartbeat` en cada paso de generación.
    *   Lógica de "Amnistía" para resetear `consecutive_api_errors` basada en `last_api_error_at`.

