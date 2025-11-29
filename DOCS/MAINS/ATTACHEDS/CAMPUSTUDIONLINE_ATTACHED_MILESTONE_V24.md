# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Propósito:** Hito contenedor para tareas de depuración a demanda, resolución de dudas imprevistas y mantenimiento correctivo menor que no encaje en hitos específicos.
**Estado:** **PAUSADO**

## Bitácora de Sesión

### 28/11/2025 - Creación
*   **Acción:** Hito creado como punto de entrada para futuras sesiones de mantenimiento general.

### 29/11/2025 - Resolución de Incidencia Crítica de Base de Datos y Mejoras
*   **Incidencia:** Bloqueo inminente por exceso de cuota en MySQL (34.5 GB ocupados).
*   **Diagnóstico:** Fragmentación masiva ("ghost data") en `orchestrator_pendingcontenttask` debido a logs históricos no purgados.
*   **Solución Aplicada:**
    1.  Reconstrucción total de la tabla (`mysqldump` filtrado -> `DROP` -> `RELOAD`). **Espacio liberado: >32 GB**.
    2.  Implementación de parche de seguridad en `orchestrator/tasks.py` para truncar payloads JSON mayores a 2000 caracteres, previniendo recurrencia.
*   **Mejoras:**
    1.  Añadida plantilla de generación para la categoría **Botánica** en `CONTENT_PROMPTS.md`.
*   **Estado Final:** Sistema estable. Uso de disco normalizado (65% de cuota).

### 29/11/2025 - Registro de Incidencias Pendientes (Para Próxima Sesión)
*   **Incidencia Crítica (Admin Users):** Error 500 al intentar editar el usuario administrador (`/admin/users/customuser/1/change/`).
    *   **Error:** `django.core.exceptions.FieldError: Unknown field(s) (mostrar_degree_en_portafolio, ...) specified for UserProfile`.
    *   **Diagnóstico:** Desincronización entre `users/admin.py` y el modelo `UserProfile`. El admin intenta mostrar campos de visibilidad del portafolio que ya no existen con esos nombres en el modelo.
*   **Incidencia Secundaria (Template):** Error de sintaxis en `contents/personal_workspace.html`.
    *   **Error:** `TemplateSyntaxError: Invalid block tag on line 17: 'static'`.
    *   **Diagnóstico:** Falta cargar el tag (`{% load static %}`) o está mal cerrado un bloque en la plantilla.
