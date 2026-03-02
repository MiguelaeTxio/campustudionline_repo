# ANEXO: HITO 24 - SISTEMA DE RUEGOS Y PREGUNTAS (SOPORTE Y MANTENIMIENTO)
# ESTADO: EN PROGRESO

## CONTEXTO DE LA INCIDENCIA
Existe un fallo crítico en el sistema de generación de contenido masivo (`orchestrator`). Actualmente, los usuarios solicitan contenidos, estas solicitudes se aprueban y se marcan para su automatización, pero el motor no las está procesando ni generando. 

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
La siguiente sesión debe centrarse EXCLUSIVAMENTE en diagnosticar y reparar esta interrupción en el flujo de automatización, siguiendo este orden estricto:

1. **Investigación Histórica (Auditoría Hit):**
   - Rastrear en el historial de sesiones (`GEMINI_SESSIONS_HISTORY.md` y directorio de sumarios `COMPLETED`) las últimas intervenciones arquitectónicas realizadas sobre el módulo `orchestrator` y la lógica de generación masiva. 
   - Objetivo: Identificar qué cambios recientes o refactorizaciones pudieron haber desconectado o bloqueado la cola de tareas.

2. **Auditoría de Código y Base de Datos (Orchestrator):**
   - Revisar el estado y funcionamiento de los modelos `AutomationSettings` y `PendingContentTask` en `orchestrator/models.py`.
   - Analizar la lógica de asignación y ejecución en `orchestrator/tasks.py` para determinar si el proceso Celery está fallando silenciosamente, si hay cuellos de botella de API, o si el interruptor maestro de generación masiva no se está respetando.
   - Extraer logs de tareas fallidas (`last_error`, `task_log`) desde la base de datos para obtener la traza de la excepción.

3. **Resolución y Restauración del Servicio:**
   - Aplicar los parches pertinentes para reactivar el flujo.
   - Garantizar que las solicitudes pasen correctamente del estado pendiente/aprobado a la cola de procesamiento y concluyan generando el `ContentMaterial`.
