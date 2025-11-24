# Hito 5: Mantenimiento y Mejoras Generales

**Propósito:** Abordar bugs acumulados, realizar mejoras de usabilidad y optimización de infraestructura.
**Estado:** **EN PROGRESO**

## Hoja de Ruta Inmediata (Noviembre 2025) - Próxima Sesión: UX/UI

### 1. Unificación de UX/UI (Estandarización Visual)
*   **Estandarización de Botones:** Unificar aspecto, tamaño y paleta de colores de todos los botones de la plataforma. Asegurar que una misma acción tenga siempre la misma leyenda y color en toda la plataforma.
*   **Corrección de Leyendas:** Corregir literales incorrectos o confusos (ej. en Sala de Estudio cambiar `resumen reciente` por `actividad reciente`).
*   **Reubicación del Explorador:** Mover el acceso al Explorador a la NavBar, ubicándolo junto al menú personal. Debe ser un icono/menú hamburguesa sin leyenda de texto.
*   **Renombrado de Contexto:** Al acceder desde el Explorador, eliminar "Sala de Estudio" del título y sustituirlo por "Accesos Directos" o similar.

## Histórico de Tareas

- **Tareas Completadas (Noviembre 2025 - Sesión Logs/API):**
    - **(COMPLETADO) Recuperación de Visibilidad de API Keys:** Se restauraron los indicadores visuales de estado (Cuarentena/Activa) en el panel de administración del Orquestador (`ApiKeyAdmin`), resolviendo la regresión visual.
    - **(COMPLETADO) Sistema Integral de Gestión de Logs:** 
        - Se implementó el mecanismo de **Offloading** para descargar logs pesados a JSON y purgar la base de datos (acciones `download_logs` y `purge_logs`).
        - Se creó una herramienta de **Visualización Offline** integrada en el admin para consultar los logs descargados sin rehidratar la BBDD.
        - Se optimizó el logging en `tasks.py` eliminando la persistencia de prompts masivos.
        - Se ejecutó una limpieza retrospectiva (`clean_task_logs`) saneando más de 13,000 entradas de log históricas.

- **Tareas Completadas (Anteriores):**
    - Refactorización del Sistema de Anotaciones.
    - Corrección y Robustecimiento de `CopiaContenido`.
    - **Estabilización del Servidor (Resolución de `Segmentation Faults`):** Se erradicó la causa de los `segfaults` intermitentes reemplazando `PyMuPDF` por `weasyprint` + `pdf2image`.
    - **Refactorización del Servidor de Estáticos:** Eliminación de `Whitenoise` en favor de `collectstatic` nativo.
    - **Visitas Guiadas (`Shepherd.js`):** Implementación completa en Sala de Estudio, Evaluaciones y Resultados.
    - **Corrección de Bugs Críticos:** Teclado virtual en Android, enlaces de corrección en evaluaciones, regresiones visuales en directorios.
    - **Re-arquitectura del Dashboard de `content_automation`:** Transformación a un panel jerárquico y observabilidad mejorada.
    - **Estabilización Post-Refactorización (Identificadores):** Resolución masiva de `NoReverseMatch`, `ImportError` y errores de templates tras la estandarización a inglés.
    - **Robustecimiento del Generador de Contenido:** Lógica de bloqueo de duplicados, gestión de errores de cuota (`ResourceExhausted`) y reintentos inteligentes.
    - **Sistema de Generación Automática (v1):** Creación de la app `content_automation` (ahora integrada en `orchestrator`).
    - **Optimización de Generación (Markdown):** Eliminación de dependencia JSON en favor de parsing Markdown robusto.
    - **Creación de Jerarquía de Chats Académicos:** Generación masiva de 4433 salas.

- **Tareas Pendientes (Backlog):**
    - **Refactorización del Directorio Intelectual:** Corregir visualización de categorías vacías y restaurar arquetipos.
    - **Mejoras de UX en Sala de Estudio:** Botones de compartición y ayuda contextual.
