# /home/MiguelAeTxio/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/HITO_V18_GENERADOR_CONTENIDO_ANEXO.md
**Título:** Anexo de Seguimiento: Hito de Re-arquitectura v18 - Estrategia de Guías Docentes (COMPLETADO)

**Filosofía:** Este documento es la única fuente de verdad para la planificación, ejecución y seguimiento del hito de re-arquitectura del generador de contenido. Se actualizará al final de cada sesión de trabajo para reflejar el progreso real.

---

#### **1. Visión General del Hito**

El objetivo de este hito es re-arquitecturizar el sistema de generación de contenido para que se base en la extracción de datos estructurados de las guías docentes de la UGR. El nuevo flujo de trabajo consistirá en tres etapas principales:
1.  **Extracción y Persistencia:** Un conjunto de herramientas locales y comandos de Django extraerán los `inputs` clave (Objetivos, Contenido Bruto, Bibliografía de la Guía) de los PDFs y los persistirán en la base de datos de la plataforma.
2.  **Generación Asistida por IA:** La IA utilizará estos `inputs` para generar un `master_schema` y, posteriormente, el contenido de cada sección individual, incluyendo las fuentes bibliográficas específicas que utilice para cada una.
3.  **Ensamblaje Inteligente:** El contenido final se ensamblará de forma estructurada, con una sección de "Fuentes y Bibliografía" compilada a partir de las fuentes proporcionadas por la IA para cada sección.

---
#### **2. Estado General Actual (Post-FASE 1)**
**La FASE 1 ha sido completada con éxito.** Se ha diseñado, implementado y ejecutado una tubería de datos (`data pipeline`) completa para la extracción, transformación y carga (ETL) de 4507 guías docentes. El proceso, orquestado por los scripts locales `ugr_scraper.py`, `guide_parser.py` y `transform_ugr_data.py`, ha generado el `dataset` final (`ugr_data_cleaned.json`). Posteriormente, el comando de gestión `import_ugr_data --purge` ha poblado la base de datos de la plataforma con esta información detallada. **La base de datos se encuentra en un estado íntegro y lista para la siguiente fase.**

---

#### **2.1. Descubrimiento Crítico y Re-priorización (Post-FASE 5)**
**Se ha detectado un fallo arquitectónico fundamental que invalida el estado actual de la generación de contenido.** Una "Auditoría Arqueológica" con `git` ha revelado que la conexión original y universal entre el contenido académico (`Subject`) y el intelectual (`Topic`) a través de un `ForeignKey` en `ContentMaterial` se perdió en una refactorización anterior.

**Impacto:** El sistema actual crea contenido "huérfano" que rompe la lógica de la plataforma.

**Acción Inmediata:** La finalización de este hito queda **bloqueada** hasta que la arquitectura universal de contenido sea restaurada. La próxima sesión se dedicará por completo a esta tarea crítica.

---

#### **2.2. Resolución de Bloqueo y Re-calibración de Estrategia (Sesión Actual)**
**El bloqueo arquitectónico ha sido resuelto con éxito.** Se ha completado la misión crítica de restauración, verificando que los modelos (`ContentMaterial`), la lógica de negocio (`tasks.py`) y las señales (`signals.py`) están correctamente alineados con la arquitectura universal de contenido.

Una prueba de validación de extremo a extremo, generando el curso "Anatomía e Histología Humanas", demostró que la infraestructura es robusta y funcional. Sin embargo, también reveló que la estrategia de prompts actual otorga demasiada libertad creativa a la IA, resultando en un `master_schema` que no se alinea fielmente con el alcance de la guía docente.

**Acción Inmediata:** La próxima sesión se centrará en una refactorización quirúrgica de los prompts para forzar una adherencia estricta al temario y a los objetivos de aprendizaje de la guía, pasando de un modelo de "creación" a uno de "transposición pedagógica".

---

