# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Propósito:** Hito contenedor para tareas de depuración a demanda, resolución de dudas imprevistas y mantenimiento correctivo menor que no encaje en hitos específicos.
**Estado:** **EN PROGRESO**

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

### 30/11/2025 - Reparación Integral de Admin y Flujo de Registro
*   **Corrección Admin Users:** Solucionado error 500 en `/admin/users/customuser/` actualizando `users/admin.py` para usar los nombres de campo correctos (`show_*` en lugar de `mostrar_*`).
*   **Corrección Plantilla Personal Workspace:** Subsanado error de sintaxis en `contents/templates/contents/personal_workspace.html`.
*   **Recuperación Crítica de `register.html`:** El archivo `users/templates/users/register.html` estaba vacío debido a un error en la migración de repositorios. Se recuperó la versión funcional del 24 de Agosto desde el historial del repositorio antiguo y se modernizó (namespaces `users:`).
*   **Blindaje del Sistema de Tokens:**
    *   Implementado `AccountActivationTokenGenerator` robusto en `users/tokens.py` (hash basado en `pk + timestamp + is_active`, ignorando cambios volátiles como password).
    *   Corregida lógica en `users/views.py` para usar el nuevo generador y evitar errores en flujos de reactivación.
    *   Solucionado error en redirección de reactivación que pasaba el token incorrecto a la vista de cambio de contraseña.
*   **Mejoras UX Móvil (Registro):**
    *   Reposicionada la barra de fortaleza de contraseña encima del input.
    *   Reposicionados los mensajes de error (ej: "contraseñas no coinciden") encima de los campos para evitar ocultamiento por el teclado virtual.

## Tareas Pendientes (Próxima Sesión)
*   **Optimización "Mis Publicaciones":** Implementar paginación para evitar sobrecarga y crash en la vista de lista plana.
*   **Limpieza UI:** Eliminar la leyenda "No hay subcarpetas para mostrar" en vistas que no disponen de árbol de directorios.
