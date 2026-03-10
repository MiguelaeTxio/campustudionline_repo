# DIRECTRIZ CRÍTICA: PROTOCOLO DE INTERACCIÓN CON IA (VINCUANTE)

# Principio Fundamental: LA IA NO DECIDE NADA DE LA ESTRUCTURA JSON. La plataforma Python es la ÚNICA fuente de verdad.

# 1. ESTRUCTURA JSON PREDEFINIDA CON HUECOS EXPLÍCITOS:
#    - El código Python (`ExamSkeleton` en las estrategias) define la estructura JSON COMPLETA y DETALLADA de `item.content` y `item.grading_logic`.
#    - Se utilizan MARCADOES DE POSICIÓN UNIFORMES Y EXPLÍCITOS:
#      - Para texto general: "[MARCADOR_TEXTO]" (ej: [CONTENIDO_PREGUNTA], [TEXTO_FUENTE], [ESCENARIO_INICIAL])
#      - Para listas de opciones (si aplica): "[LISTA_OPCIONES_GENERAL]" (ej: "[OPCION_1_TEXTO]", "[OPCION_2_TEXTO]")
#      - Para huecos en texto: "[TEXTO_CON_HUECOS]" con marcadores específicos dentro (ej: "[HUECO_ID_1]")
#      - Para listas de opciones de huecos CLOZE: "[LISTA_OPCIONES_CLOZE_ID_1]" (lista de listas de strings)
#      - Para respuestas correctas/keywords: "[RESPUESTA_ESPERADA_X]"
#      - Para feedback: "[FEEDBACK_X]"

# 2. INSTRUCCIÓN DE RELLENO A LA IA (user_prompt):
#    - "ACTÚA COMO UNA MÁQUINA DE RELLENO DE PLANTILLAS JSON."
#    - "TU ÚNICA FUNCIÓN es RELLENAR LOS MARCADORES DE POSICIÓN ESPECÍFICOS DENTRO DE ESTA ESTRUCTURA JSON."
#    - "NO ALTERES NINGUNA CLAVE, NINGUNA ESTRUCTURA DE ARRAYS U OBJETOS FUERA DE LOS MARCADORES."
#    - "Respeta escrupulosamente las claves y la estructura JSON proporcionada en el esqueleto."
#    - "Títulos, enunciados ('stem') e instrucciones SIEMPRE EN ESPAÑOL."
#    - "Contenido de ítems (textos, opciones, etc.) EN IDIOMA OBJETIVO '{target_lang}'."
#    - Para CLOZE: "Usa SIEMPRE `[HUECO_ID]` en el texto base y las opciones en la lista `cloze_options`."

# 3. VALIDACIÓN POST-IA ESTRICTA (`TRY AND FAIL`):
#    - El orquestador compara la respuesta JSON de la IA con la plantilla original.
#    - Si la IA altera la estructura, añade claves o cambia tipos de datos, el intento se RECHAZA INMEDIATAMENTE, se loguea y se reintenta.