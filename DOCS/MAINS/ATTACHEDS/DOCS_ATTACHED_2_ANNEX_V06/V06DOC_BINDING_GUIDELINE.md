# DIRECTRIZ CRÍTICA: PROTOCOLO DE INTERACCIÓN CON IA (VINCULANTE)

# Principio Fundamental: OUTPUTS ESTRUCTURADOS NATIVOS (STRUCTURED OUTPUTS)
# La plataforma interactúa con `gemini-3.1-flash` utilizando la capacidad nativa de "Structured Outputs", forzando a la IA a adherirse a un `response_schema` (Pydantic Schema).

# 1. ESQUEMA DE DATOS PREDEFINIDO:
#    - El código Python (las Estrategias) define el esquema esperado mediante clases Pydantic para `item.content` y `item.grading_logic`.
#    - ABANDONO DE MARCADORES: Ya NO se utilizan marcadores de posición (ej. [HUECO_ID_1]) ni plantillas vacías. La IA genera el JSON completo respetando las claves tipadas del esquema proporcionado.

# 2. INSTRUCCIÓN DE GENERACIÓN (system_instruction / user_prompt):
#    - "Actúa como un generador de contenido académico experto."
#    - "Debes devolver un objeto JSON que cumpla estrictamente con el esquema de datos solicitado."
#    - "Títulos, enunciados ('stem') e instrucciones SIEMPRE EN ESPAÑOL."
#    - "Contenido de ítems (textos, opciones, etc.) EN IDIOMA OBJETIVO '{target_lang}'."

# 3. VALIDACIÓN IMPLÍCITA Y SDK:
#    - Al usar `response_mime_type="application/json"` junto con `response_schema`, el SDK de Google GenAI garantiza sintácticamente que la respuesta cumple con la estructura JSON requerida.
#    - Se elimina el bucle manual de "Try and Fail" para corrección de sintaxis JSON.