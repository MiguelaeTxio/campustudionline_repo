### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse OBLIGATORIAMENTE con la siguiente constelación documental:
*   V06DOC_ARCHETYPES.md
*   V06DOC_SUBARCHETYPES.md
*   V06DOC_SUBDIVISIONS.md
*   V06DOC_BLOCKS.md
*   V06DOC_WIDGETS.md
*   V06DOC_METADATA.md
*   V06DOC_LEVELS.md
*   V06DOC_TEMPLATES.md
*   V06DOC_STRUCTURE.md
*   V06DOC_LOGIC_MAPPING.md
*   V06DOC_ROADMAP.md

**PROTOCOLO DEL MANIFIESTO (FUENTE DE LA VERDAD):**
El archivo V06DOC_ROADMAP.md es la ÚNICA fuente de verdad para el progreso. 
1. Es OBLIGATORIO auditar este archivo al inicio de cada sesión.
2. Es MANDATORIO actualizar su estado atómico (Checklist) al cierre de cada sesión.

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (AUDITORÍA DE RESILIENCIA Y VALIDACIÓN FINAL)

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (EPI)
*   **Restauración Crítica (Hotfix):** Se recuperó quirúrgicamente la función `_safe_generate_content` y la infraestructura de buzón de cuarentena en `orchestrator/tasks.py`, perdidas en una refactorización anterior.
*   **Blindaje de Cuota:** Implementada la detección de error 429 (`ResourceExhausted`) y la activación automática de `is_quarantined=True` en tiempo real, forzando la rotación de API Keys sin abortar la tarea.
*   **Cobertura Total:** El blindaje se ha aplicado tanto a la generación de cursos (`generate_full_course_task`) como a la de exámenes (`generate_exam_task`).

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**VALIDACIÓN FINAL DE MOTORES (22/22):**

1.  **CORRECCIÓN DE NOMINALES:** Editar `assessment_v2/management/commands/validate_v06_engines.py` para corregir los nombres de las 3 asignaturas que fallaron en la prueba anterior (`SUB-LIN-LIT`, `SUB-SAN-CUID`, `SUB-HUM-HIST`).
2.  **EJECUCIÓN DE VALIDACIÓN:** Ejecutar `python manage.py validate_v06_engines` hasta certificar el éxito en los 22 subarquetipos.
3.  **AUDITORÍA DE LOGS:** Verificar en `tasks.log` o `event_log` que la rotación de claves funciona correctamente bajo carga.
4.  **CIERRE DE HITO:** Finalizar la auditoría y marcar el Hito 06 como completado.

---
