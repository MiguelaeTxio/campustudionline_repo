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
# ESTADO: RECONSTRUCCIÓN ESTRUCTURAL COMPLETADA - FALLO EN CORE DETECTADO

### PARTE MUTABLE (RESUMEN TÉCNICO Y HOJA DE RUTA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN (NRA)
*   **Sincronización Doc-Impl:** Se ha resuelto la desalineación entre la documentación V06 y el código. Los documentos satélites ahora definen `section_stimulus` y `layout_mode` para gestionar estímulos inéditos (Readings) en lugar de apuntes.
*   **Fix Orquestador y Estrategias:** Reparado el orden de parámetros en `tasks.py`, el crash por atributo inexistente en `TechnicalStrategy` y el silenciamiento de errores en la generación asíncrona.
*   **Controlador UI Secuencial:** Implementado motor de estaciones en `exam_take.html` con aislamiento de secciones y temporizadores dinámicos.
*   **Diagnóstico de Bloqueo:** El sistema falla por una incompatibilidad de firma en `core/services/gemini_service.py` al no aceptar el argumento `response_schema`.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**OBJETIVO: DEPURACIÓN DEL CORE GEMINI Y VALIDACIÓN DE FLUJO ATÓMICO**

### I. FASE DE REPARACIÓN DEL CORE
1.  **Auditoría del Servicio Core:** Analizar y modificar `core/services/gemini_service.py` para añadir soporte al argumento `response_schema` en la función `generate_text_content`.

### II. FASE DE PRUEBA DE CARGA (END-TO-END)
1.  Lanzar la generación de un examen de Lenguas y verificar que Gemini genera el `section_stimulus` (Reading) integrándolo en el JSON.
2.  Validar en el frontend que el panel lateral dinámico muestra correctamente el texto generado por la IA.
