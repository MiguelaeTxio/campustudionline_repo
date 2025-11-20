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