#### 2.3. Validación Final y Cierre del Hito (Sesión Actual)
**La nueva arquitectura simplificada ha sido validada con éxito mediante la generación completa y sin errores del curso 'Álgebra II'.** El sistema ha demostrado ser robusto y resiliente, superando los fallos transitorios de la IA sin errores de parseo.

****El Hito 18 ha sido completado con éxito.** Se ha verificado la correcta escritura de logs enriquecidos, se ha implementado la interfaz de gestión de archivos de log en el panel de administración y se han corregido todos los errores residuales que bloqueaban su cierre.** La nueva arquitectura del generador de contenido se declara estable y finalizada.

---


#### **2.5. Cierre del Hito y Estabilización Final (Sesión 2025-11-28)**
**HITO COMPLETADO.**

Se han resuelto todos los bloqueos técnicos y lógicos que impedían la operación continua del sistema.
**Logros Clave:**
*   **Orquestador Resiliente:** Implementación de "Autolimpieza de Zombies" y detección de errores lógicos fatales para evitar bucles infinitos.
*   **Contenido Libre Funcional:** Corrección de formularios HTMX, validación dinámica, recuperación de clasificación y deduplicación de contenido.
*   **Interfaz Desbloqueada:** Simplificación del admin para permitir la gestión manual de categorías y corrección de errores en plantillas de usuario.
*   **Visibilidad:** Corrección del bug que dejaba el contenido oculto tras la generación.

El sistema de generación masiva está ahora operativo y estable.

#### **3. Hoja de Ruta Detallada del Hito**

A continuación, se desglosa el hito en fases y tareas específicas, indicando el estado actual de cada una.

**FASE 1: Extracción y Preparación de Datos (`Inputs` para la IA)**

*   **Tarea 1.1: Finalizar el Parser de Guías Docentes (`guide_parser.py`)**
    *   **Descripción:** Implementar las expresiones regulares definitivas y robustas para extraer los tres bloques de texto (Objetivos, Contenido Bruto, Bibliografía de la Guía) del texto completo de un PDF.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 1.2: Estructurar la Salida del Parser**
    *   **Descripción:** Modificar `guide_parser.py` para que, en lugar de imprimir en consola, guarde los tres bloques de texto extraídos en un archivo `ugr_data.json` estructurado.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 1.3: Crear Comando de Importación de Datos**
    *   **Descripción:** Desarrollar un nuevo comando de gestión en la aplicación `academic_structure` llamado `import_ugr_data`. Este comando leerá el `ugr_data.json` y poblará los campos correspondientes del modelo `Subject` (o un nuevo modelo si es necesario) con la información extraída.
    *   **Estado:** `[COMPLETADA]`

**FASE 2: Adaptación de la Arquitectura de Datos (Modelos)**

*   **Tarea 2.1: Extender el Modelo de `Chunks` de Contenido**
    *   **Descripción:** Modificar el modelo `content_automation.GeneratedContentChunk` para añadir un nuevo campo: `ai_sources = models.TextField(blank=True, null=True, verbose_name="Fuentes de la IA")`.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 2.2: Aplicar Migraciones de Base de Datos**
    *   **Descripción:** Ejecutar `makemigrations` y `migrate` para aplicar los cambios del modelo a la base de datos.
    *   **Estado:** `[COMPLETADA]`

**FASE 3: Actualización del Núcleo de Generación (Lógica de IA)**

*   **Tarea 3.1: Refactorizar el Generador de Prompts**
    *   **Descripción:** Modificar el servicio `core/services/prompt_generators.py`. El prompt que solicita la generación de una sección individual (`chunk`) debe ser re-diseñado para exigir a la IA que devuelva una respuesta en formato JSON con dos claves: `{"content": "...", "sources": "..."}`.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 3.2: Refactorizar la Tarea Celery de Generación**
    *   **Descripción:** Actualizar la tarea Celery (`content_automation/tasks.py`) que gestiona la generación de `chunks`. La tarea deberá parsear la respuesta JSON de la IA y guardar el valor de `content` en el campo `body` y el valor de `sources` en el nuevo campo `ai_sources` del `GeneratedContentChunk`.
    *   **Estado:** `[COMPLETADA]`

