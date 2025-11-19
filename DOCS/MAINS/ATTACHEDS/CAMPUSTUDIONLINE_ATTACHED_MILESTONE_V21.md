# Hito 21: Refactorización del Orquestador de Tareas Asíncronas (EN PROGRESO)

## Resumen de la Sesión del 19/11/2025 (PCS)

**Objetivo Estratégico:** Completar la refactorización del orquestador moviendo todas las dependencias lógicas desde `content_automation`, estabilizando la base de datos y restaurando la funcionalidad completa.

**Desarrollo y Hallazgos:**
La sesión se centró en una depuración exhaustiva y metódica de múltiples capas del sistema:

1.  **Estabilización de la Base de Datos:** Se diagnosticó y reparó una inconsistencia severa en el esquema de la base de datos causada por una migración parcialmente aplicada. La reparación implicó la creación manual de tablas SQL faltantes (`orchestrator_pendingcontenttask`, `orchestrator_contentrequest`, etc.) y la resincronización forzada del historial de migraciones de Django.

2.  **Estabilización del Sistema de Tareas (Celery):** Se diagnosticó y resolvió un error crítico de conexión a la base de datos (`Unknown MySQL server host`) que afectaba a los procesos de Celery. La causa raíz, identificada empíricamente a través de los logs, fue el uso del intérprete de Python incorrecto en la "Always-on task" de PythonAnywhere. El problema se solucionó corrigiendo el comando de ejecución para usar la ruta absoluta al intérprete del entorno virtual, estabilizando por completo el sistema de tareas asíncronas.

3.  **Refactorización de Vistas y Plantillas:** Se continuó con la refactorización a nivel de aplicación. Se movieron las plantillas de `content_automation` a `orchestrator`. Se corrigieron errores `NoReverseMatch` actualizando la configuración de `core/urls.py` y los `namespaces` en las plantillas (`dashboard.html`, `automation_control_center.html`, y plantillas parciales). Se implementó la lógica para las vistas `automation_control_view` y `get_automation_status_view`, eliminando los `Placeholders` iniciales.

**Estado Actual:**
El sistema es estable. La base de datos es coherente, el sistema de tareas Celery es funcional y las vistas principales del panel de administración del orquestador cargan sin errores críticos. Sin embargo, la refactorización funcional **no está completa**. Múltiples vistas secundarias dentro del "Centro de Control de Automatización" (ej. `create_academic_task`, `manage_logs`) permanecen como `Placeholders` no implementados, lo que impide el uso completo de la funcionalidad.

## Hoja de Ruta para la Próxima Sesión

**Objetivo Estratégico:** Completar la implementación de las vistas refactorizadas del orquestador hasta restaurar el 100% de la funcionalidad.

**Plan de Acción Atómico:**
1.  Iniciar la sesión y verificar la estabilidad del sistema.
2.  Proceder con la implementación de la siguiente vista `Placeholder` en `orchestrator/admin_views.py`, siguiendo la secuencia lógica de la interfaz de usuario.
3.  Repetir el ciclo de `PMA` para la vista y su plantilla correspondiente (si la tuviera) hasta que todas las funciones del "Centro de Control de Automatización" sean operativas.
