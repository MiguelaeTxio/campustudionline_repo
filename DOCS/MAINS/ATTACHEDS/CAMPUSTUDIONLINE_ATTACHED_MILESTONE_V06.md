# Hito 6: Sistema de Autoevaluaciones con IA (Depuración de Interfaz v6)

**Estado:** 🚧 EN DESARROLLO (BLOQUEO TÉCNICO)
**Modelo:** `gemini-2.5-flash-lite`

## RESUMEN DE LA SESIÓN
- **UI/UX:** Implementado filtro `render_markdown` en todas las plantillas. Eliminados badges. Habilitada subida de archivos (imágenes/PDF) con aviso de "Archivos Efímeros".
- **Lógica de Limpieza:** Implementado borrado físico de adjuntos en `orchestrator/tasks.py` al caducar resultados.
- **Estrategia Idiomas:**
    - Dividida en dos llamadas (Split-Call) en `orchestrator/tasks.py` (Reading/Writing + Listening/Speaking).
    - Refactorizada `languages_strategy.py` con prompts endurecidos (Aleatoriedad temática, Anti-metalingüística, Entrevista oral UGR).
- **INCIDENCIA CRÍTICA:** `core/services/prompt_generators.py` contiene un `SyntaxError` (literal de cadena no terminado) que impide el arranque del servidor. La reparación (`PMA`) quedó pendiente de aplicación.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: REPARACIÓN DE EMERGENCIA (PRIORIDAD ABSOLUTA)
1.  **Restaurar `prompt_generators.py`:** Aplicar el parche de sintaxis corregido para levantar el servidor WSGI.

### PASO 2: VERIFICACIÓN DE ESTRATEGIA IDIOMAS
1.  **Test de Generación:** Una vez levantado el servidor, solicitar una evaluación de Idiomas (ej: Francés).
2.  **Validación de Split-Call:** Confirmar que se generan las 4 secciones (Reading, Writing, Listening, Speaking).
3.  **Validación de Contenido:**
    -   Tema aleatorio (no gramatical).
    -   Idioma correcto (Francés).
    -   Speaking formato Entrevista (3 preguntas).

### PASO 3: VALIDACIÓN DE LIMPIEZA
1.  Simular caducidad de una evaluación con adjuntos y verificar que el archivo físico se elimina.

### PASO 4: CIERRE DE HITO
1.  Si todo funciona, limpiar logs y cerrar el hito.
