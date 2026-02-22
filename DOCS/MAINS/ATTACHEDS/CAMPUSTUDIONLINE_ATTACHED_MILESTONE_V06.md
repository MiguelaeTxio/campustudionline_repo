{# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md #}
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
# ESTADO: EN PROGRESO (AUDITORÍA DE RESILIENCIA)

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (EPI)
*   **Validación de Motores:** Se ejecutó el comando de gestión `validate_v06_engines` logrando validar 19 de los 22 motores académicos sobre asignaturas reales de la UGR.
*   **Reparación de Navegación:** Corregido error de regresión en `navigation_builder.py` donde se intentaba filtrar por un campo inexistente (`results_expiration_date` -> `expiration_date`).
*   **Blindaje RPM:** Inyectado un retraso de seguridad (`time.sleep(5)`) en `orchestrator/tasks.py` para mitigar el bloqueo por frecuencia (RPM) en la generación de ítems.
*   **Hallazgo Crítico:** Se identificó una asimetría en la gestión de resiliencia; la tarea de exámenes no activa automáticamente la cuarentena (`is_quarantined`) de las API Keys tras un error 429, a diferencia del generador de cursos.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**AUDITORÍA INTEGRAL DE CUARENTENA Y ROTACIÓN:**

1.  **AUDITORÍA DE LÓGICA DE RESILIENCIA:** Analizar comparativamente `generate_full_course_task` y `generate_exam_task` para asegurar que el "castigo" a llaves agotadas sea uniforme en toda la plataforma.
2.  **UNIFICACIÓN DE DISPARADORES:** Implementar la marcación de `is_quarantined = True` en el motor de exámenes tras detectar errores `RESOURCE_EXHAUSTED`.
3.  **VALIDACIÓN DE PLENO (22/22):** Re-ejecutar el comando de gestión con las asignaturas afinadas (SUB-LIN-LIT, SUB-SAN-CUID, SUB-HUM-HIST) para certificar el 100% de los subarquetipos tras la auditoría de rotación.
4.  **CONTROL DE RÁFAGAS:** Ajustar el orquestador para manejar el Throttling por minuto de Google sin quemar innecesariamente el pool de llaves.

---
