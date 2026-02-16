# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_ROADMAP.md
# V06DOC_ROADMAP - MANIFIESTO DE CUMPLIMIENTO TÉCNICO (V1.2)

## 1. INFRAESTRUCTURA Y MODELADO (V06DOC_STRUCTURE & TEMPLATES) - [X] 100%
- [X] Deslinde de competencias Orchestrator vs Assessment_v2.
- [X] Modelos relacionales: Exam (Header), ExamSection (Phase), ExamItem (Atomic).
- [X] Registro de Consumo (TrackingService) y CostLogs.
- [X] Registro de Sesión (EventLog JSON en modelo Exam).
- [X] Capa de Transporte: Inclusión de namespaces 'assessment_admin' en core/urls.py.

## 2. CEREBRO DE DEDUCCIÓN (V06DOC_LOGIC_MAPPING & LEVELS) - [X] 100%
- [X] Detección de Archetype (LANG, HEALTH, TECH, SOC, HUM).
- [X] Detección de Itinerario sensible al contexto (MAIOR, MINOR, ROT, PROF).
- [X] Detección de Nivel Pedagógico (C->B->A) con soporte para numerales romanos.
- [X] Implementación de 'Rigor Factor' (0.8, 1.0, 1.6) y 'Penalty Threshold'.

## 3. VALIDACIÓN DE MOTORES DE BLOQUES (V06DOC_BLOCKS) - [EN PROGRESO]
- [X] **PRM-STRIKE**: Fórmula UGR [A - E/(N-1)] y distractores conceptuales.
- [ ] **RBT-CANON**: Validación por lexemas nucleares (Sin paráfrasis en PROF).
- [ ] **RPP-TRAZA**: Calificación multietapa con arrastre de error (Lógica 50% planteamiento).
- [ ] **CDS-KILL**: Checklist dicotómico. Omisión = Anulación de sección.
- [ ] **DRA-HOLO**: Rúbrica de 4 ejes. Penalización formal hasta -2.5.
- [ ] **BMT-SHIFT**: Transferencia de registro técnico/divulgativo.
- [ ] **ILC-CONTEXT**: Inferencia diagnóstica basada en datos brutos.
- [ ] **EV-PALE**: Transcripción y exégesis de fuentes primarias.
- [ ] **CLO-OPEN**: Open Cloze con validación morfosemántica.
- [ ] **CLO-MULTI**: Multiple Choice Cloze con distractores de "False Friends".
- [ ] **MAT-LINK**: Matriz de vinculación Drag & Drop.

## 4. VALIDACIÓN DE COMPONENTES UI (V06DOC_WIDGETS) - [PENDIENTE]
- [ ] **W-TECH-CALC**: Consola de cálculo con renderizado MathJax.
- [ ] **W-CLIN-SCAN**: Visor HD de imágenes médicas y marcado.
- [ ] **W-OBJ-STRIKE**: Selector con tachado visual de descartes.
- [ ] **W-HUM-TEXT**: Editor con pantalla dividida y gestor de citas.
- [ ] **W-PROC-ACTION**: Checklist con cronómetro ECOE integrado.
- [ ] **W-COMM-DIALOG**: Grabadora e interacción UniversIA.
- [ ] **W-LAW-NAV**: Buscador de jurisprudencia y normativa emulada.
- [ ] **W-TXT-CLOZE**: Inputs incrustados en texto fluido.
- [ ] **W-MIX-MATCH**: Interfaz de conectores visuales.

## 5. REGLAS DE NEGOCIO Y FEEDBACK (V06DOC_METADATA) - [PENDIENTE]
- [ ] Matriz de Etiquetas: COMP_GEN, COMP_TRA, COMP_ESP, COMP_PROF.
- [ ] Taxonomía Cognitiva: COG_REM a COG_CREA.
- [ ] Taxonomía de Feedback: FB_CONCEPT, FB_FORMAL, FB_PROCEDURAL, FB_SAFETY.
- [ ] Sistema de Badges: Estados 'Generando', 'Listo', 'Calificado'.

---
**LEY DE CONTINUIDAD:** Prohibido dar por completada una tarea sin test unitario o validación visual documentada.
