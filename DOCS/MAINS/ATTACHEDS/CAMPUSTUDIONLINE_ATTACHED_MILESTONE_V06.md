### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

**Nota para el cierre (`PCS`):** Esta sección debe ser copiada textualmente en la "Hoja de Ruta para la Siguiente Sesión" para garantizar la persistencia de la Ley.

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (DESPLIEGUE DE INTERFACES UGR)

1.  **Tarea 1 (Frontend Ciencias): Implementación de `take_assessment_sciences.html`**
    *   **Objetivo:** Soporte nativo para notación matemática (LaTeX/MathJax) en el arquetipo `LOGIC_AND_TECH`.
    *   **Acción:** Crear la plantilla específica. Integrar librería MathJax en el bloque `extra_js`. Asegurar renderizado correcto de fórmulas en enunciados y opciones.

2.  **Tarea 2 (Frontend Derecho): Implementación de `take_assessment_legal.html`**
    *   **Objetivo:** Interfaz de "Pantalla Dividida" (Split View) para el arquetipo `SOCIO_LEGAL`.
    *   **Acción:** Crear la plantilla específica. Implementar layout CSS grid/flex donde el "Supuesto de Hecho" (Reading Stimulus) permanezca fijo a la izquierda (o arriba en móvil) mientras se responde a las preguntas.

3.  **Tarea 3 (Frontend Salud): Implementación de `take_assessment_health.html`**
    *   **Objetivo:** Interfaz tipo ECOE (Estaciones Clínicas) para el arquetipo `HEALTH_SCIENCES`.
    *   **Acción:** Crear plantilla específica. Optimizar el contenedor de "Estímulo" para mostrar imágenes médicas (Radiografías/ECG) con opción de zoom/lightbox.

4.  **Tarea 4 (Backend Views): Refactorización de Contexto de Vistas**
    *   **Objetivo:** Inyectar datos específicos requeridos por las nuevas plantillas.
    *   **Acción:** Revisar `assessment/views.py` (función `take_assessment`). Asegurar que el contexto pasado a la plantilla incluya configuraciones específicas (ej: flags para activar MathJax) según el `assessment.archetype`.
