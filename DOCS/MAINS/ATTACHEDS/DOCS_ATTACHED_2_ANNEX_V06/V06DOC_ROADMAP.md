<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_ROADMAP.md -->
# V06DOC_ROADMAP - MANIFIESTO DE CUMPLIMIENTO TÉCNICO (V1.7)

## 9. GESTIÓN DE CICLO DE VIDA (ANTI-ABUSO) - [X] 100%
- [X] Implementación del campo `expiration_date` en modelo Exam.
- [X] Sincronización de `navigation_builder.py` con el esquema V2 (Fix results_expiration_date).

## 10. AUDITORÍA DE RESILIENCIA Y CUOTA (NUEVO) - [ ] 20%
- [X] Diagnóstico de Throttling RPM vs Cuota Diaria.
- [X] Implementación de delay preventivo en orquestador (tasks.py).
- [ ] Auditoría de disparadores de cuarentena en tareas de evaluación.
- [ ] Certificación final de 22/22 motores bajo ráfaga controlada.

---
**ESTADO:** EN PAUSA PARA AUDITORÍA DE INFRAESTRUCTURA API.
