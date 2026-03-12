<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_STRUCTURE.md -->
# V06DOC_STRUCTURE - ARQUITECTURA DE SOFTWARE SEGREGADA (V1.2 - SKELETON-PROMPT BINDING)

## 1. DESLINDE DE COMPETENCIAS
*   ORCHESTRATOR: Gestiona tráfico, colas Celery y el bucle de llamadas atómicas por sección.
*   ASSESSMENT_V2: Contiene la lógica pedagógica, las estrategias y el motor de calificación.

## 2. PROTOCOLO DE ORQUESTACIÓN (ESTRATEGIA COMO PLANTILLA)

### 1. CLASIFICACIÓN Y SELECCIÓN
*   El sistema valida cuotas e identifica el `sub_archetype_id` (ej: `SUB-LIN-CERT`).
*   Selecciona la `Strategy` específica correspondiente (la "Vista").

### 2. FASE ESTRUCTURAL Y DE ESQUEMA (PYTHON - ESTRATEGIA)
*   El orquestador solicita el plan de generación: `schema_plan = strategy.get_exam_schema_plan()`.
*   **La Estrategia define:** La lista de secciones e ítems (widgets), junto con el **Pydantic Schema** (o JSON Schema) estricto requerido para ese widget.
*   **SCHEMA-PROMPT BINDING:** La Estrategia asocia a cada ítem una instrucción específica y su correspondiente `response_schema`.
*   **Gestión de Estado:** Ya no se persiste un "esqueleto vacío" en BBDD de antemano. La estructura se maneja en memoria hasta su generación completa.

### 3. FASE DE GENERACIÓN ESTRUCTURADA (IA)
*   El orquestador (Task) ejecuta llamadas atómicas por sección utilizando **Structured Outputs**.
*   Pasa el `response_schema` directamente a la API (`gemini-3.1-flash`) garantizando el formato JSON nativo.
*   **Prompt de Generación:** La IA recibe el contexto y la `TaskInstruction` para generar los datos exactos que demanda el esquema.
*   **Persistencia:** Una vez devuelto el JSON estructurado, se instancian y guardan los objetos `ExamSection` y `ExamItem` definitivos en la base de datos.

### 4. FINALIZACIÓN
*   El examen pasa a estado 'READY' una vez que todos los huecos de la plantilla han sido rellenados.

## 3. BLINDAJE DE SEGURIDAD TÉCNICA
*   SCHEMA-FIRST: Garantiza que la IA esté forzada a nivel de API a devolver una estructura de datos JSON predecible.
*   ATOMIC-PROMPTING: Reduce la ventana de atención de la IA a una sola sección, erradicando errores de truncamiento JSON.
*   PROMPT-BINDING: Asegura que la IA no alucine con el tipo de dato, forzándola a adecuarse al widget definido por Python.
