# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 13/11/2025 (CSO)

**Objetivo:** Rediseñar el sistema de autoevaluaciones para que sea robusto y resiliente ante fallos, solucionando un bucle de reintentos ineficaz.

**Desarrollo y Resultado Empírico:**
La sesión aplicó un riguroso método empírico, utilizando el arquetipo de Tarea Celery Resiliente de la app `content_automation` como referencia para la refactorización:
1.  **Diagnóstico:** El análisis de los logs confirmó que la tarea de generación de autoevaluaciones (`generate_assessment_from_content_task`) carecía de una estrategia de manejo de errores robusta, especialmente para fallos de cuota de API, lo que provocaba un bucle de reintentos infinito.
2.  **Refactorización del Modelo:** Se actualizó el modelo `Assessment` (`assessment/models.py`) para incluir estados de fallo granulares (ej: `GENERATION_FAILED_RETRYABLE`, `GENERATION_FAILED_QUOTA`, `GENERATION_FAILED_FATAL`), siguiendo el patrón del arquetipo.
3.  **Refactorización de la Tarea Celery:** Se modificó la tarea `generate_assessment_from_content_task` en `assessment/tasks.py` para implementar un manejo de excepciones explícito, lógica de reintentos con `exponential backoff` y la actualización del estado del modelo en la base de datos para registrar la causa del fallo.
4.  **Migración y Sincronización:** Se generó y aplicó una migración de base de datos para sincronizar el esquema con los nuevos estados del modelo.
5.  **Corrección de Efectos Secundarios:** Se diagnosticaron y corrigieron `AttributeError` subsecuentes en `contents/study_room_views.py` y `assessment/utils.py`, que hacían referencia a los antiguos estados de fallo.

**Estado Final:** La refactorización ha sido completada, dotando al sistema de autoevaluaciones de la resiliencia y robustez requeridas. Sin embargo, se ha detectado un nuevo problema de usabilidad en la interfaz.

## Hoja de Ruta para la Próxima Sesión

El objetivo principal será diagnosticar y corregir el comportamiento anómalo del botón "Realizar Evaluación" en la Sala de Estudio.

1.  **Investigación Empírica:** Ejecutar un script en la `shell` de Django para consultar el estado real de todos los objetos `Assessment` asociados al `ContentCopy` del usuario. El objetivo es verificar la hipótesis de que no existe ninguna evaluación en el estado `COMPLETED` que habilite dicho botón.
2.  **Análisis de la Lógica de la Vista:** Basado en los resultados de la consulta, analizar la función `get_assessment_context` en `assessment/utils.py` para confirmar si la lógica que determina la habilitación del botón está funcionando como se espera o si existe una condición de borde no contemplada.
3.  **Implementación Correctiva:** Aplicar las modificaciones necesarias en la capa de utilidades o vistas para asegurar que el estado del botón refleje fielmente la disponibilidad real de una evaluación para ser realizada.
