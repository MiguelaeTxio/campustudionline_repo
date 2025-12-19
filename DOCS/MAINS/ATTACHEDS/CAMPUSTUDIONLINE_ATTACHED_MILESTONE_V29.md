# Hito 29: Extensión de UniversIA a la Plataforma

## 1. Visión y Objetivos
Universalizar la presencia del asistente UniversIA en toda la plataforma, permitiendo una asistencia híbrida (pedagógica/navegación) según el contexto del usuario.

## 2. Estado del Hito
*   **Estado:** COMPLETADO
*   **Fecha de Finalización:** 19/12/2025

## 3. Hoja de Ruta Táctica (Logros)
*   [x] Modificación del Widget de UniversIA para inclusión global en `base.html`.
*   [x] Refactorización del servicio de UniversIA para manejar prompts contextuales según la URL.
*   [x] Definición de `UNIVERSIA_NAVIGATION_PROMPT` para soporte de navegación.
*   [x] Ajuste de CSS para responsividad móvil (max-width dinámico).
*   [x] Verificación de discriminación de contexto (Tutor vs Guía).
*   [x] Implementación de resiliencia activa (reintentos automáticos de ApiKey por cuota).

## 4. Conclusión Técnica
Se ha estabilizado la extensión global de UniversIA implementando una lógica de reintento interno recursivo que garantiza la disponibilidad del servicio ante fallos de cuota de API, manteniendo siempre una comunicación profesional con el usuario.
