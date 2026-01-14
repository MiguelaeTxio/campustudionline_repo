# Hito 6: Sistema de Autoevaluaciones con IA (RECTIFICACIÓN MULTIMEDIA)

**Estado Actual:** ⚠️ CRÍTICO - RECONSTRUCCIÓN NECESARIA
**Modelo Vinculante:** `gemini-2.5-flash-lite` (Restaurado por estabilidad).

## ESTADO TÉCNICO AL CIERRE (14/01/2026)
1.  **Modelo:** Regresión ejecutada de 3.0 a 2.5 Lite tras errores 503. Directriz actualizada en `TOTAL_COMMANDER.md`.
2.  **Infraestructura:** Rotación de claves API estandarizada en `orchestrator/tasks.py`.
3.  **Frontend:** Inyectada lógica para MathJax (LaTeX), TTS (Listening) y Grabador V2 (Speaking) en `take_assessment.html`.
4.  **Backend:** `views.py` preparado para recibir archivos de audio.

## ERRORES DETECTADOS (DEUDA TÉCNICA OBLIGATORIA)
*   **Violación de Idioma:** Los enunciados generados por la IA están en Inglés (Cambridge Style) en lugar de Castellano.
*   **Fallo de Inyección:** Las etiquetas `[---TAGS---]` no están siendo capturadas por el JS debido a interferencias de renderizado Markdown.
*   **Fuga de Datos:** El texto del Listening es visible para el alumno.
*   **Desalineación Pedagógica:** Se pide "Use of English" en asignaturas que no son de lengua inglesa.

# HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (ORDEN DE EJECUCIÓN)
**El modelo entrante DEBE ejecutar estas tareas sin desviarse:**

1.  **Refactor de `prompt_generators.py`:**
    *   Traducir TODAS las etiquetas de interfaz al Castellano (ej: "PARTE 1: USO DE LA LENGUA").
    *   Parametrizar el idioma de la asignatura para que no asuma Inglés por defecto.
    *   Instruir a la IA para que entregue los tags `[---TRANSCRIPT---]` y `[---RECORDING-REQUIRED---]` en texto plano, prohibiendo negritas o bloques de código que rompan la Regex.

2.  **Blindaje Frontend en `take_assessment.html`:**
    *   Implementar una clase CSS `.transcript-hidden { display: none; }` para asegurar que el texto del listening nunca sea visible antes de ser procesado por el JS.
    *   Actualizar la Regex de JS para que sea tolerante a etiquetas HTML (usar `strip tags` antes del match si es necesario).
    *   Inyectar el código de idioma (`it-IT`, `en-GB`) como un atributo `data-lang` en la pregunta para que el TTS no use acentos erróneos.

3.  **Validación de Grabación:**
    *   Realizar una prueba de flujo completo: Grabar -> Enviar -> Verificar que el archivo llega a `media/assessment/audio/`.

