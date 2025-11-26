# Hito 5: Mantenimiento y Mejoras Generales

**Propósito:** Abordar bugs acumulados, realizar mejoras de usabilidad y optimización de infraestructura.
**Estado:** **EN PROGRESO**

## Hoja de Ruta Inmediata - Próxima Sesión: Fix Badges

### 1. Corrección de Inconsistencia en Badges (NavBar)
*   **Problema:** Al solicitar una evaluación, el badge de progreso no aparece inmediatamente. Solo se muestra cuando el estado pasa a corrección.
*   **Objetivo:** Asegurar que el badge de "Evaluación en progreso" (spinner) aparezca desde el momento en que se solicita la evaluación.

## Histórico de Tareas

- **Tareas Completadas (Noviembre 2025 - Sesión UX/UI Unificación):**
    - **(COMPLETADO) Navegación y Contexto:**
        - Reubicación del acceso "Explorador" a la zona de usuario en la NavBar (icono hamburguesa).
        - Renombrado del panel lateral a "Accesos Directos".
    - **(COMPLETADO) Corrección de Literales:**
        - "Resumen Reciente" -> "Sala de Estudio".
        - "Actividad Reciente" -> "Copias para Estudio".
    - **(COMPLETADO) Estandarización de Botones:**
        - Definición y aplicación de Guía de Estilo: Acciones Principales (Azul), Secundarias (Borde Azul), Borrar (Rojo), Favoritos (Amarillo), Tours (Cyan).
        - Unificación visual en vistas de creación (Contenido, Anuncios, Salas, Enlaces) y listados.
    - **(COMPLETADO) Unificación Vista de Detalle:**
        - Estandarización del botón "Copiar para estudio" (mismo texto y estilo para académico y libre).
        - Implementación de **Breadcrumbs Académicos** para paridad visual con el directorio libre.

- **Tareas Completadas (Noviembre 2025 - Sesión Logs/API):**
    - **(COMPLETADO) Recuperación de Visibilidad de API Keys:** Restauración de indicadores en Admin.
    - **(COMPLETADO) Sistema Integral de Gestión de Logs:** Offloading a JSON, purga de BBDD y visualización offline.

- **Tareas Completadas (Anteriores):**
    - Refactorización del Sistema de Anotaciones.
    - Corrección y Robustecimiento de `CopiaContenido`.
    - **Estabilización del Servidor:** Reemplazo de `PyMuPDF` por `weasyprint`.
    - **Refactorización del Servidor de Estáticos:** `collectstatic` nativo.
    - **Visitas Guiadas (`Shepherd.js`):** Implementación completa.
    - **Corrección de Bugs Críticos:** Teclado Android, enlaces de corrección, etc.
    - **Re-arquitectura Dashboard `content_automation`.**
    - **Robustecimiento Generador de Contenido.**
