# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Propósito:** Hito contenedor persistente para tareas de depuración, resolución de dudas imprevistas y mantenimiento correctivo del sistema.
**Estado:** **EN PROGRESO** (Fase de Monitorización Pasiva)

## Bitácora de Sesión

### 28/11/2025 - 29/11/2025 (Sesiones Previas)
*   Resolución de incidencia crítica de BD (34GB liberados).
*   Reparación integral de Admin Users y Registro.

### 30/11/2025 - Mejoras UX y Seguridad
*   **Spinner Global:** Implementación exitosa de indicador de carga que intercepta navegación interna y formularios.
*   **Anti-Screenshot:** Evaluado y descartado por UX en móvil.

### 01/12/2025 - Corrección de Flujos de Contenido y Orquestación
*   **Fix "Zombie" (Backend):** Refactorización de `admin_views.py` para diferir la creación del `ContentMaterial`.
*   **Fix Flujo Solicitudes:** Corrección del formulario "Aprobar Solicitud".
*   **Fix Namespaces:** Corrección de `NoReverseMatch` en Orchestrator.
*   **Fix "Asesino de Zombies":** Corrección crítica en `_purge_zombie_tasks`. Se aumentan el umbral a 24h y se protegen los estados de espera.
*   **Cortafuegos Empírico de Cuota:** Implementación de lógica de espera de 70s ante errores 429.
*   **Rescate de Contenido:** Restauración de la lógica de reintento ante `PROHIBITED_CONTENT`.
*   **Robustez de Parsers:** Mejoras en `clean_json_response` y detección flexible de `---FUENTES---`.

### 01/12/2025 (Tarde) - Estabilidad y Copyright
*   **Resolución de "Error Fantasma" en Admin:** Se confirmó que el error `NoReverseMatch` en el panel de control del orquestador se debía a una falta de recarga del proceso WSGI tras cambios previos.
*   **Manejo de Errores de Copyright (Recitation):**
    *   **Detección:** Implementada captura de `finish_reason: 4` en `gemini_service.py` para identificar bloqueos por recitación literal de fuentes protegidas.
    *   **Mitigación:** Implementada estrategia de evasión automática en `orchestrator/tasks.py`. Si se detecta el error, el sistema reintenta la generación de esa sección específica inyectando instrucciones de paráfrasis y síntesis en el prompt.

## Hoja de Ruta (Tareas Pendientes)

### Monitorización
*   **Estado:** A la espera de resultados de la prueba con usuarios reales. Mantenimiento del hito abierto para incidencias emergentes.
