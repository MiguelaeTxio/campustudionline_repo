# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Estado:** COMPLETADO

## Resumen de la Sesión CYC (13/12/2025) - Estabilización de Plataforma
*   **Bloqueo Resuelto 1 (Redis, NameError, Conexiones):**
    *   **Hot-Swap a Redis DB 0 (core/settings.py):** Corrección de la URL del Broker que fallaba al apuntar a la DB 1 (`DB index out of range`).
    *   **Optimización de Pool de Conexiones (core/settings.py):** Implementación de `CELERY_BROKER_POOL_LIMIT = 1` para compartir un único pool entre todos los workers y el beat, resolviendo la alerta de saturación del 93% y el retardo en notificaciones.
    *   **Doble Worker (start_unified_workers.sh):** Creación de un script lanzadera para desplegar dos workers (uno para carga pesada y otro exclusivo para chat/notificaciones) en una sola tarea Always-on.
*   **Bloqueo Resuelto 2 (UX/Frontend):**
    *   **Resiliencia Chat Backend (messaging/views.py):** Implementación de un bloque `try...except` para evitar que los fallos de notificaciones bloqueen el envío de mensajes.
    *   **UX Envío de Mensaje (conversation_detail.html):** Aplicación de lógica "Optimista" para que la caja de texto se limpie instantáneamente al enviar.
    *   **Preloader Global (conversation_detail.html):** Inyección de CSS para ocultar el preloader global que se mostraba incorrectamente en la vista de chat privado.

## Hoja de Ruta (Hito CERRADO)
Este hito se cierra. Los problemas de estabilidad y rendimiento prioritarios se han resuelto. La próxima hoja de ruta se centrará en el nuevo Hito 26.
