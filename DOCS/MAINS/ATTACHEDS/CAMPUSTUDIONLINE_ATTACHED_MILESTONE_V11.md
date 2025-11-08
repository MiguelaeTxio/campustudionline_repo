# Hito de Estabilización: Generador de Contenido v5 (Arquitectura de Persistencia Incremental)

**Propósito:** Re-arquitecturizar el sistema de generación de contenido para erradicar el riesgo de pérdida de datos ante fallos en la fase de ensamblaje final.
**Estado:** **COMPLETADO**.

- **Propósito:** Re-arquitecturizar el sistema de generación de contenido para erradicar el riesgo de pérdida de datos ante fallos en la fase de ensamblaje final. El incidente crítico (`max_allowed_packet` error) demostró que el enfoque de "ensamblar y guardar al final" es inaceptable. La nueva arquitectura se basará en la persistencia incremental y atómica de cada sección de contenido generada.
- **Estado:** COMPLETADO.
- **Tareas:**
    - **Re-arquitectura del Modelo de Persistencia:**
        - Introducir un nuevo modelo (`content_automation.GeneratedContentChunk`) para almacenar cada sección de contenido individualmente, vinculada a la `PendingContentTask`.
        - Refactorizar la tarea Celery para que guarde cada sección en la nueva tabla inmediatamente después de su generación exitosa, en lugar de acumularla en memoria.
        - Modificar la fase final de la tarea para que construya el `ContenidoMaterial` a partir de los `chunks` ya persistidos en la base de datos.
    - **Optimización del Flujo de API:**
        - Implementar un retardo configurable entre llamadas a la API para mitigar los errores de límite de cuota y estabilizar el proceso de generación a largo plazo.
        - **Re-arquitectura del Almacenamiento de Contenido (COMPLETADO):** Se ha eliminado la dependencia de un único campo `body` en `ContentMaterial`. El sistema ahora ensambla y renderiza dinámicamente el contenido a partir de los `GeneratedContentChunk` persistidos, eliminando el error `max_allowed_packet` y permitiendo contenido de tamaño virtualmente ilimitado.
    - **Validación de Estrategia de Reintento para `MAX_TOKENS` (COMPLETADO):** Se ha validado experimentalmente una estrategia de resiliencia para el generador de contenido. Cuando una tarea falla por exceder el límite de tokens (`MAX_TOKENS`), el sistema estará preparado para reintentar la generación de esa sección utilizando un prompt alternativo que exige una menor verbosidad a la IA, asegurando la finalización de la tarea sin intervención manual.

