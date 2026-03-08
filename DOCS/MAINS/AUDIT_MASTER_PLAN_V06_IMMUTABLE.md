# PLAN MAESTRO DE AUDITORÍA INTEGRAL DE FLUJO (V1.0 - INMUTABLE)
# ESTE DOCUMENTO ES LA FUENTE DE VERDAD PARA LA VALIDACIÓN DEL HITO 6.
# PROHIBIDA SU SIMPLIFICACIÓN O RESUMEN.

## 0. FILOSOFÍA DE AUDITORÍA: "TRAZABILIDAD TOTAL"
La auditoría por capas (verificar si existe el archivo) ha fallado.
La nueva metodología es la **AUDITORÍA DE FLUJO**.
Se debe verificar el dato desde que nace en la Documentación hasta que se pinta en el HTML.

**SI UN SOLO PASO FALLA, EL FLUJO ENTERO SE MARCA COMO ROTO.**

---

## 1. FASE DE REPARACIÓN INMEDIATA: ARQUETIPO LENGUAS (PRIORIDAD CRÍTICA)
El sistema actual genera exámenes en Inglés y muestra JSON crudo. Esto es inaceptable.

### 1.1. Auditoría de la Estrategia (`languages.py`)
**Instrucción al Modelo:** Abrir `assessment_v2/services/engine/strategies/languages.py` y verificar LÍNEA POR LÍNEA:
1.  **Firma del Método:** ¿`get_user_prompt` incluye `skeleton_json`? (Debe ser SI).
2.  **Inyección del Esqueleto:** ¿Se serializa `skeleton_json` a string y se mete en el prompt? (Debe ser SI).
3.  **Prompt Binding (Idioma):** ¿Existe una instrucción EXPLÍCITA y DICTATORIAL que diga: *"Títulos e instrucciones EN ESPAÑOL. Contenido del ítem en el idioma objetivo {target_language_code}"*? (Si falta, es ERROR CRÍTICO).
4.  **Prompt Binding (Estructura):** ¿Se ordena a la IA *"NO ALTERES widget_id NI block_type"*? (Si falta, es ERROR CRÍTICO).

### 1.2. Auditoría del Renderizado (`exam_take.html` y includes)
**Instrucción al Modelo:** Abrir `assessment_v2/templates/assessment_v2/exam_take.html` (y sus parciales) y verificar LÍNEA POR LÍNEA:
1.  **Iteración de Ítems:** ¿Cómo se recorre `section.items`?
2.  **Discriminación de Widgets:** ¿Existe un bloque `{% if item.widget_id == 'W-TXT-CLOZE' %}` o similar?
    *   **ERROR ACTUAL:** Si el template hace `{{ item.content }}`, imprimirá el JSON crudo.
    *   **CORRECCIÓN OBLIGATORIA:** Debe haber lógica HTML para pintar:
        *   `W-OBJ-STRIKE` -> Botones de opción / Radio buttons.
        *   `W-TXT-CLOZE` -> Texto con inputs (Open) o Selects (Multi).
        *   `W-MIX-MATCH` -> Columnas conectables (Drag & Drop o SVG).
3.  **Manejo de Feedback:** ¿El feedback se muestra tras la interacción o está visible en el JSON pintado?

---

## 2. FASE DE AUDITORÍA SISTEMÁTICA: ARQUETIPOS RESTANTES
Una vez reparado Lenguas, se debe aplicar el mismo rigor a los otros 5 arquetipos.

### 2.1. Arquetipo HUMANIDADES (`humanities.py`)
*   **Verificar Widget `W-HUM-TEXT`:** ¿El template soporta la pantalla dividida (Split Screen) definida en `V06DOC_WIDGETS`?
*   **Verificar Prompt:** ¿Se fuerza el idioma Español en las instrucciones del ensayo?

### 2.2. Arquetipo SOCIALES (`social.py`)
*   **Verificar Widget `W-LAW-NAV`:** ¿El template tiene un iframe o simulador de buscador legislativo? Si no existe, ¿hay un fallback a texto?
*   **Verificar Prompt:** ¿Se inyecta el `skeleton_json` correctamente?

### 2.3. Arquetipo TÉCNICO (`tech.py`)
*   **Verificar Widget `W-TECH-CALC`:** ¿El template renderiza MathJax/LaTeX? ¿Hay inputs para pasos intermedios (`RPP-TRAZA`)?
*   **Verificar Prompt:** ¿Se fuerza el idioma Español?

### 2.4. Arquetipo CIENCIAS (`science.py`)
*   **Verificar Widget `ILC-CONTEXT`:** ¿Cómo se renderizan las tablas de datos o gráficas? ¿Es JSON crudo?
*   **Verificar Prompt:** ¿Se fuerza el idioma Español?

### 2.5. Arquetipo SALUD (`health.py`)
*   **Verificar Widget `W-CLIN-SCAN`:** ¿El template soporta visualización de imágenes (Zoom/Pan)?
*   **Verificar Widget `W-PROC-ACTION`:** ¿Se renderiza el Checklist de Seguridad (`CDS-KILL`)? ¿Es interactivo?

---

## 3. FASE DE AUDITORÍA DE DATOS Y PERSISTENCIA
1.  **Guardado en BBDD:** Verificar en `orchestrator/tasks.py` (o donde se procese la respuesta de Gemini):
    *   ¿Se valida el JSON contra `EXAM_ITEM_CONTENT_SCHEMA` antes de guardar?
    *   ¿Se limpian los caracteres de escape inválidos que suele meter Gemini en LaTeX?
2.  **Modelo de Datos (`ExamItem`):**
    *   ¿El campo `content` es `JSONField`?
    *   ¿El campo `grading_logic` se guarda separado para no enviarlo al frontend antes de tiempo?

---

## 4. INSTRUCCIONES DE EJECUCIÓN PARA EL MODELO
1.  **NO ASUMIR NADA:** Si un archivo no se ha leído con `cat`, no existe.
2.  **NO RESUMIR:** Si encuentras un error, cítalo literal.
3.  **NO SIMPLIFICAR:** Si la solución requiere 200 líneas de código HTML para los templates, se escriben las 200 líneas.
4.  **SECUENCIA OBLIGATORIA:**
    *   Paso A: Reparar `languages.py` (Prompt Binding).
    *   Paso B: Reparar/Crear `exam_widgets.html` (Renderizado HTML condicional).
    *   Paso C: Verificar Integración en `exam_take.html`.
    *   Paso D: Testear visualmente (o simular renderizado).

