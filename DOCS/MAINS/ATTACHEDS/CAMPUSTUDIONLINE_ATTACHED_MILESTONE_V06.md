<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md -->
# ANEXO: HITO 06 - BLINDAJE Y REFACTORIZACIÓN DEL ARQUETIPO DE LENGUAS
# ESTADO: EN PROGRESO (HOJA DE RUTA DEFINITIVA)

## 1. DIRECTRIZ CRÍTICA: PROTOCOLO DE INTERACCIÓN CON IA (VINCULANTE)
**PRINCIPIO: LA IA NO DECIDE LA ESTRUCTURA JSON. PYTHON ES LA ÚNICA FUENTE DE VERDAD.**

*   **Estructura JSON Predefinida:** Las estrategias (`ExamSkeleton`) definen el JSON completo con marcadores:
    *   `[CONTENIDO_PREGUNTA]`, `[TEXTO_FUENTE]`, `[ESCENARIO_INICIAL]`.
    *   `[OPCION_X_TEXTO]` para listas de opciones.
    *   `[TEXTO_CON_HUECOS]` con `[HUECO_ID_X]` internos.
    *   `[RESPUESTA_ESPERADA_X]`, `[FEEDBACK_X]`.
*   **Instrucción de Relleno:** La IA actúa exclusivamente como una MÁQUINA DE RELLENO. Prohibido alterar claves o estructuras.
*   **Idioma:** Títulos e instrucciones en ESPAÑOL. Contenido de ítems en IDIOMA OBJETIVO.

## 2. HOJA DE RUTA DE IMPLEMENTACIÓN (PRÓXIMA SESIÓN)

### PASO 1: REFACTORIZACIÓN DE languages.py (CONTROL JSON)
*   **W-OBJ-STRIKE (PRM-STRIKE, RBT-CANON):** Implementar marcadores en `item.content.stem` y `item.content.options`.
*   **W-TXT-CLOZE (CLO-MULTI, CLO-OPEN):** Configurar `text_with_gaps` con `[HUECO_ID]` y `cloze_options` estructurado en el esqueleto.
*   **W-HUM-TEXT (DRA-HOLO):** Definir `item.content.source_text` como marcador.
*   **W-COMM-DIALOG & W-LAW-NAV:** Definir `item.content.initial_scenario` como marcador.

### PASO 2: REFACTORIZACIÓN DE exam_take.html (FRONT-END)
*   **W-OBJ-STRIKE:** Adaptar template para renderizar strings directas desde `options`.
*   **W-TXT-CLOZE:** Refactorizar JS para generar `<select>` o `<input>` dinámicamente detectando `[HUECO_ID]` en el texto base.
*   **W-HUM-TEXT:** Inyectar `source_text` en el panel lateral.

### PASO 3: VALIDACIÓN ESTRICTA (orchestrator/tasks.py)
*   **Capa de Validación:** Comparar el JSON de respuesta contra la plantilla de marcadores.
*   **Try and Fail:** Rechazo inmediato y reintento si la IA añade claves o cambia tipos de datos.

## 3. REFERENCIA TÉCNICA
*   Documentación satélite: `DOCS_ATTACHED_2_ANNEX_V06/`
*   Estrategia principal: `assessment_v2/services/engine/strategies/languages.py`
