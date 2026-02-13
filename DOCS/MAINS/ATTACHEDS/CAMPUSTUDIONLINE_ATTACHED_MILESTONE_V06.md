### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse con los siguientes documentos para garantizar el contexto completo del Estándar de Máxima Calidad:
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

### PARTE MUTABLE PERO MANDATORIA EN TODOS LOS PCS

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE 3: INFRAESTRUCTURA BASE COMPLETADA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN
Se ha instalado la infraestructura común para todos los subarquetipos:
*   **Señalización (Badges):** Implementado `BadgeService` y `context_processor`. Los badges se integraron en el NavBar (dentro de "Sala de Estudio") para dar feedback de estados (Generando/Listo).
*   **Motor de Seguimiento (Tracking):** Creado `TrackingService` e implementados modelos `TokenUsage` y `CostLog`. La tarea Celery ya registra el consumo de tokens y el coste estimado.
*   **Contrato Pedagógico:** Creada la clase abstracta `BaseExamStrategy` y sincronizada la `ExamFactory`.
*   **UX de Selección:** Implementado el filtrado de metadatos/H1 en la TOC (`utils.py`) y la lógica de restricción de rangos en el frontend (`exam_create.html`).

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
Objetivo: Reparación Administrativa y Consolidación del Engine.

### TAREAS CRÍTICAS (ORDEN OBLIGATORIO)
1.  **Reparación del Admin (Glitch Visual):**
    *   Limpiar `templates/admin/base_site.html` eliminando el texto `class="button">` que se renderiza por un comentario mal cerrado.
    *   Restaurar el acceso al "Motor" (Planes/Cuotas) apuntando el botón a la lista de aplicaciones de `assessment_v2`.
2.  **Evolución del Engine (`BaseExamStrategy`):**
    *   Implementar el método `generate_structure()` en la clase base para que fabrique el esqueleto JSON del "Exam Contract".
3.  **Refactorización de Tarea Celery:**
    *   Asegurar que `generate_exam_task` instancie la estrategia correcta y use `generate_structure` para el prompt.
4.  **Integración de Badges en SideBar:**
    *   Modificar `contents/templates/contents/partials/_navigation_sidebar.html` para replicar los indicadores del NavBar.
5.  **Desarrollo del Dashboard de Exámenes:**
    *   Crear la vista de lista en `assessment_v2` para que el usuario gestione sus evaluaciones previas.

---