**FASE 4: Actualización del Ensamblador del Producto Final**

*   **Tarea 4.1: Refactorizar la Lógica de Ensamblaje de `ContenidoMaterial`**
    *   **Descripción:** Modificar la lógica que construye el `ContenidoMaterial` final. Deberá iterar sobre todos los `chunks` asociados a la tarea, construir la sección "Fuentes y Bibliografía" a partir de los campos `ai_sources` y añadirla al final del cuerpo del material.
    *   **Estado:** `[COMPLETADA]`

**FASE 5: Implementación de la Lógica de Negocio y UI**

*   **Tarea 5.1: Conectar la UI con la Vista de Detalle de Guía Docente**
    *   **Descripción:** Añadir un enlace "Previsualizar Guía" en la vista de creación de tareas (`create_academic_task.html`) que apunte a la vista de detalle del `SubjectAdmin`, permitiendo al administrador consultar los datos de la guía antes de generar contenido.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 5.2: Re-arquitectura del Dashboard de Contenidos**
    *   **Descripción:** Transformar el dashboard para que muestre estadísticas globales y un listado de `ContentRequest` (solicitudes de usuarios) priorizadas por número de peticiones, convirtiéndolo en un verdadero centro de mando.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 5.3: Corregir el Renderizado de la Previsualización**
    *   **Descripción:** Modificar los métodos `display_*` en `academic_structure/admin.py` para asegurar que el contenido de las guías (objetivos, temario, bibliografía) se muestre de forma legible, respetando saltos de línea y formato.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 5.4: Implementar Notificaciones de Solicitud**
    *   **Descripción:** Crear un mecanismo (probablemente una señal `post_save`) que envíe una notificación push a los administradores cuando se crea una nueva solicitud de contenido por parte de un usuario.
    *   **Estado:** `[COMPLETADA]`


---
#### **4. Estrategia de Retoma y Re-planificación**

El hito se retoma con una visión estratégica expandida, centrada en la **automatización total de la generación de contenido** y la gestión de múltiples API Keys para garantizar la continuidad del proceso. La estrategia inicial de "evitar duplicados" se ha consolidado en una arquitectura completa de orquestación. La nueva hoja de ruta detallada se encuentra en la sección 5.


---

#### **5. Hoja de Ruta Detallada (v2.0): El Centro de Control de Contenidos de Generación Masiva**

**FASE 1: El Rotador de API Keys (El Corazón del Sistema)**

*   **Tarea 5.1: Crear el Modelo Singleton `AutomationSettings`**
    *   **Descripción:** Crear un nuevo modelo en la app `global_settings` o `content_automation` para gestionar el estado persistente del sistema de automatización (`active_key_index`, `is_running`).
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 5.2: Refactorizar el Servicio de Gemini (gemini_service.py)**
    *   **Descripción:** Modificar `core/services/gemini_service.py` para que consulte el modelo `AutomationSettings` y utilice la clave activa del pool de API Keys.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 5.3: Implementar la Lógica de Rotación por Fallo de Cuota**
    *   **Descripción:** Modificar la tarea Celery `generate_full_course_task` para que, tras fallos repetidos de `ResourceExhausted`, incremente el `active_key_index` en `AutomationSettings`, rotando a la siguiente API Key.
    *   **Estado:** `[COMPLETADA]`

**FASE 2: La Interfaz de Control (La Cabina de Mando)**

*   **Tarea 6.1: Crear Vistas y URLs para los Nuevos Dashboards**
    *   **Descripción:** Crear las vistas y rutas para el "Dashboard de Creación de Contenido Académico" y el "Centro de Control de Automatización".
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 6.2: Crear las Plantillas de los Dashboards**
    *   **Descripción:** Maquetar los archivos `.html` para las nuevas vistas, incluyendo botones, estadísticas (inicialmente con valores de marcador de posición) y el interruptor maestro "Iniciar/Detener".
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 6.3: Implementar la Lógica del Interruptor Maestro**
    *   **Descripción:** Crear una vista HTMX que será llamada por el botón "Iniciar/Detener" para cambiar el estado `is_running` en el modelo `AutomationSettings`.
    *   **Estado:** `[EN PROGRESO]`

