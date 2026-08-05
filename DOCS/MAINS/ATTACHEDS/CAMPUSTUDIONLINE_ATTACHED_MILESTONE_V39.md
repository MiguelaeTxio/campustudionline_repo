# Hito 39 — Motor de Refinamiento por IA para Ítems PENDING_AI_ANALYSIS

---

## 1. Objetivo del Hito

Sustituir el placeholder heurístico fijo (`Decimal('0.6')`,
`pending_ai_refinement: True`) que devolvían siempre los motores
`DRA-HOLO`, `ILC-CONTEXT` y `DIA-INTERACT` por una corrección real,
generada por IA, del contenido efectivamente entregado por el alumno —
sin degradar la experiencia de "Finalizar Evaluación" con llamadas
síncronas a Gemini.

Hallazgo original: S028 (durante H06), ampliado en S029 al confirmar que
`ILC-CONTEXT` es un cuarto motor afectado, transversal a cuatro
arquetipos (no solo `DIA-INTERACT`/`DRA-HOLO` en tres). Acordado con
Miguel Ángel como hito propio — no tarea suelta de H06 — el 2026-08-05
(S029), tras construir y verificar el motor en sí como desvío dentro de
esa misma sesión, tras desbloquear con él el PASO 4 de H06.

---

## 2. Contexto Técnico

### 2.1. Estado real al abrir este hito (S029)

El motor **ya está construido y verificado end-to-end contra datos
reales de producción** — no es un hito que arranque de cero:

- `assessment_v2/services/engine/logic.py`:
  `GradingOrchestrator.recompute_aggregate_scores(submission)` — recalcula
  `section_scores`/`final_score`/`passed`/`qualitative_summary` a partir
  de un `grading_report` ya persistido con ítems refinados, sin reejecutar
  toda la estrategia de calificación (evita efectos secundarios sobre
  ítems ya calificados correctamente por el motor determinista original).
- `orchestrator/tasks.py`:
  - `REFINEMENT_RESPONSE_SCHEMA` — esquema estructurado (`score`,
    `justification`) para la respuesta de Gemini.
  - `_build_refinement_prompt(block_type, item, student_input, item_report)`
    — construye el prompt real de corrección según el tipo de bloque.
    Reutiliza la misma extracción de `student_input` que
    `GradingOrchestrator.grade_submission` (contrato `raw_input`).
  - `refine_pending_ai_items_task(submission_id)` — tarea Celery,
    cola `high_priority` (misma que `generate_exam_task`), `max_retries=2`.
    Recorre todos los ítems `pending_ai_refinement=True` del informe,
    llama a `generate_text_content` con el esquema estructurado, actualiza
    el informe in situ y dispara `recompute_aggregate_scores` +
    notificación si hubo algún refinamiento real.
  - `_send_grading_refinement_notification(submission)` — push + email,
    calca el patrón **probado** de `_send_completion_notifications` (no
    el patrón roto de `send_unified_notification`, ver Sección 4).
- `orchestrator/templates/orchestrator/email/grading_refinement_complete.html`
  — plantilla de email nueva.
- `core/settings.py`: `CELERY_TASK_ROUTES['orchestrator.tasks.
  refine_pending_ai_items_task'] = {'queue': 'high_priority'}`.
- `assessment_v2/views.py`: `ExamSubmitView` encola la tarea vía
  `transaction.on_commit` (evita condición de carrera con Celery) solo si
  quedó algún ítem pendiente tras la calificación síncrona;
  `ExamReportView` expone `has_pending_refinement` al contexto.
- `assessment_v2/templates/assessment_v2/exam_report.html`: banner de
  "revisión en curso" (con aviso explícito de que el alumno puede
  abandonar la página) + marca visual por ítem individual aún pendiente.

### 2.2. Decisión de diseño clave: `DIA-INTERACT` es texto, no audio

`_grade_dia_interact` (`base.py`) y la recolección real del frontend
(`widgetState.chatLogs[itemId]`, `exam_take.html`) confirman que la
interacción dialéctica se envía como **texto** (log de chat), no como
grabación de audio — pese a que `generate_multimodal_correction`
(`gemini_service.py`, ya existente desde Hito 6) sugería una vía
multimodal de audio. El widget de "Grabación de Respuesta Oral" visible
en pantalla existe en la UI pero **no se recoge ni se envía en el
payload real** — es una vía muerta, no conectada a `DIA-INTERACT`.
Confirmado por lectura de código real, no por suposición.

Consecuencia: el motor de refinamiento de este hito usa un único camino
de texto (`generate_text_content` con `response_schema`) para los tres
tipos (`DRA-HOLO`, `ILC-CONTEXT`, `DIA-INTERACT`) — no necesita la vía
multimodal de audio en absoluto.

### 2.3. Alcance real de `ILC-CONTEXT` (ampliación S029)

