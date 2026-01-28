### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (DEPURACIÓN CRÍTICA FASE A/B)

**Estado Actual:** INESTABLE. El sistema ha sido estabilizado respecto a errores de referencia local (`UnboundLocalError`) y sintaxis de imports. Sin embargo, la generación atómica falla en la creación del esqueleto (Fase A) debido a una inconsistencia de claves entre el orquestador y la estrategia.

**LOG DE ERROR PARA ANÁLISIS:**
`2026-01-28T06:26:36 ERROR ERROR FATAL: 'label'`
`2026-01-28T06:26:36 INFO PASO 2 (Generación Atómica) - CEFR_LANGUAGES`

**Tarea 1: Armonización de Claves de Diccionario (Fix KeyError)**
- **Acción:** Modificar la función `_create_assessment_skeleton` en `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/orchestrator/tasks.py`.
- **Causa:** El orquestador busca `q_data['label']`, pero la nueva estrategia `languages_strategy.py` entrega `section_label`.
- **Solución:** Implementar acceso seguro mediante `.get()` con fallbacks para todas las claves estructurales (`section_label`, `source_type`, `interaction_type`, `response_mode`).

**Tarea 2: Verificación de Densidad UGR (17 ítems)**
- **Acción:** Tras el fix de claves, ejecutar `verify_ugr_flow.py` y confirmar que se crean 17 preguntas para el itinerario MINOR.

**Tarea 3: Auditoría de Inmersión Lingüística**
- **Acción:** Verificar que en el Paso 2 (Fase B), las instrucciones se generan en castellano para niveles MINOR, respetando la Ley Técnica UGR.
