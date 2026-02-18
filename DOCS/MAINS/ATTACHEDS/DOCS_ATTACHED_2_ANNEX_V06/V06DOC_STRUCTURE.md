<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_STRUCTURE.md -->
# V06DOC_STRUCTURE - ARQUITECTURA DE SOFTWARE SEGREGADA (V1.1 - SKELETON-FIRST)

## 1. DESLINDE DE COMPETENCIAS
*   ORCHESTRATOR: Gestiona tráfico, colas Celery y el bucle de llamadas atómicas por sección.
*   ASSESSMENT_V2: Contiene la lógica pedagógica, las estrategias y el motor de calificación.

## 2. PROTOCOLO DE ORQUESTACIÓN (REVISADO)
1.  Petición del usuario y validación de cuotas.
2.  **FASE ESTRUCTURAL (Python):** El `orchestrator` invoca `strategy.get_section_plan()` y crea el objeto `Exam` y sus `ExamSection` correspondientes en la BBDD.
3.  **FASE DE LLENADO ATÓMICO (IA):** El orquestador itera sobre las secciones creadas. Por cada una, realiza una llamada a `gemini-2.5-flash-lite` inyectando el contexto de la sección y el `system_instruction` blindado.
4.  **PERSISTENCIA:** Los `ExamItem` generados se vinculan a la sección activa.
5.  **FINALIZACIÓN:** Una vez recorrido el bucle, el examen pasa a estado 'READY'.

## 3. BLINDAJE DE SEGURIDAD TÉCNICA
*   SKELETON-FIRST: Garantiza que la estructura relacional sea siempre válida antes de llamar a la IA.
*   ATOMIC-PROMPTING: Reduce la ventana de atención de la IA a una sola sección, erradicando errores de truncamiento JSON.
