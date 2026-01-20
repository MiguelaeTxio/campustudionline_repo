# ANEXO HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA (UGR EMULATOR)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

---

## ESTADO DE LA HOJA DE RUTA TÉCNICA (Ref. Plan Maestro)
1. [X] **Refactor de Orchestrator.** (Reparado).
2. [X] **Estrategia CEFR_LANGUAGES.** (Refinado: Implementada persistencia dinámica de nivel CEFR e inmersión total B1+).
3. [X] **Estrategia LOGIC_AND_TECH.** (Completado).
4. [X] **Estrategia SOCIO_LEGAL.** (Completado).
5. [X] **Estrategia HEALTH_SCIENCES.** (Completado).
6. [X] **Estrategia HUMANITIES_ARTS.** (Completado: Implementado rigor UGR y estructura de ensayo obligatoria).
7. [X] **Optimización UX y Estabilidad.** (Completado: Markdown, LaTeX, Audio Controls y Deduplicación).

---

## LOG DE AVANCES DE ESTA SESIÓN
*   **Renderizado Markdown & LaTeX:** Implementado filtro `render_markdown` con soporte `arithmatex` y MathJax en frontend.
*   **Control de Audio:** Sustituido TTS simple por `ttsController` con estados Play/Pause/Stop.
*   **Deduplicación de Preguntas:** Implementado filtro de unicidad en `orchestrator/tasks.py` para evitar repeticiones.
*   **Inmersión Lingüística:** Corregido prompt de idiomas para forzar inmersión total en niveles B1+ y eliminadas etiquetas hardcodeadas en la interfaz.
*   **Blindaje de Sistema:** Actualizado `TOTAL_COMMANDER.md` con reglas de bloqueo para rutas absolutas y disciplina operativa.

---

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
**Objetivo Primario:** Auditoría de Estándares Académicos UGR.

1.  **Investigación de Estándares:** Comprobar la realidad de los exámenes de idiomas en la UGR más allá de las 4 destrezas estándar.
2.  **Expansión de Arquetipos:** Evaluar si los 5 arquetipos actuales cubren todo el tejido académico o si se requieren nuevas estructuras de evaluación.
3.  **Validación de Inmersión:** Testear la generación de exámenes en idiomas no latinos (Chino, Árabe) tras los cambios de inmersión.
