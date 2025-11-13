# Hoja de Ruta: Sesión Temporal para la Corrección de Plantillas de Notificación

## Objetivo

Corregir el `django.template.base.VariableDoesNotExist` que ocurre durante el envío de notificaciones (email y push) cuando una autoevaluación está lista.

## Diagnóstico Empírico

Los logs de Celery de la sesión anterior mostraron de forma inequívoca que el motor de plantillas de Django no pudo encontrar las variables `content_title` y `action_url` en el contexto proporcionado.

## Plan de Acción

1.  **Investigación Empírica:**
    *   Solicitar los archivos implicados: `assessment/tasks.py` (para analizar el `context` que se construye), `core/utils.py` (para revisar la función `send_unified_notification`) y las plantillas de notificación (`assessment/email/assessment_ready_subject.txt`, `assessment/email/assessment_ready_body.txt`, `assessment/email/assessment_ready_body.html`).
    *   Analizar el `context` que la tarea `generate_assessment_from_content_task` pasa a la función `send_unified_notification`.

2.  **Implementación Correctiva (PMA):**
    *   Modificar la tarea `generate_assessment_from_content_task` en `assessment/tasks.py` para construir y pasar un `context` completo que incluya las variables requeridas por las plantillas.
