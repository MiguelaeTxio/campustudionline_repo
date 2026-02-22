<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_ROADMAP.md -->
# V06DOC_ROADMAP - MANIFIESTO DE CUMPLIMIENTO TÉCNICO (V1.6)

## 5. REGLAS DE NEGOCIO Y FEEDBACK - [X] 100%
- [X] Aplicación de Rigor Engine (x0.8, x1.3, x1.6).
- [X] Inyección sistemática de Taxonomía de Feedback (FB_*) en GradingReport.
- [X] Resumen Cualitativo 'Voz del Catedrático' (Implementado en logic.py).

## 6. GENERACIÓN SEGMENTADA (SKELETON-FIRST) - [X] 100% (DESBLOQUEADO)
- [X] Auditoría de compatibilidad SDK v1 (system_instruction).
- [X] Diseño de Arquitectura Fragmentada (Python Structure + IA Items).
- [X] Implementación de `get_section_plan` en estrategias (para `LanguagesStrategy`).
- [X] Refactorización del bucle iterativo en `orchestrator/tasks.py` (Implementado Atomic Loop).
- [X] Sincronización Documental: El código del orquestador ahora refleja fielmente V06DOC_STRUCTURE.
- [X] Refactorización de UI: Widgets dinámicos implementados con tags de traducción (Regla de Oro).
- [X] Sistema de Resiliencia: Protocolo de 3 reintentos/10min implementado.


## 7. INTEGRIDAD Y LOCALIZACIÓN DINÁMICA (IA) - [X] 100%
- [X] Auditoría Forense: Restauración de 'SD_SPEAK' para espejo total con V06DOC_ARCHETYPES.
- [X] Delegación de Autoridad: La IA asume la traducción dinámica de secciones (Erradicación de listas estáticas).
- [X] Validación de Persistencia: Verificado soporte JSON para widgets V2 complejos.
- [X] Blindaje de Seguridad: Restauración del sistema de bloqueo Staff y Modal Académico.

## 8. INTERFAZ DE EVALUACIÓN (UI/UX) - [X] 100%
- [X] **Integración de Widgets:** Plantilla `exam_take.html` reescrita para cumplir estrictamente con los contratos JSON de `V06DOC_BLOCKS` (RPP-TRAZA, CDS-KILL, etc.).
- [X] **Controlador de Entregas:** Implementado `ExamSubmitView` con ensamblaje de payload y conexión al `GradingOrchestrator`.

## 9. GESTIÓN DE CICLO DE VIDA (ANTI-ABUSO) - [ ] 0% (EN PROGRESO)
- [ ] **Modelo de Datos:** Implementación del campo `expiration_date` en el modelo `Exam` (Ref: V06DOC_TEMPLATES V1.3).
- [ ] **Lógica de Negocio:** Implementación de la regla de caducidad de 24h tras generación (Estado READY).
- [ ] **Integración de Navegación:** Corrección de `navigation_builder.py` para filtrar exámenes caducados o mostrar alertas.
- [ ] **Certificación Final:** Test End-to-End del ciclo completo con validación de caducidad.

---
**ESTADO:** FASE FINAL DE CIERRE Y ANTI-ABUSO.
