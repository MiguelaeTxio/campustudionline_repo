### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**

*A DEFINIR EN LA SESIÓN*

### PARTE MUTABLE PERO MANDATORIA EN TODOS LOS PCS

*DEPENDE DE `V06DOC_ROADMAP.md`*

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE NUKE)

## 1. RESUMEN TÉCNICO

- **EMULADOR DE ACREDITACIÓN CALIDAD UGR**

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### DOCUMENTACIÓN
- **Tarea 1:** Nuke hay que eliminar las estrategias, documentación, modelos, aplicación y todo lo referente a `assessments`. Sacar de `orchestrator` cualquier referencia a assessments. A nivel de `frontend` cuando en la sala de estudio se pulse el botón de `solicitar evaluación` saltará un modal diciendo que se está reconstruyendo y está inoperativo
- **Tarea 2:** Documentar los arquetipos de acreditación de la `UGR` según la web.
- **Tarea 3:** Documentar los subarquetipos de acreditación de cada arquetipo de la `UGR`.
- **Tarea 4:** Documentar todas las subdivisiones de cada arquetipo.
- **Tarea 5:** Documentar todos los bloques que pertenezcan a una subdivisión.
- **Tarea 6:** Documentar todos los widgets que pertenezcan a una subdivisión.
- **Tarea 7:** Documentar todas las etiquetas que intervengan en cada subdivisión.
- **Tarea 8:** Documentar todos los niveles pedagógicos de cada subdivisión.
- **Tarea 9:** Documentar todas las plantillas que se deben generar para todos y cada uno de los arquetipos.
- **Tarea 10:** Documentar la estructura de archivos segregada que se va a seguir, la orquestación que dependerá de `orchestrator` fijar la directriz de carga de los documentos obligatorios y la carga selectiva dependiente de la tarea a realizar.

### RESUMEN DE ARCHIVOS DE DOCUMENTACIÓN

*   ANEXO PROPIAMENTE DICHO (ESTE DOCUMENTO CON LA DIRECTRIZ DE CARGA OBLIGATORIA Y LA SELECTIVA)
*   DIRECTORIO: `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/`
*   NOMENCLATURA: `V06DOC_{NAME}.md`

##### CARGA OBLIGATORIA (UNA VEZ DEFINIDOS EN ESTA SESIÓN DEBEN QUEDAR REFLEJADOS EN LA PARTE INMUTABLE)

*   **ESTRUCTURA:** {NAME} = `STRUCTURE`
*   CONTIENE:
*   *    MODELOS.
*   *    ESTRUCTURA DE ARCHIVOS.
*   *    ARQUITECTURA DE SOFWARE.
*   *    RESUMEN GENERAL DEL HITO.
*   *    LISTA DE DOCUMENTACIÓN DE CARGA OBLIGATORIA.
*   *    LISTA DE DOCUMENTACIÓN DE CARGA SELECTIVA.
*   **HOJA DE RUTA:** {NAME} = `ROADMAP`
*   CONTIENE EL ÁRBOL DE TAREAS PARA IR TACHANDO:
*   *    EJEMPLO:{ARCH01}{SUBARCH01}{WIDGET01}[X]
*   *    {ARCH01}{SUBARCH01}{TEMPLATE01}[X]
*   **ARQUETIPOS:** {NAME} = `ARCHETYPES`
*   CONTIENE UN RESUMEN DE TODOS LOS ARQUETIPOS Y SUS SUBARQUETIPOS. TODO ARQUETIPO DEBE TENER AL MENOS UN SUBARQUETIPO
*   **BLOQUES:** {NAME} = `BLOQS`
*   CONTIENE TODOS LOS TIPOS DE BLOQUES Y DESTREZAS QUE SE PUEDEN APLICAR EN UN EXAMEN.
*   **COMPONENTES:** {NAME} = `WIDGETS`
*   CONTIENE TODOS LOS TIPOS DE WIDGETS QUE PUEDEN APARECER.
*   **NIVELES:** {NAME} = `LEVELS`
*   CONTIENE TODOS LOS NIVELES PEDAGÓGICOS QUE PUEDAN EXISTIR PARA CADA ARQUETIPO Y SU INLUENCIA.
*   **SUBDIVISIONES:** {NAME} = `SUBDIVISIONS`
*   CONTIENE TODAS LAS SUBDIVISIONES O ITINERARIOS Y SU INFLUENCIA

##### CARGA SELECTIVA

*   **PLANTILLAS:** {NAME} = `TEMPLATES_{SUBARCHE}_{TYPE}`
*   CONTIENE LA ESTRUCTURA DE LA PLANTILLA Y SUS ELEMENTOS DEPENDIENDO DEL TIPO DE PLANTILLA(A REALIZAR O CORREGIDA)
*   **SUBARQUETIPOS:** {NAME} = `SUBARCHE_{ARCHE_NAME}[00..99]{SUBARCHE_NAME}`
*   CONTIENE EL DETALLE DE TODOS LOS ELEMENTOS QUE LO FORMAN.