# Sumario de Sesión: Implementación de Control Híbrido del Orquestador

## 1. Resumen Ejecutivo
Se ha intervenido el núcleo del sistema de orquestación (`orchestrator`) para implementar una lógica de ejecución híbrida. Esto permite detener el consumo de API asociado a la "Generación Masiva" (relleno de fondo) sin interrumpir el servicio a los usuarios finales (Evaluaciones y Solicitudes de Contenido). Adicionalmente, se resolvió una incidencia operativa con la gestión de campañas en Meta Ads.

## 2. Cambios Implementados
*   **Modelo de Datos (`AutomationSettings`):** Nuevo campo `is_mass_generation_enabled`.
*   **Lógica de Negocio (`tasks.py`):** Reestructuración del flujo de `global_orchestrator_task`. Ahora, las tareas prioritarias (Usuarios) se evalúan antes de comprobar los interruptores de limitación.
*   **Interfaz de Administración:** Nuevo panel de control con gestión independiente para el "Sistema General" y la "Generación Masiva", incluyendo indicadores visuales de estado.

## 3. Estado Final
*   **Sistema:** ONLINE
*   **Generación Masiva:** PAUSADA (Por defecto/Configuración actual)
*   **Hito 24:** COMPLETADO

## 4. Archivos Afectados
*   `orchestrator/models.py`
*   `orchestrator/tasks.py`
*   `orchestrator/admin_views.py`
*   `orchestrator/admin_urls.py`
*   `orchestrator/templates/admin/orchestrator/_automation_control_panel.html`
*   `orchestrator/templates/admin/orchestrator/_automation_status_panel.html`