`_grade_ilc_context` (`base.py`) lo usan CUATRO estrategias, no tres:
`health.py` (ARCH_HEALTH, vía `W-CLIN-SCAN`), `science.py` (ARCH_SCI),
`social.py` (ARCH_SOC) y `tech.py` (ARCH_TECH). El motor construido en
S029 cubre `ILC-CONTEXT` de forma genérica (no está acoplado a un
arquetipo concreto), pero **solo se ha verificado en caliente contra un
ítem `DRA-HOLO`** (examen `74407b97`, item 228). Falta verificar
`ILC-CONTEXT` y `DIA-INTERACT` con datos reales — ver hoja de ruta.

### 2.4. Migración de modelo Gemini (hallazgo colateral S029)

Durante la verificación de este motor se descubrió que `gemini-2.5-flash`
devolvía 404 real ("no longer available to new users") — apagado
anticipado de Google confirmado con múltiples fuentes externas
independientes, afectando a TODA la plataforma (`GEMINI_MODEL_NAME` es
una constante global en `core/services/gemini_service.py`). Migrado a
`gemini-3.5-flash`. No es un asunto propio de este hito, pero el cambio
de modelo se hizo en el curso de verificarlo — mencionado aquí por
completitud, el hallazgo y la corrección viven documentados en el anexo
de H06 (S029).

---

## 3. Hoja de Ruta (ejecutable de forma autónoma)

**PASO 1 — Verificación E2E con examen generado desde cero.**
La verificación de S029 reutilizó una `Submission` ya existente de una
sesión anterior (examen `74407b97`, ítem `DRA-HOLO`). Falta generar un
examen nuevo, completo, con al menos un ítem `DRA-HOLO` respondido con
contenido real (no gibberish), enviarlo, confirmar que
`refine_pending_ai_items_task` se encola automáticamente vía
`transaction.on_commit`, que el banner de "revisión en curso" aparece en
`exam_report.html`, y que la notificación push+email llega de verdad al
terminar.

**PASO 2 — Verificar `ILC-CONTEXT` con datos reales.**
Generar un examen con un ítem `ILC-CONTEXT` real (p. ej. `SUB-SAN-MED-
BASIC` vía `W-CLIN-SCAN`, ya verificado E2E en H06 hasta la generación),
responderlo con interpretación real, y confirmar que el refinamiento
produce una nota y justificación coherentes — no solo que no falle.

**PASO 3 — Verificar `DIA-INTERACT` con datos reales.**
Generar un examen con un ítem `DIA-INTERACT`, mantener una interacción de
chat real con UniversIA, enviarlo, y confirmar el refinamiento con el
`chat_log_preserved` real.

**PASO 4 — Decidir el destino del widget de audio no conectado.**
El botón "Grabación de Respuesta Oral" existe en la UI de
`DIA-INTERACT` pero no se envía ni se usa. Decidir con Miguel Ángel: (a)
retirarlo de la UI por no estar conectado a nada, (b) conectarlo de
verdad usando `generate_multimodal_correction` (ya existe) como una
mejora futura del motor de este hito, o (c) dejarlo documentado como
deuda técnica aparte y no tocarlo. No decidir unilateralmente.

**PASO 5 — `send_unified_notification` roto (deuda técnica heredada de H06).**
`_send_exam_failure_notification` (`orchestrator/tasks.py`) llama a
`send_unified_notification` (`core/utils.py`) con una firma que no
coincide con la función real, y con nombres de URL de la app `assessment`
legacy (`assessment:view_results`) en vez de `assessment_v2`. Falla
silenciosamente cada vez, envuelta en el `try/except` de la función — el
push de fallo de examen nunca llega, aunque el email sí. No corregido
todavía. Encontrado en S029 mientras se construía
`_send_grading_refinement_notification` (que usa el patrón probado de
`_send_completion_notifications` en su lugar, no este). Corregirlo aquí o
en H06, a decidir con Miguel Ángel cuando se retome.

---

## 4. Notas de Verificación (S029)

- `refine_pending_ai_items_task(20)` ejecutada directamente (no vía
  `.delay()`) contra la `Submission 20` real: primer intento reveló el
  404 de `gemini-2.5-flash`; tras migrar a `gemini-3.5-flash`, segundo
  intento devolvió HTTP 200 real y el ítem 228 quedó `GRADED` con
  justificación real de la IA sobre la respuesta del alumno
  ("Jjmbvcgj" → nota 0.0, justificación coherente).
- `_send_grading_refinement_notification` verificada de forma aislada
  tras corregir el `NameError` (ver Sección 2.4 del anexo H06, S029):
  push enviado con éxito a la mayoría de suscripciones reales, email
  aceptado por MailerSend (202). Dos fallos de push preexistentes y no
  relacionados quedaron anotados en la deuda técnica de H06 (S029), no
  de este hito.
