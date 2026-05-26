# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06 -- HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA

## 1. Descripcion del Hito

Motor de autoevaluacion con IA basado en arquetipos y subarquetipos academicos.
82 subarquetipos certificados. 22 widgets de evaluacion. 20 motores de calificacion.

---

## 2. HOJA DE RUTA PARA LA PROXIMA SESION (LEY SUPREMA - INELUDIBLE)

**ESTADO DEL HITO:** EN PROGRESO - Fase de Implementacion CERTIFICADA S023. Pendiente primer despliegue real.
**FECHA DE ULTIMA ACTUALIZACION:** 2026-05-26
**OBJETIVO S024:** Primer despliegue real controlado. Retirar pantalla de bloqueo para usuario de prueba, generar examen real end-to-end, verificar pipeline completo.

---

### FASE DE IMPLEMENTACION - ESTADO FINAL (S023 -- 2026-05-26)

**18/18 ARCHIVOS CERTIFICADOS (Auditoria TLA S023 -- 0 fallos de codigo):**
1. assessment_v2/models/main.py -- INC-01: comentario INGENIERIA (16)->(17)
2. core/services/gemini_schemas.py -- INC-04: SD_MEDI eliminado. INC-05: step_matrix. INC-06: gap_solutions dict
3. core/services/gemini_service.py -- Sin incidencias
4. assessment_v2/services/engine/strategies/base.py -- INC-07: _grade_ev_tra_precision
5. assessment_v2/services/engine/logic.py -- ITIN_DOC verificado y certificado
6. assessment_v2/services/engine/factory.py -- Sin incidencias
7. assessment_v2/services/engine/strategies/languages.py -- INC-07: EV-TRA-PRECISION en grade_item
8. assessment_v2/services/engine/strategies/health.py -- 18 subarquetipos conformes
9. assessment_v2/services/engine/strategies/humanities.py -- 6 subarquetipos conformes
10. assessment_v2/services/engine/strategies/science.py -- 15 subarquetipos conformes
11. assessment_v2/services/engine/strategies/social.py -- 19 subarquetipos conformes
12. assessment_v2/services/engine/strategies/tech.py -- 17 subarquetipos conformes
13. orchestrator/tasks.py -- Pipeline Skeleton-First verificado
14. assessment_v2/views.py -- Barrera de fuego Data Leak verificada
15. assessment_v2/services/quotas.py -- Ventana movil y penalizacion FREE verificadas
16. assessment_v2/templates/assessment_v2/exam_take.html -- 22/22 widgets. Occidentalizacion (ja/ar/el). data-target-lang
17. assessment_v2/templates/assessment_v2/exam_report.html -- INC-09: qualitative_summary. INC-10: rutas feedback
18. assessment_v2/management/commands/validate_v06_engines.py -- INC-11: docstring 87->82

**DOCUMENTACION SATELITE ACTUALIZADA:**
- V06DOC_LEVELS.md -- Seccion 5 ITIN_DOC certificado (5.1-5.6, base documental UGR 2024-2025)

---

### S024 -- PRIMER DESPLIEGUE REAL CONTROLADO

**CONTEXTO:**
Fase de Implementacion declarada CERTIFICADA en S023 tras auditoria TLA bidireccional
de 18 archivos contra 11 satelites. 11 incidencias detectadas: 9 resueltas, 2 cerradas.
Sistema tecnicamente listo para despliegue real con usuarios controlados.

**PRERREQUISITOS VERIFICADOS EN S023:**
- Selector de rango de temario: operativo
- Widgets de escritura: operativos (touch events, OCR, Occidentalizacion ja/ar/el)
- Pantalla de bloqueo: activa
- collectstatic: ejecutado al cierre de S023

**PASOS S024 -- EN ESTE ORDEN ESTRICTO:**

PASO 1 -- Verificacion de estado del servidor
- Estado de Celery y Redis
- Cola de tareas pendientes: Exam.objects.filter(status=PENDING) via shell
- Logs de error recientes

