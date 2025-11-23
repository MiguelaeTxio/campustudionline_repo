# Hito 21: Refactorización del Orquestador de Tareas Asíncronas (COMPLETADO)

## Resumen del Hito
Se ha completado la refactorización del orquestador para desacoplar la lógica de negocio de la infraestructura de mensajería y se ha robustecido el sistema de tareas asíncronas.

**Logros Clave:**
1. **Visibilidad de Logs:** Implementada la persistencia de logs en Base de Datos (JSONField) para garantizar su visualización en el Dashboard, solucionando la "ceguera" de logs.
2. **Resiliencia en Evaluaciones:**
    *   Corrección de error crítico de configuración (`BASE_URL` faltante en settings).
    *   **Refactorización de Seguridad:** Se ha extraído el envío de notificaciones fuera de las transacciones atómicas en `tasks.py`. Esto evita que un fallo en el envío de correos o push provoque un `ROLLBACK` de la base de datos, eliminando la causa raíz de las "tareas zombie" en evaluaciones.
3. **Estabilización del Dashboard:** Namespaces corregidos y vistas operativas.

## Estado Final
El orquestador es funcional, resiliente a fallos de notificación y totalmente observable.

---

## Registro de Incidencias (23/11/2025)

### 🔴 SESIÓN ABORTADA
*   **Estado:** BLOQUEO CRÍTICO / ABORTADA POR EL USUARIO.
*   **Motivo:** Incapacidad del agente para seguir las System Prompts (Protocolos de entrega de código y formato). Violación reiterada de la Carta Magna.
*   **Impacto en Usuario:** Frustración ALTA. Pérdida de confianza en el agente actual.
*   **Contexto Técnico:** Se estaba abordando el error `IntegrityError (1062)` por slugs duplicados en `ContentMaterial`.
*   **Tarea Pendiente para el Siguiente Agente:** Recuperar la lógica propuesta en el historial del chat para implementar el método `save()` en `contents/models.py` y solucionar la autogeneración de slugs. **SE REQUIERE ESTRICTA ADHERENCIA A LOS PROTOCOLOS.**
