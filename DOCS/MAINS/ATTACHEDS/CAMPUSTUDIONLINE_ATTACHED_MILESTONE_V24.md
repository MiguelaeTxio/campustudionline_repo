# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Propósito:** Hito contenedor persistente para tareas de depuración, resolución de dudas imprevistas y mantenimiento correctivo del sistema.
**Estado:** **EN PROGRESO**

## Bitácora de Sesión

### 28/11/2025 - 29/11/2025 (Sesiones Previas)
*   Resolución de incidencia crítica de BD (34GB liberados).
*   Reparación integral de Admin Users y Registro.

### 30/11/2025 - Mejoras UX y Seguridad
*   **Spinner Global:** Implementación exitosa de indicador de carga que intercepta navegación interna y formularios.
*   **Anti-Screenshot:** Evaluado y descartado por UX en móvil.

### 01/12/2025 - Corrección de Flujos de Contenido
*   **Fix "Zombie" (Backend):** Refactorización de `admin_views.py` para diferir la creación del `ContentMaterial` y evitar bloqueos por validación.
*   **Fix Flujo Solicitudes:** Corrección del formulario "Aprobar Solicitud" (pre-llenado y cambio de estado).
*   **Fix Namespaces:** Corrección de `NoReverseMatch` en plantillas de Orchestrator.

## Hoja de Ruta (Tareas Pendientes - Prioridad Máxima)

### Estabilización del Motor de Generación (Celery)
*   **Incidencia:** Bucles infinitos en tareas de contenido libre y fallo de parser (`---FUENTES---`).
*   **Plan de Acción:**
    1.  **Diagnóstico:** Trazar ejecución de `generate_full_course_task`.
    2.  **Robustez:** Mejorar parsers para tolerar respuestas imperfectas de la IA.
    3.  **Cortafuegos:** Limitar reintentos de API para proteger la cuota.
