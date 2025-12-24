# Hito 31: Sistema de Agenda Académica Personal (Schedule)

## 1. Visión
Implementación de una agenda académica integrada que centralice clases, exámenes y entregas, con sistema de alertas proactivas.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (Bloqueo Crítico en Frontend)
*   **Fecha de Inicio:** 24/12/2025
*   **Última Actualización:** 24/12/2025

## 3. Arquitectura Implementada
*   **Backend:** App `schedule` con modelo `AcademicEvent`. API REST (`/api/feed/`) para consumo del calendario.
*   **Infraestructura:** Segregación de Workers en `primary` (Beat + Notificaciones) y `heavy` (IA).
*   **Notificaciones:** Tarea periódica `check_scheduled_reminders` configurada en Celery Beat.

## 4. Hoja de Ruta Táctica para la Siguiente Sesión (ESTRICTA)

### PRIORIDAD 1: Reparación del Frontend (Calendar Blank Screen)
El calendario carga la estructura pero no renderiza la grilla ni los eventos ("Cargando...").
1.  **Diagnóstico de Consola:** Verificar errores JS en el navegador (posible fallo de carga de CDN FullCalendar o conflicto de sintaxis en `schedule.js`).
2.  **Validación de API:** Confirmar que el endpoint `/schedule/api/feed/` devuelve el JSON con el formato exacto que espera FullCalendar v6.
3.  **Corrección de Inicialización:** Asegurar que el script JS espera al DOM y a la librería externa antes de instanciar la clase `Calendar`.

### PRIORIDAD 2: Verificación de Notificaciones
1.  **Prueba de Fuego:** Crear un evento para dentro de 1 hora.
2.  **Monitorización:** Verificar logs de Celery (`worker_pri`) para confirmar la ejecución de `check_scheduled_reminders`.
3.  **Recepción:** Confirmar recepción de Push Notification y Email.
