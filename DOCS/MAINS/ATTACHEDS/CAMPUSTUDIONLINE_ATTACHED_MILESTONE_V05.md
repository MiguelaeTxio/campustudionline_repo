# Hito 5: Mantenimiento y Mejoras Generales

**Propósito:** Abordar bugs acumulados, realizar mejoras de usabilidad y optimización de infraestructura.
**Estado:** **EN PROGRESO**

## Hoja de Ruta Inmediata - Próxima Sesión: Fix Content Redundancy

### 1. Eliminación de Duplicidad en Visualización de Contenidos
*   **Problema:** Al visualizar un material, el texto del "Resumen" se renderiza dos veces de forma redundante: una vez en la tarjeta de cabecera y otra inmediatamente después como introducción del cuerpo (verificado visualmente).
*   **Objetivo:** Modificar la plantilla de detalle de contenido (presumiblemente `content_detail.html`) para unificar o limpiar esta redundancia visual.

## Histórico de Tareas

- **Tareas Completadas (Noviembre 2025 - Sesión Fix Badges):**
    - **(COMPLETADO) Corrección de Inconsistencia en Badges (NavBar):**
        - Se eliminó el filtro temporal (24h) en `context_processors.py` que ocultaba evaluaciones "en progreso" si el proceso demoraba.
        - Se añadió un *spinner* animado al badge (`_navbar_indicators.html`) para feedback visual inmediato de actividad.

- **Tareas Completadas (Noviembre 2025 - Sesión UX/UI Unificación):**
    - **(COMPLETADO) Navegación y Contexto:**
        - Reubicación del acceso "Explorador" a la zona de usuario en la NavBar.
        - Renombrado del panel lateral a "Accesos Directos".
    - **(COMPLETADO) Corrección de Literales:** "Sala de Estudio" y "Copias para Estudio".
    - **(COMPLETADO) Estandarización de Botones:** Guía de Estilo (Azul/Secundario/Rojo) unificada.
    - **(COMPLETADO) Unificación Vista de Detalle:** Breadcrumbs Académicos y botón "Copiar para estudio".

- **Tareas Completadas (Noviembre 2025 - Sesión Logs/API):**
    - **(COMPLETADO) Recuperación de Visibilidad de API Keys:** Restauración de indicadores en Admin.
    - **(COMPLETADO) Sistema Integral de Gestión de Logs:** Offloading a JSON y purga de BBDD.

- **Tareas Completadas (Anteriores):**
    - Refactorización del Sistema de Anotaciones.
    - Corrección y Robustecimiento de `CopiaContenido`.
    - **Estabilización del Servidor:** Reemplazo de `PyMuPDF` por `weasyprint`.
    - **Refactorización del Servidor de Estáticos:** `collectstatic` nativo.
    - **Visitas Guiadas (`Shepherd.js`):** Implementación completa.
    - **Corrección de Bugs Críticos:** Teclado Android, enlaces de corrección, etc.
    - **Re-arquitectura Dashboard `content_automation`.**
    - **Robustecimiento Generador de Contenido.**
