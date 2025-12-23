# Hito 31: Sistema de Agenda Académica Personal (Schedule)

## 1. Visión
Dotar al estudiante de una herramienta de gestión del tiempo integrada, que le permita visualizar sus obligaciones académicas y recibir recordatorios proactivos, centralizando su vida universitaria en la plataforma.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Fecha de Inicio:** 24/12/2025

## 3. Estrategia Técnica
*   **App:** `schedule`
*   **UI:** FullCalendar.js + HTMX
*   **Async:** Celery Beat para cron jobs de notificaciones.

## 4. Hoja de Ruta Táctica para la Siguiente Sesión

### FASE 1: Backend y Modelado (Core)
*   [ ] Inicializar app `schedule`.
*   [ ] Definir modelo `AcademicEvent` con tipología de eventos universitarios.
*   [ ] Implementar validaciones de fechas y relaciones con `Subject`.
*   [ ] Registrar en Admin.

### FASE 2: API Interna y Vistas
*   [ ] Crear endpoint `JSON` para alimentar el calendario frontend.
*   [ ] Crear vistas CRUD (Create, Read, Update, Delete) usando formularios de Django.

### FASE 3: Interfaz de Usuario (Frontend)
*   [ ] Integrar librería `FullCalendar.js`.
*   [ ] Implementar vista mensual, semanal y de agenda (diaria).
*   [ ] Crear modales con HTMX para la gestión de eventos (Drag & Drop si es posible).
*   [ ] Estilar eventos según `event_type` (Ej: Examen = Rojo, Práctica = Azul).

### FASE 4: Motor de Notificaciones
*   [ ] Crear tarea de Celery `check_scheduled_reminders`.
*   [ ] Integrar con servicio de Email (`core`).
*   [ ] Integrar con servicio de WebPush (`messaging`).
