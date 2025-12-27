# Hito 31: Sistema de Agenda Académica Personal (Schedule)

## 1. Visión
Gestión integral de eventos académicos y personales con interfaz moderna y fluida.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (Bloqueo Técnico - Pantalla Blanca tras Borrado)
*   **Última Actualización:** 26/12/2025

## 3. Hoja de Ruta Táctica para la Siguiente Sesión (LEY SUPREMA)
*   **Diagnóstico de "Pantalla Blanca":** Investigar la causa exacta del comportamiento tras confirmar el borrado. Determinar si el navegador está navegando hacia la respuesta JSON (renderizándola como texto plano) o si el modal se vacía sin cerrarse.
*   **Verificación de Flujo AJAX:** Confirmar si la estrategia de "Bypass de Cabeceras" (`?is_ajax=true`) está logrando que el backend devuelva JSON o si persiste la redirección `302`.
*   **Refinamiento de UI:** Una vez recuperada la funcionalidad, pulir los estilos del calendario para asegurar la excelencia visual en móviles (basada en la versión "Night").

## 4. Estado Técnico
*   **Backend:** Implementada detección híbrida (`is_ajax` param + Headers).
*   **Frontend:** Implementada inyección de parámetro `is_ajax=true` en `fetch`. UI restaurada a versión estable.
*   **Pendiente:** El spinner global (`base.html`) se mantiene sin cambios. El spinner local ha sido eliminado.