PASO 2 -- Prueba funcional end-to-end con superusuario (plan DIOS)
- Generar un examen por cada uno de los 6 arquetipos
- Verificar en cada examen:
  a. Clasificacion IA correcta (archetype_id + sub_archetype_id)
  b. Skeleton correcto para ese subarquetipo
  c. Llenado completo de items (content + grading_logic + metadata)
  d. Widgets renderizados en exam_take.html
  e. Entrega y calificacion (submission + grading_report)
  f. Informe renderiza qualitative_summary y desglose

PASO 3 -- Resolucion de incidencias detectadas en produccion
- Documentar cada incidencia
- Resolver on-fly si posible
- Si requiere cambios en constelacion -> candidata a S025

PASO 4 -- Decision apertura a usuarios reales
- Retirar pantalla de bloqueo (despliegue total), o
- Mantener bloqueo y abrir solo a usuarios beta

**NOTA TECNICA -- ITIN_DOC:**
El system_instruction de classify_subject_identity lista 82 IDs de subarquetipos
pero NO menciona ITIN_DOC -- correcto, el itinerario lo deduce Python (AcademicDeductor).
Verificar en prueba funcional que asignatura de Magisterio recibe ITIN_DOC.

**NOTA TECNICA -- Modo Occidentalizacion:**
Motor de transliteracion lee data-target-lang del div#exam-container.
Para japones: examen debe tener target_language_code = ja.
Verificar con examen SUB-LIN-MINOR japones que wanakana.bind() se activa.

---

## 3. Arquitectura del Motor (Referencia)

### 3.1. Pipeline de Generacion (Skeleton-First)
ExamCreateView.post
  -> generate_exam_task.delay(exam_uuid, context_text, topic)
    -> AcademicDeductor.get_context_metadata(subject)
      -> Fase 1: classify_subject_identity (IA Gemini)
      -> Fase 2: deduce_itinerary / deduce_level / deduce_immersion_mode (Python)
    -> ExamFactory.get_strategy(archetype_id, sub_archetype_id, ...)
    -> strategy.get_exam_skeleton() -> ExamSection + ExamItem (vacios)
    -> [bucle por seccion] strategy.get_user_prompt + get_system_prompt
      -> _safe_generate_content -> Gemini API
      -> dirtyjson.loads -> mapeo por UUID -> db_item.save()
    -> exam.status = READY

### 3.2. Pipeline de Calificacion
ExamSubmitView.post
  -> ExamFactory.get_strategy(...)
  -> GradingOrchestrator.grade_submission(submission, strategy)
    -> [por seccion][por item] strategy.grade_item(item, student_input)
    -> apply_rigor_adjustment(raw_score)
    -> kill-switches: CDS-KILL, ITIN_INV, ARCH_HEALTH, ARCH_HUM, ARCH_SOC
    -> gating: ARCH_LANG Non-Compensation Rule
    -> _generate_qualitative_feedback (Voz del Catedratico)
  -> submission.grading_report = report
  -> exam.status = GRADED

### 3.3. Widgets Implementados (22/22)
W-TECH-CALC, W-PROC-ACTION, W-CLIN-SCAN, W-OBJ-STRIKE, W-HUM-TEXT,
W-TXT-CLOZE, W-MIX-MATCH, W-LAW-NAV, W-COMM-DIALOG, W-AUDIO-INSTR,
W-MUS-SCORE, W-ART-IDENT, W-CALLI-PAD, W-PORTFOLIO, W-PHILO-IPA,
W-PHILO-ECDO, W-PHILO-OCR-PALE, W-DOC-RESOURCES, W-CASE-ECOE,
W-MEDI-LAYOUT, W-OCR-PRO, W-INSTR-SELECTOR

### 3.4. Motores de Calificacion (20/20)
PRM-STRIKE, RBT-CANON, RBT-SHORT-LANG, RPP-TRAZA, CDS-KILL,
DRA-HOLO, DRA-HOLO-LIT, BMT-SHIFT, ILC-CONTEXT, EV-PALE,
EV-DIAC-VAL, EV-NORM-ANALYSIS, EV-TRA-PRECISION, EV-TRA-PRECISION-TECH,
EV-ICON-ART, EV-MUS-ANAL, CLO-OPEN, CLO-MULTI, MAT-LINK, DIA-INTERACT

---

## 4. Registro de Sesiones

