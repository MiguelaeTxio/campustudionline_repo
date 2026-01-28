### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

---

### HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (ESTADO DE FALLO DE PERSISTENCIA ATÓMICA)

**Estado Actual:** CRÍTICO. El blindaje SQL directo (`.update()`) ha fallado en persistir el diccionario `questions_cache`. El sistema sigue reiniciando desde el ítem 1 al no encontrar datos en la caché al recuperar la tarea.

**Tarea 1: Diagnóstico de Escritura SQL Directa**
- **Acción:** Verificar mediante scripts de shell si el comando `Assessment.objects.filter(id=assessment_id).update(prompt_data=p_data)` realmente modifica el registro en la base de datos MySQL de PythonAnywhere durante la ejecución de la tarea.

**Tarea 2: Análisis de Hidratación de Objetos en Celery**
- **Acción:** Investigar si el worker de Celery está trabajando con una instancia cacheada del objeto `Assessment` que ignora los cambios realizados por `.update()` en otros procesos o si el campo JSON se corrompe al serializarse.

**Tarea 3: Implementación de Persistencia Física (JSON File)**
- **Acción:** Como medida de contingencia absoluta, considerar el volcado del progreso a un archivo físico `.json` en el sistema de archivos del servidor, omitiendo la base de datos para la caché de preguntas.
