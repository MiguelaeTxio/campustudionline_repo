# V06DOC_ROADMAP - MANIFIESTO DE CUMPLIMIENTO TÉCNICO (V1.3)

## 1. INFRAESTRUCTURA Y MODELADO (V06DOC_STRUCTURE & TEMPLATES) - [X] 100%
- [X] Deslinde de competencias Orchestrator vs Assessment_v2.
- [X] Modelos relacionales: Exam, ExamSection, ExamItem.
- [X] Registro de Consumo (TrackingService) y CostLogs (Integrado en BaseExamStrategy).
- [X] Registro de Sesión (EventLog JSON).
- [X] Persistencia de Identidad: sub_archetype_id obligatorio en creación y guardado.

## 2. CEREBRO DE DEDUCCIÓN (V06DOC_LOGIC_MAPPING & LEVELS) - [X] 100%
- [X] Detección Heurística de los 22 Sub-Arquetipos (Regex branch/subject).
- [X] Detección de Itinerario (MAI, MIN, ROT, PROF, INV, DOC).
- [X] Detección de Nivel Pedagógico (C->B->A) con soporte robusto para numerales romanos (I, II, III).
- [X] Implementación Matemática de 'Rigor Factor' (0.8, 1.0, 1.6) aplicado en el flujo de notas.

## 3. VALIDACIÓN DE MOTORES DE BLOQUES (V06DOC_BLOCKS) - [X] 100%
- [X] **PRM-STRIKE**: Fórmula UGR [A - E/(N-1)] integrada en lógica de calificación.
- [X] **RBT-CANON**: Validación por lexemas nucleares con discriminación por itinerario.
- [X] **RPP-TRAZA**: Calificación multietapa interactiva (Step-log JS).
- [X] **CDS-KILL**: Lógica de anulación de SECCIÓN COMPLETA vía GradingOrchestrator.
- [X] **MAT-LINK**: Lógica de vinculación Drag & Drop funcional en UI.
- [X] **CLO-OPEN/MULTI**: Captura de múltiples inputs en texto fluido.

## 4. VALIDACIÓN DE COMPONENTES UI (V06DOC_WIDGETS) - [X] 100%
- [X] **W-TECH-CALC**: Consola interactiva con registro de pasos en tiempo real.
- [X] **W-CLIN-SCAN**: Visor con sistema de marcado de coordenadas (X,Y) en overlay.
- [X] **W-OBJ-STRIKE**: Selector con tachado visual y descarte de opciones.
- [X] **W-HUM-TEXT**: Editor de pantalla dividida (Fuente vs Redacción).
- [X] **W-PROC-ACTION**: Panel de seguridad con validación interactiva de pasos.
- [X] **W-TXT-CLOZE**: Integrador de huecos con captura de array de respuestas.
- [X] **W-MIX-MATCH**: Interfaz Drag & Drop funcional con mapping de vinculación.
- [X] **W-COMM-DIALOG**: Estructura de interacción y botones UniversIA.
- [X] **W-LAW-NAV**: Sidebar de recursos dinámico preparado para carga selectiva.

## 5. REGLAS DE NEGOCIO Y FEEDBACK (V06DOC_METADATA) - [EN PROGRESO]
- [X] Aplicación de Rigor Engine (x0.8, x1.3, x1.6).
- [ ] Inyección sistemática de Taxonomía de Feedback (FB_CONCEPT, FB_FORMAL) en GradingReport.
- [ ] Sistema de Badges: Estados 'Generando', 'Listo', 'Calificado'.

---
**PRÓXIMA SESIÓN:** Auditoría Integral, Absoluta y Microscópica inicial para verificar que no existen omisiones entre el código consolidado y la documentación V06.
