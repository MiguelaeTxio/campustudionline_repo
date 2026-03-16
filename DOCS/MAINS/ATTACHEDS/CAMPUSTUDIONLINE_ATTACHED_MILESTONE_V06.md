# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN

**Objetivo Principal:** Erradicar de forma definitiva los fallos de presentación en la vista de examen (`exam_take.html`), garantizando una interfaz de usuario limpia, profesional y funcional. Se atacarán simultáneamente tres frentes: la lógica de la vista, la estructura de la plantilla y la variedad del contenido generado.

**Directrices de Implementación (Fuente de la Verdad Absoluta):**

**1. Refactorización de la Vista (`assessment_v2/views.py`):**
    *   **Acción:** Se debe modificar la función `get_context_data` en la `ExamTakeView`.
    *   **Lógica de Sanitización Obligatoria:** Antes de pasar el contexto a la plantilla, se implementará un bucle que recorra las opciones de cada ítem. Dicho bucle debe ser una barrera de contención robusta:
        1.  Verificará si una opción es un `string` que parece un diccionario (ej: `"{'id': 'A', ...}"`). Si es así, intentará convertirlo a un diccionario real usando `ast.literal_eval`.
        2.  Una vez procesado, sea un diccionario original o uno rescatado de un string, extraerá **exclusivamente** el valor de la clave `'text'`.
        3.  El resultado final que se entregará a la plantilla será una lista de diccionarios, donde cada diccionario tendrá **únicamente una clave**: `{'text': '...'}`. Esto garantiza que la plantilla es incapaz de renderizar `id` o cualquier otro metadato.

**2. Limpieza y Re-estructuración de la Plantilla (`exam_take.html`):**
    *   **Encabezado:** Se eliminará la cabecera de depuración actual y se sustituirá por una profesional que muestre dinámicamente el título de la asignatura (`{{ exam.content_copy.original_content.title }}`) y una mención a "UniversIA".
    *   **Visualización del Contexto (`section_stimulus`):** Se modificará la lógica condicional. Si un `section_stimulus` (el texto para leer) existe, **DEBE** mostrarse, independientemente del `layout_mode` del examen. Se eliminará la condición que lo ocultaba en el modo `STANDARD`.
    *   **Renderizado de Opciones:** La plantilla se simplificará al máximo. El bucle que muestra las opciones de respuesta múltiple (`W-OBJ-STRIKE`) se limitará a renderizar `{{ option.text }}`, confiando ciegamente en que la vista ya ha realizado todo el trabajo de limpieza.

**3. Auditoría de la Estrategia de Lenguas (`assessment_v2/services/engine/strategies/languages.py`):**
    *   **Objetivo secundario (si el tiempo lo permite):** Una vez que la presentación sea validada con un **VBO**, se auditará el método `get_exam_schema_plan` en la estrategia `LanguageInstrumentalStrategy`.
    *   **Acción:** Se verificará por qué no se están generando ítems de los tipos `W-MIX-MATCH` (emparejamiento) y `W-TXT-CLOZE` (rellenar huecos), tal como lo permite la documentación (`V06DOC_BLOCKS.md`), y se propondrá una modificación para asegurar su inclusión y aumentar la variedad de los exámenes de idiomas.

Esta hoja de ruta guiará el inicio de la próxima sesión de forma ineludible.
