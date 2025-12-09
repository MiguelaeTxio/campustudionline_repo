# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Estado:** **EN REINGENIERÍA - DEFECTO LÓGICO EN ROTACIÓN DE CLAVES DETECTADO**

## Bitácora de Sesión (09/12/2025)
*   **Actividad:** Depuración Profunda del Orquestador (Celery) y Lógica de Reintentos.
*   **Correcciones Implementadas (`orchestrator/tasks.py`):**
    1.  **Corrección de Silenciamiento de Excepciones:** Se solucionó el bug donde `self.retry()` era capturado por un bloque `except` genérico, matando la tarea en lugar de hibernarla.
    2.  **Fusible Global (Circuit Breaker):** Se activó la protección contra bucles de reinicio (`global_actuation_count`), abortando tareas que superan los 20 arranques fallidos.
    3.  **Hot-Swap (Rotación en Caliente):** Se implementó el cambio inmediato de clave ante error de cuota.
*   **Fallo de Diseño Identificado (Ping-Pong de Claves Agotadas):**
    *   La implementación actual del Hot-Swap rota la clave ante el *primer* fallo.
    *   **Consecuencia Crítica:** Al rotar inmediatamente, la clave fallida nunca acumula los 4 errores consecutivos necesarios para entrar en Cuarentena.
    *   **Resultado:** Las claves agotadas regresan al pool marcadas como "Activas", provocando que el sistema las vuelva a elegir y falle repetidamente, impidiendo que el mecanismo de Cuarentena limpie el pool de recursos inservibles.

## Hoja de Ruta (Siguiente Sesión)

### 1. CORRECCIÓN DEL MECISMO DE CUARENTENA
*   **Objetivo:** Asegurar que las claves agotadas sean marcadas como tal antes de ser rotadas.
*   **Acciones:**
    1.  Modificar la lógica de `tasks.py` para que los errores de cuota se registren persistentemente en el modelo `ApiKey` (o en un contador asociado) antes de realizar el Hot-Swap.
    2.  Garantizar que una clave solo se libere al pool si realmente funciona, y que se ponga en Cuarentena si falla, independientemente de si rotamos a otra o no.

### 2. VERIFICACIÓN DE ESTABILIDAD
*   Monitorizar que las claves agotadas pasen a estado `IS_QUARANTINED = True` automáticamente.
