### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

**Nota para el cierre (`PCS`):** Esta sección debe ser copiada textualmente en la "Hoja de Ruta para la Siguiente Sesión" para garantizar la persistencia de la Ley.

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (RECONSTRUCCIÓN DEL EMULADOR UGR)

**Estado Actual:** INESTABLE. Se ha reparado el `ImportError` y actualizado la Ley Técnica (Inmersión Progresiva), pero la implementación técnica de la universalidad de idiomas ha fallado por errores en los scripts de parcheo (`re.error: bad escape \s`). Celery probablemente persiste en un ciclo de reinicio (Tarpit) debido a un `TypeError` en `assessment/tasks.py`.

**Tarea 1: Estabilización del Entorno (Freno al Tarpit)**
- **Acción:** Corregir manualmente la firma de la función `generate_languages_item_prompt` en `assessment/tasks.py` para que acepte el argumento `itinerary`. Esto detendrá el consumo de CPU.
- **Validación:** Ejecutar `python manage.py shell -c "import assessment.tasks"` hasta que el resultado sea `OK`.

**Tarea 2: Implementación Universal (Languages Strategy)**
- **Acción:** Aplicar la refactorización de `languages_strategy.py` usando `PEA` (Entrega de Archivo Completo) para evitar fallos de regex.
- **Objetivo:** Extracción dinámica del idioma objetivo y esqueletos de 17 (MINOR) y 36 (MAIOR) ítems.

**Tarea 3: Sincronización de Itinerarios**
- **Acción:** Refactorizar el orquestador global para que la detección del itinerario sea jerárquica y se persista antes de la generación de ítems.

**Tarea 4: Auditoría de Resultados**
- **Acción:** Generar una evaluación para una asignatura MINOR (ej. Chino Inicial) y otra MAIOR para verificar que la inmersión lingüística se comporta según la nueva Ley Técnica.
