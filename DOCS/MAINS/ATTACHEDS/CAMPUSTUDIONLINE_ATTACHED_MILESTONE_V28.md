# Hito 28: Implementación de Asistente Contextual 'UniversIA'

## 1. Visión y Objetivos
Dotar a la Sala de Estudio de un asistente virtual avanzado ("UniversIA") capaz de resolver dudas específicas sobre el material que el estudiante está visualizando en ese momento. Se utilizará arquitectura RAG (Retrieval-Augmented Generation) inyectando el contenido de la copia de estudio en el contexto de Gemini.

## 2. Estado del Hito
*   **Estado:** PENDIENTE
*   **Dependencia:** Hito 27 (Completado)

## 3. Hoja de Ruta Táctica

### 3.1. Backend (Gemini Service)
*   [ ] **Método de Chat Contextual:** Extender `GeminiService` para aceptar contexto de `ContentCopy`.
*   [ ] **Gestión de Historial:** Implementar persistencia de la conversación (opcional) o manejo de sesión efímera.

### 3.2. Frontend (Sala de Estudio)
*   [ ] **Widget de Chat:** Interfaz flotante o panel lateral en `edit_copy.html`.
*   [ ] **Comunicación Asíncrona:** Endpoints AJAX/HTMX para envío de preguntas y recepción de streaming de respuesta.

### 3.3. Identidad
*   [ ] **Persona:** Definir el "System Prompt" de UniversIA (tono académico, alentador y preciso).

## 4. Notas de Ejecución
Se abordará tras finalizar la optimización de UX del Hito 27.