NOTA DE AUDITORIA (PAA -- 2026-05-09): Tabla reconstruida via PAA desde historial Git.
S001-S008: Etapa Pre-v5.0 sin certificacion contra fuentes primarias UGR.
S009+: Fase de Certificacion con Fidelidad 100% UGR garantizada.

S001  2026-03-18  Pre-v5.0 SUB-LIN-INSTR/MINOR       Refactorizacion subatomica inicial. Sin certificacion UGR.
S002  2026-03-19  Pre-v5.0 SUB-LIN-PHILO              Refactorizacion PHILO. Motores EV-DIAC-VAL y EV-PALE. Sin certificacion UGR.
S003  2026-03-19  Pre-v5.0 SUB-LIN-NORM               Refactorizacion NORM. Motor EV-NORM-ANALYSIS. Sin certificacion UGR.
S004  2026-03-19  Pre-v5.0 Blindaje documental         Reescritura integra del anexo V06. V06DOC_WORD_OF_GOD revertido en S009.
S005  2026-03-19  Pre-v5.0 SUB-LIN-TRA-TECH           Refactorizacion TRA-TECH. Jerarquia errores FTI. Sin certificacion UGR.
S006  2026-03-22  Pre-v5.0 SUB-LIN-NORM bis           Nueva sesion NRA NORM. Calibracion x1.7. Sin certificacion UGR.
S007  2026-03-23  Pre-v5.0 TRA-TECH quirurgico         Reconstruccion quirurgica post-sobrescritura. Hoja de ruta reescrita.
S008  2026-03-25  Pre-v5.0 Infraestructura             Correccion AttributeError users/views.py. Resolucion OSError NFS.
S009  2026-04-19  v5.0 SUB-LIN-INSTR cert.            INICIO CERTIFICACION REAL. 12 errores corregidos. Constelacion v5.0.
S010  2026-04-20  v5.1 SUB-LIN-MINOR/PHILO/ECDO       9 lenguas MINOR. Tri-destreza PHILO. Desmembramiento ECDO. v5.1.
S011  2026-04-20  v5.1 SUB-LIN-NORM/TRA-TECH/LIT      Rama Lenguas CERRADA. SDK google-genai 1.55.0->1.73.1. v5.1.
S012  2026-04-21  v5.2 Sincronizacion + HUM Fase A    W-DOC-RESOURCES. DRA-HOLO-LIT. Arranque Humanidades. v5.2.
S013  2026-04-22  v5.3 Humanidades cert.              6 subarquetipos HUM. Rama Humanidades CERRADA. v5.3.
S014  2026-04-25  v5.4 Ciencias de la Salud cert.     18 subarquetipos SALUD. DECISION: siempre segregar. Rama CERRADA. v5.4.
S015  2026-04-26  v5.5 CSJ pasos S1-S4                9 subarquetipos Derecho+Economia.
S016  2026-04-27  v5.5 CSJ pasos S5-S10               19 subarquetipos totales CSJ. Rama CERRADA. v5.5.
S017  2026-04-28  v5.6 Ingenieria cert.               17 subarquetipos Ingenieria. Rama CERRADA. v5.6.
S018  2026-05-02  v5.7 Ciencias cert.                 SUB-SCI-DATA (fuente UCM GIDIA). Rama Ciencias CERRADA. v5.7.
S019  2026-05-11  v5.9 Auditoria Fidelidad 87/87       86 CONFORMES + 1 leve. AUTORIZADA para implementacion.
S020  2026-05-16  Resolucion TRA-LIT + Apertura        SUB-LIN-TRA-LIT resuelto. PEAs models/main.py + gemini_schemas.py.
S021  2026-05-24  Implementacion core 12/17 archivos   PEAs base.py, logic.py, factory.py, 6 strategies, tasks.py, views.py, quotas.py.
S022  2026-05-25  Implementacion cierre 17/17 archivos exam_take.html (22 widgets), exam_report.html, validate_v06_engines.py. SYNTAX OK.
S023  2026-05-26  Auditoria TLA + Certificacion        11 incidencias: 9 resueltas, 2 cerradas. ITIN_DOC certificado V06DOC_LEVELS. Modo Occidentalizacion (ja/ar/el). Selector rango verificado. Fase Implementacion CERTIFICADA. collectstatic ejecutado.
