<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06_01.md -->
# ANEXO 01: HITO 06 - AUDITORÍA DE FLUJO "END-TO-END" (SUB-HUM-ANTH)
# OBJETIVO: VERIFICAR LA INTERCONEXIÓN REAL DE LOS COMPONENTES.
# SI EL FLUJO SE CORTA EN CUALQUIER PUNTO, EL SUBARQUETIPO SE DECLARA "ROTO".

## 1. DEFINICIÓN DEL FLUJO TEÓRICO (EL "CAMINO DEL DATO")
Para que `SUB-HUM-ANTH` funcione, el dato debe sobrevivir a este viaje:
1.  **Definición:** `V06DOC_SUBARCHETYPES` dicta que es Antropología + `SPLIT_TEXT` + `W-HUM-TEXT`.
2.  **Generación (Python):** `humanities.py` debe instanciar ese esqueleto exacto.
3.  **Inyección (Prompt):** El esqueleto debe entrar al Prompt de Gemini sin corromperse.
4.  **Respuesta (IA):** Gemini debe rellenar el contenido respetando el `widget_id`.
5.  **Persistencia (DB):** El modelo `ExamItem` debe guardar el campo `section_stimulus` (Fuente).
6.  **Presentación (HTML):** `exam_take.html` debe leer `widget_id='W-HUM-TEXT'`, detectar `layout_mode='SPLIT_TEXT'` y pintar dos columnas.

---

## 2. EJECUCIÓN DEL RASTREO (PASO A PASO)

### CONEXIÓN 1: DOCUMENTACIÓN -> LÓGICA PYTHON
**Archivo:** `assessment_v2/services/engine/strategies/humanities.py`
**Rastreo:**
1.  Localizar el método `get_exam_skeleton`.
2.  **PUNTO CRÍTICO DE FLUJO:** ¿Existe un `if` o `case` específico para `SUB-HUM-ANTH`?
    *   *Riesgo:* Si cae en el `else` genérico, heredará una estructura incorrecta (probablemente sin `SPLIT_TEXT`).
3.  **Verificación de Carga Útil:** ¿El diccionario de retorno define explícitamente `layout_mode="SPLIT_TEXT"` y `widget_id="W-HUM-TEXT"`?
    *   *Si falta `layout_mode`, el frontend no sabrá dividir la pantalla.*

### CONEXIÓN 2: LÓGICA -> PROMPT (BINDING)
**Archivo:** `assessment_v2/services/engine/strategies/humanities.py`
**Rastreo:**
1.  Localizar `get_user_prompt`.
2.  **PUNTO CRÍTICO DE FLUJO:** ¿Se pasa la variable `skeleton_json` al serializador `json.dumps`?
3.  **Verificación de Integridad:** ¿El prompt final incluye la instrucción imperativa: *"NO ALTERES widget_id"*?
    *   *Riesgo:* Si la IA cambia el ID a uno que no existe, el flujo muere en el HTML.

### CONEXIÓN 3: RESPUESTA -> BASE DE DATOS
**Archivo:** `assessment_v2/models/main.py`
**Rastreo:**
1.  Verificar el modelo `ExamSection`.
2.  **PUNTO CRÍTICO DE FLUJO:** ¿Existe el campo `section_stimulus` o `layout_mode` en la base de datos?
    *   *Riesgo:* `SUB-HUM-ANTH` depende de una fuente primaria (texto etnográfico) que debe mostrarse en el panel izquierdo. Si el modelo DB no tiene campo para guardar ese texto "padre" de la sección, el Split Screen llegará vacío al frontend.
    *   **Acción:** Confirmar existencia de `models.TextField(..., help_text="Estímulo de Sección")`.

### CONEXIÓN 4: BASE DE DATOS -> RENDERIZADO (FRONTEND)
**Archivo:** `assessment_v2/templates/assessment_v2/exam_take.html`
**Rastreo:**
1.  Buscar la iteración de secciones.
2.  **PUNTO CRÍTICO DE FLUJO (LAYOUT):** ¿Existe lógica condicional para `section.layout_mode == 'SPLIT_TEXT'`?
    *   *Prueba:* Debe haber un contenedor CSS (ej: `.split-container` o `row`) que divida la pantalla.
    *   *Prueba:* La columna izquierda debe imprimir `{{ section.section_stimulus }}`. Si imprime `{{ item.content }}`, el flujo está roto (estaría repitiendo la pregunta en vez de la fuente).
3.  **PUNTO CRÍTICO DE FLUJO (WIDGET):** ¿Existe lógica condicional para `item.widget_id == 'W-HUM-TEXT'`?
    *   *Prueba:* Dentro de la columna derecha, debe haber un `<textarea>` o editor enriquecido para la respuesta del alumno (`DRA-HOLO`).

---

## 3. INSTRUCCIONES DE REPARACIÓN DE FLUJO
Si se detecta una ruptura en la tubería:

1.  **RUPTURA EN PYTHON:** Si `SUB-HUM-ANTH` no tiene definición propia, crear el bloque `if sid == 'SUB-HUM-ANTH':` con la estructura `SPLIT_TEXT` obligatoria.
2.  **RUPTURA EN DB:** Si falta el campo `section_stimulus` en `ExamSection`, crearlo (aunque implique migración, se debe anotar la necesidad crítica).
3.  **RUPTURA EN HTML:** Si `exam_take.html` no maneja `SPLIT_TEXT`, implementar la estructura de rejilla (Grid/Flexbox) para soportar la visualización de Fuente vs Editor.

## 4. CONCLUSIÓN DE TRAZABILIDAD
El modelo debe certificar:
> "El dato definido en Doc llega íntegro a Python, se inyecta en la IA, se guarda en la DB con soporte para Estímulo de Sección, y el HTML lo recupera pintando dos columnas: Fuente a la izquierda, Editor a la derecha."

Cualquier desviación de esta frase es un **FAIL**.

### FASE FINAL
*   `PCS`