---
### **6. Visión Estratégica Definitiva v2: La Arquitectura "Tolva y Vagonetas Non-Stop"**

Esta sección es la **única y absoluta fuente de verdad** para la arquitectura del motor de automatización y anula cualquier interpretación, plan o documento previo.

El sistema se concibe como un circuito de "Vagonetas" (`PendingContentTask`) que son llenadas por diferentes fuentes y procesadas por un "Worker".

*   **La Tolva (Universo de Tareas Académicas):**
    *   Representa todas las asignaturas (`Subject`) de la plataforma que aún no tienen contenido.
    *   **Filtros (Semillas):** El Administrador utiliza las "Semillas" (`seed_branch`, etc.) para definir el subconjunto activo de la tolva.

*   **Las Vagonetas (La Cola de Trabajo `PendingContentTask`):**
    *   La cola de trabajo activa tiene una longitud efectiva de **UNO**. Solo existe "la tarea en proceso" y "la próxima tarea pendiente".

*   **Fuentes de Llenado de Vagonetas (Prioridad):**
    1.  **El Administrador (Prioridad Absoluta):** Puede llenar manualmente la "próxima vagoneta" en cualquier momento, y el sistema automático siempre cederá el paso.
    2.  **El Motor Automático (Dispensador de la Tolva):** La tarea periódica (`automation_main_loop_task`) actúa como el dispensador. Su lógica es:
        *   Comprueba guardianes: Interruptor activo, no hay solicitudes libres, no hay tareas en proceso, y la "próxima vagoneta" está vacía.
        *   Si se cumplen, dispensa una `Subject` de la "Tolva" (filtrada por las Semillas).

*   **El Worker (Procesador de Tareas):**
    *   El `Celery Worker` que ejecuta `generate_full_course_task` es agnóstico a la fuente. Coge la siguiente vagoneta de la cola y procesa su contenido sin hacer preguntas.

*   **Lógica "Non-Stop" (Directriz Crítica):**
    *   **Propósito:** Asegurar que el motor de automatización no se detenga mientras existan asignaturas sin contenido en cualquier parte de la plataforma, incluso si el lote de trabajo definido por las semillas actuales se ha agotado.
    *   **Mecanismo de Avance Automático:** Al final de la ejecución de CADA tarea de generación masiva (`generate_full_course_task`), se añadirá un nuevo paso. Este paso comprobará si todavía quedan `Subject` que coincidan con los filtros de semilla actuales.
        *   **Si NO quedan `Subject` para las semillas actuales:**
            1.  **Notificación:** Se enviará una notificación (Push + Email) al Administrador informando de que el lote de trabajo definido por las semillas actuales (ej. "Segundo de Traducción") ha sido completado.
            2.  **Avance de Filtro:** El sistema **moverá automáticamente el filtro**, "subiendo" un nivel en la jerarquía. Por ejemplo, si se agotó un `seed_degree`, lo limpiará y mantendrá el `seed_branch`, continuando el trabajo con el resto de grados de esa rama. Si se agota la rama, la limpiará y pasará a la siguiente. Este proceso asegura una continuación fluida del trabajo.
        *   **Si SÍ quedan `Subject`:** No se hace nada. El dispensador automático (`automation_main_loop_task`) se encargará de crear la siguiente tarea en su ciclo normal.

*   **Control Operativo y Bloqueos:**
    *   El Interruptor Maestro sigue siendo el control absoluto de pausa/reanudación.
    *   Las solicitudes de contenido libre siguen actuando como "freno de mano" para todo el sistema.


### **7.Error en la generación de Contenido Libre

*   **Error inesperado al crear la tarea: ContentMaterial() got unexpected keyword arguments: 'author'**
    *   Ha dado este error al intentar crear una biografía.