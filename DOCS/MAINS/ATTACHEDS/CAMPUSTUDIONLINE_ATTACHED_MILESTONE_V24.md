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

## Bitácora de Sesión (10/12/2025)
*   **Logro Crítico:** Implementación exitosa del **Bucle de Resistencia Local** en el Orquestador (`orchestrator/tasks.py`).
*   **Problema Solucionado:**
    *   El sistema reiniciaba las tareas completas ante errores de cuota (API) o micro-cortes de red (DB), disparando el fusible de seguridad (`global_actuation_count`) y generando bucles de `OSError` con el broker de Celery.
*   **Solución Técnica ("Blindaje Total"):**
    *   **Contención Local:** Se encapsularon las llamadas a la API (tanto en fase de inicialización como de generación) dentro de bucles `while True` con captura de excepciones `try/except` interna.
    *   **Efecto:** La tarea nunca "muere" por un error transitorio. En su lugar, entra en suspensión (`sleep`) o rota la clave dentro del mismo proceso, manteniendo el contexto y evitando el tráfico innecesario con Redis.
    *   **Corrección de Bugs:** Se solucionó un `TypeError` crítico en el log de finalización y se añadió persistencia de fallos en el modelo `ApiKey`.
*   **Validación:** La tarea compleja 'Iconografía' (80 secciones) se completó exitosamente tras sobrevivir a 3 rotaciones de clave y múltiples esperas, validando la resiliencia del nuevo diseño.

## Hoja de Ruta (Siguientes Pasos)
### 1. MONITORIZACIÓN DE ESTABILIDAD
*   Vigilar el comportamiento del orquestador con la cola de tareas llena.
*   Confirmar que el contador de fusibles (`global_actuation_count`) se mantiene bajo control.

### 2. MANTENIMIENTO CORRECTIVO
*   Resolver cualquier incidencia puntual que surja en la generación masiva ahora que el motor principal funciona.
