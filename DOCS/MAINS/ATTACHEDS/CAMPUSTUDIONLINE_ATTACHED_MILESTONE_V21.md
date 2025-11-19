# Hito 21: Refactorización del Orquestador de Tareas Asíncronas (EN PROGRESO)

## Resumen de la Sesión del 19/11/2025 (PCS)

**Objetivo Estratégico:** Recuperar el acceso al Dashboard de Administración del Orquestador y verificar el flujo.

**Desarrollo y Hallazgos:**
1.  **Corrección de Namespaces (`orchestrator`):** Se aplicaron correcciones mediante `PMA` en `_task_row.html` y `task_log_full_page.html`. Se reemplazaron las referencias obsoletas `content_automation:` por `orchestrator:`, eliminando el error `NoReverseMatch` (Error 500).
2.  **Restauración del Dashboard:** El panel de administración vuelve a ser accesible.
3.  **Verificación de Generación:** El usuario confirma que la generación de contenido ha vuelto a funcionar ("Por fin ha vuelto a funcionar").
4.  **Nuevo Incidente (Logs Invisibles):** Aunque la tarea se procesa, el visor de logs (`task_log_full_page.html`) muestra "No se encontraron eventos de log para esta tarea", a pesar de que el sistema está trabajando. Esto sugiere que los eventos no se están persistiendo correctamente en el campo `task_log` del modelo o la plantilla no los está iterando correctamente tras la refactorización.

**Estado Actual:**
Backend funcional (Generación OK). Frontend de Administración accesible pero con **ceguera de logs**.

## Hoja de Ruta para la Próxima Sesión

**Objetivo Inmediato:** Reparar la visibilidad de los Logs de Tarea en el Dashboard.

**Plan de Acción Atómico:**
1.  **Diagnóstico de Persistencia de Logs:** Auditar `orchestrator/tasks.py` y el método de logging en `orchestrator/models.py` para confirmar si los logs se escriben en el JSONField `task_log` o solo en archivo físico.
2.  **Corrección de Visualización:** Asegurar que la plantilla `task_log_full_page.html` itera sobre la fuente de datos correcta.
3.  **Verificación Final:** Ejecutar una tarea y confirmar que los pasos aparecen en tiempo real (o al refrescar) en el visor de logs.
