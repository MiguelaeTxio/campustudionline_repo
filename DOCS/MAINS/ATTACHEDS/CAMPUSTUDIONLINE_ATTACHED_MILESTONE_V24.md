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

### 04/12/2025 - 05/12/2025 - Resolución de Crisis de Disco y Mejoras de UI/UX
*   **Crisis de Almacenamiento (Error 122):**
    *   **Diagnóstico:** Llenado de disco (3GB/100%) provocado por bucle de tareas de evaluación fallidas que generaban *Core Dumps* y logs masivos (SIGBUS).
    *   **Resolución:** Eliminación de 1.5GB de archivos basura (`core.*`, logs). Recuperación operativa del sistema.
*   **Estabilización del Orquestador:**
    *   **Cancelación Manual:** Corrección de Error 500 (`AttributeError: CANCELLED`) añadiendo el estado al modelo `Assessment` y permitiendo la cancelación desde Admin.
    *   **Blindaje:** Implementación de logs de tamaño de contenido (sin truncado) para monitorización y mejora en el manejo de excepciones fatales en Celery.
*   **Mejoras UI/UX Evaluación:**
    *   **Botón Flotante:** Conversión del botón de "Enviar Evaluación" en un elemento flotante (FAB) para facilitar el envío en exámenes largos.
    *   **Corrección de Badges:** Ajuste en `utils.py` para que los indicadores de estado ("Múltiples Estados") ignoren evaluaciones canceladas o fallidas, limpiando la interfaz de usuario.

## Hoja de Ruta (Tareas Pendientes)

### Monitorización
*   **Estado:** A la espera de nuevas incidencias. Mantenimiento del hito abierto a petición del usuario.
