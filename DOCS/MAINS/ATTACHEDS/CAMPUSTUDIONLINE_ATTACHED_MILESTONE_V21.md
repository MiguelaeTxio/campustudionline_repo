# Hito 21: Refactorización del Orquestador de Tareas Asíncronas (EN PROGRESO)

## Resumen de la Sesión del 18/11/2025 (PCS)

**Objetivo Estratégico:** Completar la refactorización del orquestador moviendo todas las dependencias lógicas desde `content_automation` y estabilizando la base de datos.

**Desarrollo y Hallazgos:**
Se ha ejecutado una refactorización exhaustiva del orquestador de tareas. Siguiendo un método empírico guiado por los errores de la aplicación, se han movido con éxito los `models`, `forms`, `admin_views` y `admin_urls` de la aplicación `content_automation` a `orchestrator`. Se resolvieron múltiples `ImportError`, `ModuleNotFoundError` y conflictos de migración de base de datos a través de una resincronización forzada en varias fases. La estructura del código y de la base de datos es ahora coherente. La corrección final de una referencia obsoleta en la plantilla `templates/admin/base_site.html` fue propuesta pero denegada, quedando como único punto pendiente.

**Estado Actual:** La refactorización está completa a nivel de código Python y de base de datos. Queda pendiente un único ajuste en una plantilla para resolver un error de renderizado.

## Hoja de Ruta para la Próxima Sesión (Finalización)

**Objetivo Estratégico:** Corregir la última referencia obsoleta para dar por finalizado el Hito 21.

**Plan de Acción Atómico:**
1.  Iniciar la sesión.
2.  Solicitar el archivo `templates/admin/base_site.html`.
3.  Ejecutar un `PMA` para corregir la etiqueta `{% url %}` que apunta al `namespace` obsoleto `content_automation_admin`, cambiándolo por `orchestrator`.
4.  Realizar el protocolo de verificación final End-to-End.
