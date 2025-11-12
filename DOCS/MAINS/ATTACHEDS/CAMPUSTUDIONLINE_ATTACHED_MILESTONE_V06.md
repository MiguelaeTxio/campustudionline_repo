# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 12/11/2025 (MAMC)

**Objetivo:** Corregir una regresión visual donde el indicador de autoevaluaciones pendientes no aparecía en la barra de navegación global (`NavBar`).

**Desarrollo y Solución Empírica:**
Partiendo del hallazgo de que el `badge` no se mostraba, se implementó una solución en dos fases atómicas y auditadas para asegurar la robustez del sistema:

1.  **Implementación de Notificaciones Efímeras:** Se modificó la lógica en `assessment/views.py` para que el sistema marque internamente una notificación como "vista" (`was_viewed = True`) tan pronto como el usuario accede a la página correspondiente (sea para realizar la evaluación, ver los resultados o un fallo). Esto asegura que la alerta en la `NavBar` desaparezca tras cumplir su propósito informativo, sin alterar el estado real de la evaluación.

2.  **Implementación de "Badge Inteligente":** Se refactorizó por completo el `core/context_processors.py`. La nueva lógica:
    *   Filtra y cuenta únicamente las notificaciones "no vistas".
    *   Si detecta **un solo tipo** de notificación activa, muestra un `badge` específico con el color e icono correspondientes.
    *   Si detecta **múltiples tipos** de notificaciones activas, muestra un `badge` genérico consolidado con la suma total.

**Estado Final:** El problema ha sido **resuelto**. La `NavBar` ahora muestra un indicador de notificaciones inteligente, preciso y no intrusivo que se comporta correctamente en todos los ciclos de vida de las autoevaluaciones.

## Hoja de Ruta para la Próxima Sesión

1.  **Sistema de Resiliencia y Auto-recuperación:**
    *   Eliminar por completo el estado `FAILED` del ciclo de vida de las autoevaluaciones.
    *   Diseñar e implementar un sistema resiliente que, ante un fallo en la generación o corrección, reintente automáticamente la tarea (similar a la lógica del generador de contenidos), en lugar de notificar un error al usuario.
2.  **Refinamiento de la Interfaz de Usuario (UI):**
    *   Actualizar la leyenda de indicadores para eliminar la referencia a "evaluación fallida".
    *   Reasignar el icono de exclamación (`fa-exclamation-triangle`), actualmente usado para fallos, para que sea el icono del `badge` genérico de "múltiples estados", mejorando la comunicación visual.

