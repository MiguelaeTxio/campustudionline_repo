# Hito 29: Extensión de UniversIA a la Plataforma

## 1. Visión
Asistente contextual inteligente con capacidades de gestión de agenda.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (Bloqueado por fallo en entorno Web)
*   **Última Actualización:** 25/12/2025

## 3. Hoja de Ruta Táctica para la Siguiente Sesión (LEY SUPREMA)
*   **Diagnóstico Web:** Investigar por qué el servicio funciona en consola (CLI) pero devuelve "Error del servicio" en el navegador.
*   **Auditoría WSGI:** Verificar la carga de variables de entorno (API Keys) en el proceso del servidor web vs entorno de ejecución local.
*   **Refinamiento de Historial:** Confirmar si la estructura `parts: [{'text': ...}]` es aceptada por la versión del SDK instalada en PythonAnywhere.
*   **Persistencia:** Validar el guardado del campo `context_url` bajo condiciones de sesión real.
*   **Skill Agenda:** Una vez desbloqueado el servicio, testear la creación de eventos con conflicto de horario.

## 4. Estado Técnico
*   Frontend: Identidad visual y Drag & Drop implementados.
*   Backend: Lógica de colisiones y enrutamiento por URL implementados.
