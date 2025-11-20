
# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Hoja de Ruta para la Próxima Sesión

**Objetivo Estratégico:** Finalización de UI y Estabilización del Admin.

**Estado Actual:**
El flujo principal ("Solicitar" -> "Generar" -> "Realizar" -> "Corregir" -> "Ver Resultados") está **100% funcional y verificado E2E**. Se han implementado correcciones críticas en la lógica de estados (backend), priorización de UI (frontend) y resiliencia de tareas (Celery).

**Tareas Pendientes (Backlog):**
1.  **UI Navbar:** El badge de notificación de evaluaciones en la barra de navegación no se actualiza correctamente o no aparece.
2.  **Admin Logs:** El visor de logs en el panel de administración presenta errores de visualización o enlace (`NoReverseMatch`).
3.  **Refinamiento Visual:** Pulir la consistencia de los badges entre diferentes vistas (lista vs detalle).

**Plan de Acción Inmediato:**
1.  Diagnosticar el renderizado del badge en `base.html` o el partial correspondiente de la navbar.
2.  Corregir las rutas `reverse` en el módulo de logs del Admin (`orchestrator`).

---

## Registro de Cambios (Sesión 20/11/2025)

### Correcciones Críticas
*   **Lógica de Estados (Tasks):** Se modificó `correct_assessment_task` en `orchestrator/tasks.py` para aceptar explícitamente el estado `AWAITING_CORRECTION`, evitando que las evaluaciones se quedaran en el limbo tras el envío.
*   **Persistencia de Fechas:** Se corrigió un bug en `tasks.py` donde `expiration_date` y `results_expiration_date` no se guardaban en la BD al finalizar las tareas, causando que la UI las ignorara.
*   **Prioridad de UI (Utils):** Se refactorizó `get_assessment_context` en `assessment/utils.py` para que el estado activo de una evaluación prevalezca sobre el mensaje de "Límites Alcanzados", desbloqueando el acceso al usuario.

### Mejoras de Resiliencia
*   **Manejo de Cuota API:** Se implementó un manejo robusto de la excepción `ResourceExhausted` en las tareas de evaluación, replicando la lógica de espera (60s) y cuarentena del generador de contenido.

### Infraestructura
*   **Admin Django:** Se reparó un error 500 en el admin de Evaluaciones corrigiendo los namespaces en `assessment/admin.py`.
*   **System Prompts:** Se actualizó el protocolo `PMA` para estandarizar el uso de "Python Patching" (scripts `.py` para aplicar cambios) en lugar de `sed`/`awk`, eliminando el protocolo obsoleto `PMP`.

