# Hito 30: Estrategia Comercial de Recomendación y Gestión de Afiliados

## 1. Visión y Objetivos
Implementar un sistema de captación de usuarios basado en códigos de recomendación gestionados por comerciales para trazabilidad de conversiones.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Fecha de Inicio:** 20/12/2025

## 3. Resumen de la Sesión Actual (20/12/2025)
*   **Auditoría de IA:** Verificación empírica de la inyección de guías docentes en el prompt de Fase 2. El sistema recupera y utiliza correctamente el Temario Fuente y los Objetivos.
*   **Estimación de Costes:** Calculado un coste de approx. $0.03 por curso, con una inversión total estimada de $80 para los 2169 cursos con Gemini 2.5 Flash Lite.
*   **Transición de Hito:** Pausa del Hito 24 y activación del Hito 30.
*   **Documentación:** Actualización del Documento Maestro y creación del anexo V30.

## 4. Hoja de Ruta para la Siguiente Sesión
*   Definición de modelos Django para `RecommendationCode` y grupos de usuarios.
*   Implementación de lógica de validación de códigos en el formulario de registro.
*   Creación de signals para el conteo de conversiones (primera copia y primera evaluación).
