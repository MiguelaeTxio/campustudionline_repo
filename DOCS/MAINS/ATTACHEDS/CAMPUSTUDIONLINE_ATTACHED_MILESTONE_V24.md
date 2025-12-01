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

### 01/12/2025 - Corrección de Flujos de Contenido
*   **Fix "Zombie" (Backend):** Refactorización de `admin_views.py` para diferir la creación del `ContentMaterial`.
*   **Fix Flujo Solicitudes:** Corrección del formulario "Aprobar Solicitud".
*   **Fix Namespaces:** Corrección de `NoReverseMatch` en Orchestrator.

### 01/12/2025 - Estabilización Crítica de Celery y Motor de Generación
*   **Fix "Asesino de Zombies":** Corrección crítica en `_purge_zombie_tasks`. Se aumentan el umbral a 24h y se protegen los estados de espera (`PENDING`) para evitar el borrado de tareas legítimas en cola.
*   **Cortafuegos Empírico de Cuota:** Implementación de lógica de espera de 70s ante errores 429. Si persiste tras 3 intentos espaciados, se asume cuota diaria y se aplica cuarentena.
*   **Rescate de Contenido:** Restauración de la lógica de reintento ante `PROHIBITED_CONTENT`.
*   **Robustez de Parsers:** Mejoras en `clean_json_response` y detección flexible de `---FUENTES---` para tolerar variaciones de la IA.

## Hoja de Ruta (Tareas Pendientes)

### Monitorización
*   **Estado:** A la espera de errores o regresiones. No hay desarrollos activos planificados hasta nueva incidencia.
