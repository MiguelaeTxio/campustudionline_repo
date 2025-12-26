# Hito 31: Sistema de Agenda Académica Personal (Schedule)

## 1. Visión
Gestión integral de eventos académicos y personales con interfaz moderna y fluida.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (Reversión de UI necesaria)
*   **Última Actualización:** 26/12/2025

## 3. Hoja de Ruta Táctica para la Siguiente Sesión (LEY SUPREMA)
*   **Restauración de UI:** Revertir los cambios visuales en `calendar_main.html` y `schedule.js` que han afectado al layout de FullCalendar. La prioridad es recuperar la estética original.
*   **Re-implementación de Borrado:** Diseñar un sistema de eliminación que no dependa de atributos `onclick` globales ni de inyección de scripts directos. Se evaluará el uso de un componente mediador en el DOM.
*   **Optimización FullCalendar:** Ajustar la visualización de eventos para evitar solapamientos visuales en dispositivos móviles.
*   **Consolidación de Vistas:** Unificar las respuestas AJAX en `views.py` para que sean consistentes en todos los métodos (Create/Update/Delete).

## 4. Estado Técnico
*   Backend: Detección de AJAX robusta (Case-insensitive) implementada.
*   Frontend: Fallo detectado en la gestión de ámbitos (Scope) de JavaScript.
