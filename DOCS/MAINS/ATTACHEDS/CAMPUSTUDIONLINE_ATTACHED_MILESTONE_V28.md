# Hito 28: Implementación de Asistente Contextual 'UniversIA'

## 1. Visión y Objetivos
Implementar 'UniversIA', un asistente virtual contextual basado en LLMs que acompañe al estudiante durante su navegación y estudio.

## 2. Estado del Hito
*   **Estado:** COMPLETADO
*   **Fecha de Inicio:** 16/12/2025
*   **Fecha de Finalización:** 17/12/2025

## 3. Logros Alcanzados
### 3.1. Infraestructura Backend
*   [x] Creación de la aplicación Django `universia`.
*   [x] Implementación de `UniversiaService` con integración a Google Gemini (SDK GenAI).
*   [x] Gestión de sesiones e historial de chat en base de datos (`UniversiaSession`, `UniversiaMessage`).
*   [x] Endpoints de API para envío de mensajes y recuperación de historial.

### 3.2. Frontend e Interfaz
*   [x] Widget flotante implementado en CSS/JS puro (sin dependencias pesadas).
*   [x] Integración en la "Sala de Estudio" (`edit_copy.html`).
*   [x] Renderizado de respuestas Markdown a HTML en el servidor (python-markdown) para visualización enriquecida.

### 3.3. Lógica de Negocio y Seguridad
*   [x] **Context Awareness:** Inyección dinámica del título del contenido en el System Prompt.
*   [x] **Strict Guardrails:** Configuración del asistente para rechazar temas no relacionados con el material de estudio activo.

## 4. Notas de Ejecución
*   Se ha optado por un enfoque *server-side rendering* para el Markdown para aligerar la carga del cliente.
*   El asistente vive exclusivamente en la vista de edición de copias para maximizar la utilidad contextual.
