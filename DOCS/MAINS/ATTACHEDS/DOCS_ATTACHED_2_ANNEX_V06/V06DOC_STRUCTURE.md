<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_STRUCTURE.md -->
# V06DOC_STRUCTURE - ARQUITECTURA DE SOFTWARE SEGREGADA (V1.2 - SKELETON-PROMPT BINDING)

## 1. DESLINDE DE COMPETENCIAS
*   ORCHESTRATOR: Gestiona tráfico, colas Celery y el bucle de llamadas atómicas por sección.
*   ASSESSMENT_V2: Contiene la lógica pedagógica, las estrategias y el motor de calificación.

## 2. PROTOCOLO DE ORQUESTACIÓN (ESTRATEGIA COMO PLANTILLA)

### 1. CLASIFICACIÓN Y SELECCIÓN
*   El sistema valida cuotas e identifica el `sub_archetype_id` (ej: `SUB-LIN-CERT`).
*   Selecciona la `Strategy` específica correspondiente (la "Vista").

### 2. FASE ESTRUCTURAL (PYTHON - ESTRATEGIA)
*   El orquestador solicita el esqueleto: `skeleton = strategy.get_exam_skeleton()`.
*   **La Estrategia define:** La lista exacta de `ExamSection` y `ExamItem` (con sus widgets y configuración técnica ya fijados).
*   **SKELETON-PROMPT BINDING:** La Estrategia asocia a cada ítem una `TaskInstruction` (Prompt Específico) que dicta el contenido exacto que debe proveer la IA para ese hueco.
*   **Persistencia:** Se crean en BBDD los objetos vacíos. El examen ya tiene "forma" física antes de llamar a la IA.

### 3. FASE DE RENDERIZADO (IA - LLENADO)
*   El orquestador (Task) actúa como motor de renderizado.
*   Itera sobre la plantilla (ítems vacíos) y llama a la API (Gemini) **exclusivamente para rellenar el contenido**.
*   **Prompt de Rellenado:** La IA recibe el `widget_id` y la `TaskInstruction` vinculada en la Fase 2. No tiene libertad creativa sobre el formato.
*   *Prompt:* "Rellena este Ítem de tipo {widget_id} con contenido sobre {tema} siguiendo la instrucción: {TaskInstruction}".
*   **Persistencia:** Se guarda el contenido generado en la estructura existente.

### 4. FINALIZACIÓN
*   El examen pasa a estado 'READY' una vez que todos los huecos de la plantilla han sido rellenados.

## 3. BLINDAJE DE SEGURIDAD TÉCNICA
*   SKELETON-FIRST: Garantiza que la estructura relacional sea siempre válida antes de llamar a la IA.
*   ATOMIC-PROMPTING: Reduce la ventana de atención de la IA a una sola sección, erradicando errores de truncamiento JSON.
*   PROMPT-BINDING: Asegura que la IA no alucine con el tipo de dato, forzándola a adecuarse al widget definido por Python.
