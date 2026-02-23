# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
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
# ESTADO: FALLO SISTÉMICO - AUDITORÍA INTEGRAL REQUERIDA

### PARTE MUTABLE (RESUMEN Y HOJA DE RUTA DE AUDITORÍA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (EDC)
*   **Ajustes de Infraestructura:** Corregidas las firmas de métodos en `tasks.py` para eliminar el `TypeError` y actualizados los esquemas de respuesta de la IA con `anyOf` para soportar tipos de datos mixtos en `correct_answer`.
*   **Saneamiento de Logs:** Silenciados los avisos de `bleach` mediante la implementación de `CSSSanitizer`.
*   **Identificación del Desastre:** Se ha constatado una ruptura total entre la especificación documental (`V06DOC_*`) y el resultado de la implementación, resultando en un examen genérico, vacío y con una UI que ignora la mecánica de estaciones secuenciales.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**OBJETIVO: AUDITORÍA INTEGRAL DE DESALINEACIÓN (DOCUMENTACIÓN VS IMPLEMENTACIÓN)**

### I. FASE DE DIAGNÓSTICO DE CAUSA RAÍZ
1.  **Auditoría de Lógica de Negocio:** Analizar por qué el motor ignora los parámetros `itinerary_id` y `pedagogical_level` al construir el plan de secciones en `get_section_plan`.
2.  **Rastreo de Persistencia Atómica:** Investigar el proceso de guardado de `ExamItem`. Determinar si la IA no está generando los ítems (fallo de prompt) o si el orquestador no los está persistiendo en la BBDD (fallo de código).
3.  **Análisis de la UI "Plana":** Identificar por qué `exam_take.html` ignora el arquetipo `ARCH_LANG` (Estaciones secuenciales bloqueantes) y presenta un formulario lineal prohibitivo.

### II. MAPEO DE DISCREPANCIAS
1.  Comparar punto por punto `V06DOC_ARCHETYPES` contra las clases en `assessment_v2/services/engine/strategies/`.
2.  Comparar `V06DOC_TEMPLATES` contra el contenido real de los `JSONField` en la tabla `assessment_v2_examitem`.
3.  Evaluar la inyección de contexto: ¿Por qué el Repositorio Académico lateral no recibe el material de estudio original?

### III. PLAN DE DEMOLICIÓN Y RECONSTRUCCIÓN
1.  Definir los cambios necesarios para que la documentación satélite actúe como **Única Fuente de Verdad** durante la ejecución del código.
2.  Establecer los puntos críticos de control para que el examen no pase a estado 'READY' si no cumple con la estructura de la constelación V06.

---
**ESTADO TÉCNICO:** Auditoría integral obligatoria antes de cualquier intento de reparación de código.
