# Hito de Infraestructura: Migración a Python 3.9+ y al Nuevo SDK de Google Gen AI

**Propósito:** Actualizar la infraestructura base del proyecto para superar un bloqueo tecnológico crítico. El SDK de Google Gen AI actual (`google-generativeai` v0.x) está obsoleto, su soporte finaliza el 31 de agosto de 2025 y es incompatible con funcionalidades avanzadas como el modo por lotes. El nuevo SDK (`v1.x` y superior) requiere una versión de Python (3.9+) más reciente que la utilizada actualmente. Esta migración es un requisito indispensable para la escalabilidad, el coste y el futuro del sistema de IA.
**Estado:** **PAUSADO**.

- **Propósito:** Actualizar la infraestructura base del proyecto para superar un bloqueo tecnológico crítico. El SDK de Google Gen AI actual (`google-generativeai` v0.x) está obsoleto, su soporte finaliza el 31 de agosto de 2025 y es incompatible con funcionalidades avanzadas como el modo por lotes. El nuevo SDK (`v1.x` y superior) requiere una versión de Python (3.9+) más reciente que la utilizada actualmente. Esta migración es un requisito indispensable para la escalabilidad, el coste y el futuro del sistema de IA.
- **Estado:** PENDIENTE (BLOQUEO CRÍTICO).
- **Tareas:**
    - **Creación de Entorno Virtual:** Crear un nuevo entorno virtual en PythonAnywhere con una versión de Python compatible (3.10 o superior).
    - **Instalación de Dependencias:** Reinstalar todas las dependencias del proyecto en el nuevo entorno utilizando el flujo de trabajo de `pip-tools`.
    - **Refactorización del Servicio de IA:** Actualizar el código en `core/services/gemini_service.py` y sus consumidores para utilizar la nueva sintaxis y objetos del SDK de Google Gen AI.
    - **Pruebas de Regresión:** Realizar pruebas exhaustivas para asegurar que toda la funcionalidad dependiente de la IA (generación de contenido, autoevaluaciones, etc.) sigue operando correctamente tras la migración.

