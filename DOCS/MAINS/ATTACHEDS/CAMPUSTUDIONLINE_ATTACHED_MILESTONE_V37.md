# Hito 37: Migración a Gemini 3 Flash y Estandarización de SDK

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
**Objetivo:** Migración Crítica al modelo Gemini 3 Flash.

1.  **Actualización de Entorno:**
    - Modificar `requirements.in`: Fijar `google-genai>=1.51.0`.
    - Ejecutar `pip-compile` y `pip-sync` en el servidor y local (`PCv`).
2.  **Refactorización de `core/services/gemini_service.py`:**
    - Cambiar ID del modelo a `models/gemini-3-flash`.
    - Sustituir `thinking_budget` por `thinking_level` (configurar nivel por defecto en 'medium').
    - Implementar la persistencia y envío de `Thought Signatures` en el historial de mensajes para evitar Errores 400 en sesiones multi-turno.
3.  **Auditoría de Prompts:**
    - Adaptar `DOCS/MAINS/CONTENT_PROMPTS.md` para aprovechar la mayor ventana de contexto y capacidad de razonamiento del nuevo modelo.
4.  **Verificación Empírica:** Generar un material de estudio de prueba y validar que la respuesta incluya los bloques de pensamiento correctos.
