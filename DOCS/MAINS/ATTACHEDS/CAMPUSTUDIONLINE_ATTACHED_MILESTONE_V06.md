# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Hoja de Ruta para la Próxima Sesión (REPARACIÓN URGENTE)

**Estado de la Prueba E2E (23/11/2025):** 🔴 **FALLIDO**

**Diagnóstico Detallado (Tour Fotográfico):**

1.  **Log de Admin (CRÍTICO - MUDO):**
    *   **Síntoma:** El log del modelo `Assessment` aparece vacío ("No hay eventos registrados") en el panel de administración.
    *   **Causa Probable:** Las tareas de Celery no están persistiendo correctamente los eventos en el campo `event_log` (Fallo de Transacción/Silenciamiento).
    *   **Nueva Requisito:** El log debe ser granular, mostrando el progreso pregunta por pregunta.

2.  **Navegación (Sidebar y NavBar - INCOHERENTES):**
    *   **Síntoma:** Desincronización total. El Sidebar muestra contadores genéricos y la NavBar estados desactualizados.
    *   **Causa Probable:** La señal `post_save` no está disparando `refresh_user_navigation` correctamente.

3.  **Puntos Positivos:**
    *   La lista de copias y el detalle funcionan y muestran los badges correctos.

**Plan de Acción Inmediato:**
1.  **Backend (Logs):** Auditar el punto de fallo final para la persistencia del log (hipótesis: fallo transaccional anidado o conflicto de bloqueo).
2.  **Backend (Logs Granulares):** Aplicar y validar la instrumentación de logs detallados en `orchestrator/tasks.py`.
3.  **Backend (Navegación):** Auditar la lógica de `transaction.on_commit` para asegurar que se ejecuta y que el constructor de navegación ve los datos actualizados.
4.  **Validación:** Repetir prueba E2E.

---

## Registro de Cambios (Sesión Previa)

### Correcciones Implementadas
*   **Modelo (`assessment/models.py`):** Eliminación de la supresión de errores (`try...except: pass`) en `add_log_event`.
*   **Señales (`assessment/signals.py`):** Implementado `transaction.on_commit` para `refresh_user_navigation`.
*   **Tareas (`orchestrator/tasks.py`):** Implementada la instrumentación de logs granulares. (Pendiente de confirmación de persistencia).
