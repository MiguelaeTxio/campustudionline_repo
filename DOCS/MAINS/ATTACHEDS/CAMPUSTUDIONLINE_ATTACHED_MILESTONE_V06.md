### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (ESTADO DE FALLO CRÍTICO)

**Estado Actual:** CRÍTICO. El sistema de autoevaluaciones se encuentra totalmente roto. Las tres implementaciones de lógica de persistencia y reanudación (V1, V2 y V3) en `orchestrator/tasks.py` han fallado en erradicar el bucle de reinicio infinito. Tras cada error de cuota, el sistema reinicia la generación desde el ítem 1/17, resultando en un sistema inoperativo para esta funcionalidad.

**Tarea 1: Auditoría Técnica del Ciclo de Vida de Tareas**
- **Acción:** Análisis forense del flujo en `generate_assessment_from_content_task`.
- **Objetivo:** Identificar el fallo estructural en el código entregado que ignora los guardados de base de datos y provoca la regeneración sistemática del esqueleto de la evaluación.

**Tarea 2: Análisis de Persistencia Atómica**
- **Acción:** Revisar si el manejo de excepciones está provocando rollbacks involuntarios que anulan el progreso de `questions_processed` a pesar de los comandos `save()`.

**Tarea 3: Depuración de Tareas Zombie**
- **Acción:** Limpieza de registros y tareas huérfanas en Celery y Base de Datos resultantes de las implementaciones fallidas.
