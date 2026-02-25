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
# ESTADO: MOTOR DE PLANTILLAS "PYTHON-DICTATOR" IMPLEMENTADO AL 70%

### PARTE MUTABLE (RESUMEN TÉCNICO Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (CAMA)
*   **Re-arquitectura del Orquestador:** Se ha modificado `orchestrator/tasks.py` para cumplir el estándar "Skeleton-First". El servidor ahora crea el esqueleto completo de Secciones e Ítems vacíos en la BBDD antes de invocar a la IA. La generación es atómica por sección para evitar errores de truncamiento.
*   **Blindaje de Calidad:** Implementada lógica de reintento (`self.retry`) en el orquestador. Si la IA falla, no se entregan "ítems vacíos"; se reintenta la generación y, tras agotar intentos, se notifica al administrador y al usuario.
*   **Mapa Maestro UGR V5.0:** Actualizado `V06DOC_SUBARCHETYPES.md` con 45 modelos de examen reales tras auditar las guías docentes de la UGR.
*   **Implementación de Estrategias:**
    *   `languages.py`: Implementados 6 modelos (Instrumental, Filológico, Literario, Minor, Traducción T/L).
    *   `health.py`: Implementados 10 modelos (Medicina C/B, Odonto, Fisio, Cuidados, Lab, Psy C/E, VET, NUT).
    *   `social.py`: Implementados 10 modelos (Derecho P/D, Econ Q/M, Edu K/S, Jour, AV, Geog, Work).

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**OBJETIVO: CIERRE DE LA FASE DE ESTRATEGIAS Y FRONTEND**

### I. FINALIZACIÓN DE ESTRATEGIAS (LOS 45 MODELOS)
1.  **Humanidades:** Consolidar `humanities.py` con sus 6 modelos (HIST, PHIL, ART-HIST, ART-CREA, MUS, ANTH) usando un bloque de escritura limpio.
2.  **Ciencias:** Crear `science.py` e implementar los 6 modelos restantes (BIO, CHEM, PHYS, GEOL, ENV, DATA).
3.  **Clasificador:** Revisar `AcademicDeductor` para asegurar que el mapeo de asignaturas apunta correctamente a los nuevos subarquetipos inmutables.

### II. FASE FRONTEND
1.  Aplicar parche en `assessment_v2/templates/assessment_v2/exam_take.html` para habilitar el panel lateral (`SPLIT_TEXT`) y decodificar el `section_stimulus` para lecturas y casos prácticos.

### III. VALIDACIÓN TÉCNICA
1.  Generar un examen de "Chino Minor" y un "Derecho Procesal" para verificar que los esqueletos son distintos y la inyección de contenido es correcta.
