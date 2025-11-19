# Hito 21: Refactorización del Orquestador de Tareas Asíncronas (EN PROGRESO)

## Resumen de la Sesión del 19/11/2025 (PCS)

**Objetivo Estratégico:** Restaurar la funcionalidad crítica del sistema de generación de contenido y evaluaciones, que se encontraba inoperativo y con la interfaz desincronizada de la base de datos.

**Desarrollo y Hallazgos:**
1.  **Corrección de "Ceguera" de la Interfaz (`academic_structure/models.py`):** Se diagnosticó que el botón "Generar Contenido" aparecía incluso cuando el contenido ya existía, debido a que la lógica solo verificaba "Familias de Contenido" y no asignaciones directas. Se implementó una corrección en `is_content_generation_locked` y `get_public_status` para detectar contenido vinculado directamente.
2.  **Restauración de Resiliencia en Tareas (`orchestrator/tasks.py`):** Se identificó que las evaluaciones se quedaban atascadas en estado `PROCESSING` porque la tarea usaba el campo `last_error` como almacenamiento temporal de datos, fallando silenciosamente. Se refactorizó `generate_assessment_from_content_task` para realizar la generación y guardado de preguntas de forma atómica y robusta.
3.  **Corrección de Namespaces en Plantillas:** Se corrigieron referencias obsoletas (`content_automation` -> `orchestrator`) en `create_academic_task.html`, `create_free_task.html` y `manage_logs.html`.
4.  **Limpieza de Datos:** Se eliminó manualmente la evaluación ID 158 que había quedado en un estado irrecuperable.

**Estado Actual:**
El backend de generación (contenido y evaluaciones) ha sido reparado. Sin embargo, el **Dashboard de Administración está inaccesible (Error 500)** debido a un error `NoReverseMatch` remanente en las plantillas parciales (`_task_row.html` y posiblemente otras) que aún usan los namespaces antiguos.

## Hoja de Ruta para la Próxima Sesión

**Objetivo Inmediato:** Recuperar el acceso al Dashboard y verificar el flujo completo de usuario.

**Plan de Acción Atómico:**
1.  **Corrección de Plantillas Parciales:** Descargar y corregir `_task_row.html`, `_api_key_selector.html` y `task_log_full_page.html` para solucionar el `NoReverseMatch`.
2.  **Verificación Integral:** Confirmar que:
    *   El Dashboard carga correctamente.
    *   Las asignaturas con contenido generado muestran "Ver Contenido" en lugar de "Generar".
    *   La generación de una nueva evaluación completa su ciclo sin atascarse.
