
# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Hoja de Ruta para la Próxima Sesión

**Objetivo Estratégico:** Unificación de la UI y Visibilidad del Admin.

**Estado Actual (Análisis "Tour Fotográfico"):**

1.  **Backend (SOLUCIONADO):**
    *   **Atomicidad:** Se ha erradicado la condición de carrera que permitía evaluaciones duplicadas mediante `select_for_update` y transacciones atómicas.
    *   **Flujo No-Bloqueante:** Se ha eliminado la lógica `404` defensiva. El sistema ahora gestiona la no existencia de objetos con redirecciones fluidas y mensajes al usuario.
    *   **Resiliencia:** El sistema gestiona correctamente la cuota de API (`ResourceExhausted`), reintentando o poniendo en cuarentena sin romper la ejecución.
    *   **Persistencia:** Las fechas de expiración se guardan correctamente.

2.  **Frontend (INCONSISTENTE - DEUDA TÉCNICA):**
    *   **NavBar:** ✅ Muestra correctamente el badge y el contador. Desaparece al ver los resultados.
    *   **Lista de Copias:** ❌ "Muda". No muestra el estado de la evaluación (badge amarillo/azul/verde) en los ítems de la lista.
    *   **Sidebar (Menú Lateral):** ❌ Incoherente. Muestra contadores genéricos ("1") sin contexto de estado y puntos rojos desalineados con la lógica central.
    *   **Tarjetas de Actividad Reciente:** ❌ "Mudas". Botones genéricos "Estudiar" sin indicación de que hay una evaluación en curso o lista.
    *   **Explorador:** ❌ Va por libre, mostrando iconos sin leyenda.

3.  **Administración (PARCIAL):**
    *   **Panel:** ✅ Funcional (Error 500 corregido).
    *   **Logs:** ❌ "Mudos". El detalle de la tarea de evaluación muestra "No hay eventos registrados". Falta implementar la escritura de logs en el modelo `Assessment`.

**Plan de Acción Inmediato:**
1.  **Backend (Logs):** Implementar campo `event_log` en modelo `Assessment` y conectar las tareas de Celery para escribir en él.
2.  **Frontend (Lista/Tarjetas):** Depurar la anotación de querysets (`annotate_content_copy_queryset_with_assessment_states`) para asegurar que el estado llega a la plantilla y renderizar los badges correspondientes.
3.  **Frontend (Sidebar):** Refactorizar la lógica del menú lateral para que consuma la misma "verdad única" que la NavBar.

---

## Registro de Cambios (Sesión 20/11/2025)

### Correcciones Críticas de Backend
*   **Eliminación de Race Condition:** Implementación de `transaction.atomic` y bloqueo de fila en `views.py`.
*   **Eliminación de get_object_or_404:** Refactorización completa de `assessment/views.py` para manejo de errores no destructivo.
*   **Resiliencia y Persistencia:** Actualización de `orchestrator/tasks.py` para manejo de cuotas y guardado de fechas.

### Infraestructura
*   **System Prompts:** Actualización del protocolo `PMA` (Python Patching) y eliminación de `PMP`.
*   **Admin:** Corrección de namespaces en `assessment/admin.py`.

