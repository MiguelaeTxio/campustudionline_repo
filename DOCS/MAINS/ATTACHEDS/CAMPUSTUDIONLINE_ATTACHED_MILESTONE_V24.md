# Hito 24: Soporte y Mantenimiento: Ruegos y Preguntas

## 1. Visión y Objetivos
Auditar y validar los sistemas críticos de la plataforma en la fase final de pruebas previa al lanzamiento comercial. Priorizar la estabilidad y la experiencia del usuario final sobre la generación automática de contenido.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Fecha de Inicio:** 14/12/2025

## 3. Hoja de Ruta Táctica

### 3.1. Auditoría del Orquestador de Contenido
*   [ ] **Verificación Funcional del Control de Pausa/Reanudación:** Realizar pruebas empíricas para confirmar que el botón de control de la generación masiva de contenido en el panel de administración funciona como se espera, deteniendo y reanudando las tareas de Celery correctamente.
*   [ ] **Análisis de Priorización de Tareas:** Auditar el flujo de tareas para asegurar que las peticiones de los usuarios (ej: generación de evaluaciones) tienen prioridad sobre las tareas de fondo de generación automática de contenido, en respuesta a los recortes de cuota de la API.

### 3.2. Re-evaluación Estratégica de Modelos de IA
*   [ ] **Investigación de Cuotas y Costes:** Recopilar información actualizada sobre las cuotas, límites y estructura de precios del modelo `gemini-2.5-flash-lite` y posibles alternativas viables.
*   [ ] **Análisis de Viabilidad:** Elaborar un informe comparativo para determinar si un cambio de modelo podría ser beneficioso en términos de coste y rendimiento para la fase comercial.
