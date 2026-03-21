
# 2026-03-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO
*  **Session:** Auditoría Integral de Funcionalidad Assessment V2
*  **Description:** Fase II y III del Hito 6. Auditoría exhaustiva del código frente a la documentación satélite. Verificación de llamadas al SDK de Google Gemini, correcta implementación de los widgets (ej. capacidades de texto y adjuntos) y validación de que todos los subarquetipos generan evaluaciones sin errores de sintaxis ni parámetros. Resolución de incidencias detectadas.

# 2026-03-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Estabilización Estructural de Autoevaluaciones V2
*  **Description:** Ejecución del plan de emergencia para el motor de autoevaluaciones (Hito 6). Las acciones incluyen: estandarización de la firma get_user_prompt en BaseExamStrategy, implementación del patrón 'Skeleton-Prompt Binding' en las estrategias (Humanidades, Ciencias Sociales, Tecnología, Ciencias, Salud) para evitar alucinaciones estructurales, soporte de archivos adjuntos en motores discursivos (DRA-HOLO, BMT-SHIFT), y corrección del parámetro de audio en el servicio Gemini.


# 2026-03-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC !<-- --SYSTEM -->!
*  **Session:** Auditoría y Reparación de Flujo End-to-End para Autoevaluaciones IA
*  **Description:** Inicio de la fase de auditoría integral de flujo para el sistema de autoevaluaciones (Hito 6). Se procederá a estandarizar la clase base BaseExamStrategy, implementar el Prompt Binding en todas las estrategias para garantizar el respeto del Skeleton JSON por parte de Gemini, y verificar la trazabilidad completa del dato hasta su renderizado en HTML.


# 2024-05-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Auditoría Espectro Completo Hito 6
*  **Description:** Inicio de la sesión de auditoría del Hito 6 (Sistema de Autoevaluaciones con IA). Se han cargado en memoria los 11 documentos satélite y el plan maestro. La sesión se enfocará en validar la integridad documental y estructural de los 45 subarquetipos, estrategias de generación, contratos de inyección de contenido y el renderizado de los 7 widgets correspondientes.

# 2026-03-10
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO !<-- # --SYSTEM -->!
*  **Session:** Refactorización del Arquetipo de Lenguas y Blindaje JSON
*  **Description:** Sesión enfocada en la implementación de la hoja de ruta del Hito 6. Se procederá a refactorizar la estrategia de evaluación de lenguas (languages.py) para establecer a Python como la única fuente de verdad en la generación de la estructura JSON, relegando a la IA a un rol estricto de llenado de contenido mediante marcadores predefinidos. También se adaptará el frontend (exam_take.html) para renderizar condicionalmente los nuevos widgets y se validará el flujo completo desde el backend hasta la interfaz.
# 2026-03-10
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA !<-- # --SYSTEM -->!
*  **Session:** Refactorización del Arquetipo de Lenguas y Validación JSON
*  **Description:** Implementación de la directriz crítica de inyección de contenido para el Hito 6. Se refactorizará languages.py para definir un esqueleto JSON inmutable con marcadores explícitos (W-OBJ-STRIKE, W-TXT-CLOZE, W-HUM-TEXT, etc.). A nivel de frontend, se adaptará exam_take.html para renderizar componentes dinámicos como huecos en texto y paneles laterales. Finalmente, se añadirá una capa de validación estricta en orchestrator/tasks.py que rechace cualquier alteración estructural generada por la IA, asegurando que actúe exclusivamente como motor de llenado de plantillas.

# 2026-03-11
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC !<-- # --SYSTEM -->!
*  **Session:** Blindaje y Refactorización del Arquetipo de Lenguas
*  **Description:** Sesión orientada a la refactorización del motor de evaluación de lenguas y su correspondiente validación (Hito 6). Se implementará el protocolo estricto de interacción IA mediante plantillas JSON inmutables en languages.py, garantizando que Gemini actúe únicamente como motor de relleno. Asimismo, se adaptará el frontend (exam_take.html) para soportar los nuevos marcadores como huecos (Cloze) o tachados (Strike), y se fortalecerá el orquestador (orchestrator/tasks.py) para aplicar el rechazo inmediato ante alteraciones estructurales por parte de la IA, asegurando el cumplimiento íntegro y exacto de la documentación V06.

# 2026-03-11
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** Blindaje JSON y Refactorización de Arquetipo de Lenguas
*  **Description:** Verificación documental del bug de salidas estructuradas JSON en Gemini 2.5 Flash Lite y ejecución del Hito 6 para el sistema de autoevaluaciones. Se aplicará el patrón 'Skeleton-Prompt Binding' y 'Máquina de Relleno' mediante refactorizaciones atómicas y quirúrgicas en 'languages.py' (estrategias), 'orchestrator/tasks.py' (validación estricta post-IA) y 'exam_take.html' (adaptación del frontend para widgets W-TXT-CLOZE, W-OBJ-STRIKE y W-HUM-TEXT).


# 2026-03-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO !<-- # --SYSTEM -->!
*  **Session:** Refactorización IA a Gemini 3.1 Flash y Outputs Estructurados
*  **Description:** Actualización de los documentos de directrices TOTAL_COMMANDER_*.md para usar gemini-3.1-flash y esprima. Modificación de la documentación satélite del Hito 6 para reflejar la transición a Structured Outputs (JSON nativo) abandonando el relleno de marcadores. Posteriormente, refactorización de gemini_service.py y servicios de IA dependientes para integrar los nuevos esquemas estructurados de Gemini.

# 2026-03-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Auditoría y Refactorización del Arquetipo de Lenguas
*  **Description:** Sesión dedicada a la auditoría, refactorización y testing exhaustivo del arquetipo de lenguas (ARCH_LANG) y sus 6 sub-arquetipos. Se verificará la correcta integración con los esquemas Pydantic para asegurar que la generación de contenido se realice usando Structured Outputs de forma estricta, eliminando los marcadores de texto. Posteriormente, se realizarán pruebas completas para validar que el orquestador mapea y renderiza los JSON sin errores. Una vez estabilizado, se planificará la transición al siguiente bloque en prioridad.

# 2026-03-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC
*  **Session:** Solución Error 404 Gemini API en Generación y Assessment
*  **Description:** Resolución del error 404 'NOT_FOUND' provocado por la configuración del modelo 'gemini-3.1-flash' en los servicios de IA de la plataforma. Se procede a investigar y estandarizar el modelo a 'gemini-2.5-flash-lite', cumpliendo con la directriz técnica inmutable del sistema. Esta intervención solucionará tanto el fallo en la generación de contenido (Orchestrator) como el error 500 durante la creación de evaluaciones en Assessment v2 (AcademicDeductor).


# 2024-05-21
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Desarrollo del Sistema de Autoevaluaciones con IA (Hito 6)
*  **Description:** Reanudación del trabajo en el Hito 6, enfocado en el motor de autoevaluación inteligente. La sesión se centra en la revisión de la arquitectura del motor de evaluación v2, la integración con la API de Gemini para la generación de contenidos evaluativos y la validación de los modelos de datos de seguimiento y planes de acreditación.


# 2026-03-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA # --SYSTEM -->
*  **Session:** Implementación y Testing Funcional del Arquetipo de Lenguas (Structured Outputs)
*  **Description:** Sesión dedicada a implementar y validar la generación atómica del arquetipo de lenguas (ARCH_LANG) utilizando Structured Outputs nativos. Se desarrollará un script temporal de prueba para la sección SD_READ que invoque la Strategy correspondiente y se verificará el cumplimiento estricto del esquema Pydantic (ExamSectionSchema). Además, se validará la correcta persistencia estructural en base de datos (ExamSection e ExamItem) a través de generate_exam_task. Si el flujo es exitoso, se auditará la interacción de UniversIA para garantizar la estabilidad general de la plataforma frente a los nuevos esquemas de respuesta.

# 2026-03-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Restauracion Logica Rotacion API Keys
*  **Description:** Análisis del repositorio (commit 8 de marzo) para extraer y restaurar la lógica de rotación de claves API, gestión de cuarentenas y control de cuotas por minuto. Adaptación de este flujo al nuevo SDK de Gemini 3.1 para asegurar la estabilidad del sistema de generación de autoevaluaciones y prevenir errores 429.

# 2026-03-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA
*  **Session:** Blindaje Arquetipo Lenguas y Logs Celery Hito 06
*  **Description:** Resolución de incidencias críticas del Hito 6. Se implementa instrumentación de logs en las tareas de Celery (orchestrator/tasks.py) para monitorizar la latencia en la clasificación inicial de IA mediante AcademicDeductor. Además, se refuerza el prompt del sistema en la estrategia de humanidades (assessment_v2/services/engine/strategies/humanities.py) con restricciones negativas explícitas para el idioma chino, bloqueando de forma absoluta la aparición de caracteres de silabarios japoneses o coreanos.


# 2026-03-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Refactorización asíncrona y optimización UX (Hito 6)
*  **Description:** Análisis y planificación de la refactorización de la arquitectura de evaluaciones (Hito 6). La sesión abordará el desacoplamiento de vistas para evitar bloqueos, la implementación de generación asíncrona (Batch-Atómico) a través de Celery en el orquestador, y el blindaje de la calidad de contenido utilizando esquemas estrictos de Pydantic y directrices de inyección. Además, se ajustará el frontend para reflejar notificaciones asíncronas de estado.

# 2026-03-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Refactorización Asíncrona de Generación de Evaluaciones
*  **Description:** Optimización de UX posponiendo la clasificación del examen mediante IA hasta después de la selección del temario. Implementación de generación asíncrona con modal de aviso estricto y bloqueo condicional del botón de solicitud en la vista de edición de material.


# 2026-03-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO # --SYSTEM -->
*  **Session:** Corrección de filtración de datos en exam_take.html
*  **Description:** Resolución de la vulnerabilidad en la vista de realización de exámenes (exam_take.html) que exponía metadatos sensibles como las respuestas correctas y el feedback en el código fuente. Se implementa la iteración segura para el widget W-OBJ-STRIKE, renderizando exclusivamente las opciones necesarias mediante botones de radio con estilos de Bootstrap/UniversIA y bloqueando la exposición de información crítica en el DOM.

# 2026-03-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO # --SYSTEM -->
*  **Session:** Refactorización de vista de examen y sanitización de widgets
*  **Description:** Sesión enfocada en erradicar fallos de presentación en la vista de examen (exam_take.html). Se implementará lógica de sanitización robusta en ExamTakeView mediante ast.literal_eval para limpiar diccionarios stringificados en las opciones de los ítems, extrayendo únicamente la clave de texto. Además, se reestructurará la plantilla eliminando cabeceras de depuración, corrigiendo la lógica condicional del section_stimulus para asegurar su renderizado, y simplificando el bloque de opciones. Por último, se auditará LanguageInstrumentalStrategy para habilitar la generación de los widgets W-MIX-MATCH y W-TXT-CLOZE.

# 2026-03-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** MAMC: Alineación Subatómica del Arquetipo de Lenguas con la Acreditación UGR
*  **Description:** Inicio de la fase de refactorización técnica y actualización documental para el Hito 6. El objetivo central es sincronizar el motor de autoevaluaciones con los estándares de acreditación de la Universidad de Granada para el arquetipo de lenguas. Se contempla la actualización de la estrategia de inmersión y la integración de requisitos específicos para widgets de escritura (teclado multilingüe/occidentalizado, trazos en pantalla y captura de manuscritos vía OCR/Imagen). Se aplicará el protocolo PMA para la modificación de la lógica en assessment_v2, asegurando que el código sea un reflejo fiel de la documentación académica validada.


# 2026-03-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC
*  **Session:** Refactorización Subatómica Arquetipo Lenguas (Hito 6)
*  **Description:** Auditoría y refactorización integral de la constelación documental del Arquetipo de Lenguas (ARCH_LANG) basándose en la acreditación oficial de la UGR. Inclusión de la Directriz de Multimodalidad, niveles de inmersión y reestructuración de la taxonomía de errores, respetando la prohibición estricta de alteración de código.


# 2025-03-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Refactorización del Subarquetipo Lingüístico SUB-LIN-MINOR (Hito 6 - V3.1)
*  **Description:** Inicio de la refactorización integral del subarquetipo 'Minor/Iniciación' (SUB-LIN-MINOR) para alinearlo con la normativa de la Facultad de Filosofía y Letras de la UGR. La sesión se centra en la definición de la secuencia genética obligatoria (Grafía, Gramática, Lectura y Cultura), el diseño de motores de validación de trazos (RBT-GRAPH-VAL) y el forzado de entrada multimodal en widgets para lenguas no occidentales.

# 19/03/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Sincronización de Constantes para Subarquetipo Minor
*  **Description:** Implementación de las nuevas subdivisiones académicas (Grafía y Fonética, Estructura Base, Lectura Adaptada y Contexto Sociocultural) en el modelo ExamSection de assessment_v2, alineando el motor de evaluación con la normativa refactorizada de la UGR para el subarquetipo SUB-LIN-MINOR.

# 19/03/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Refactorización Documental Filológica UGR
*  **Description:** Refactorización integral del subarquetipo SUB-LIN-PHILO para los Grados en Filología de la UGR. Definición de la secuencia genética obligatoria: Fonética y Fonología Histórica (SD_PHONO), Morfología Diacrónica (SD_MORPH_DIAC), Lexicología y Semántica (SD_LEX_SEM) y Crítica Textual (SD_TEXT_CRIT). Establecimiento del rigor LVL_C (Epistemológico) y motor de validación EV-DIAC-VAL para leyes fonéticas.

# 2026-03-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06
## CAMA
*  **Session:** Refactorización Genética del Subarquetipo Philo (UGR)
*  **Description:** Regulación técnica del subarquetipo SUB-LIN-PHILO para los Grados en Filología. Se definen las fases SD_PHONO, SD_MORPH_DIAC, SD_LEX_SEM y SD_TEXT_CRIT bajo el rigor LVL_C, priorizando el blindaje documental de la lógica diacrónica y el motor de validación EV-DIAC-VAL antes de la implementación.

# 19/03/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Hito 6: Refactorización del Subarquetipo NORM para la UGR
*  **Description:** Inicio de la sesión enfocada en la refactorización integral del subarquetipo SUB-LIN-NORM (Modelo Norma y Uso / Corrección Lingüística) dentro del Hito 6. Se ha procesado la constelación documental completa, validando la finalización del modelo PHILO y estableciendo la hoja de ruta para el cumplimiento de la normativa académica de la UGR en toda la estructura de evaluación (Templates, Widgets y Metadata). Se aplicará el protocolo de intervención quirúrgica para asegurar la integridad de los modelos previamente inyectados, centrando el esfuerzo exclusivamente en la lógica de corrección lingüística y ortografía normativa.


# 2026-03-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Refactorización Subarquetipo Traducción Literaria (SUB-LIN-TRA-LIT) - FTI UGR
*  **Description:** Inicio de la fase de implementación técnica para el subarquetipo de Traducción Literaria y Editorial (SUB-LIN-TRA-LIT) basado en los planes de estudio de la FTI (UGR). El objetivo es definir la lógica de las tres fases (Estilística, Creativa y Crítica) y configurar el motor DRA-HOLO para la evaluación de calidad literaria, asegurando la integración con la arquitectura de Assessment_V2 y el cumplimiento de los estándares de excelencia académica de la Universidad de Granada.

# 2026-03-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO
*  **Session:** Reinicio Estructural Rama Lenguas (Fidelidad UGR 100%) - SUB-LIN-INSTR
*  **Description:** Ejecución de la Fase 1 del Hito 6: Refactorización de la rama ARCH_LANG bajo el Mandato Supremo (WORD_OF_GOD). Se procede al mapeo subatómico del subarquetipo SUB-LIN-INSTR (CertAcles/CLM) integrando los criterios reales de la UGR: evaluación de 4-5 destrezas, límites de palabras en respuestas cortas y bloqueos de navegación secuencial.

# 2026-03-21
# CampuStudiOnline --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Refactorización Subatómica del Subarquetipo SUB-LIN-MINOR y Fidelidad UGR
*  **Description:** Inicio de la sesión MAMC centrada en la refactorización subatómica del subarquetipo SUB-LIN-MINOR (Modelo Minor / Iniciación) para alcanzar el 100% de fidelidad con los criterios de la Universidad de Granada. Tras cargar la constelación documental completa del Hito 6, el foco se sitúa en la definición de la secuencia genética de evaluación para lenguas de iniciación, integrando obligatoriamente los widgets de trazos y OCR para alfabetos no latinos (Árabe, Chino, Japonés, Ruso, Hebreo) y validando los criterios de grafía, fonética y cultura base. Se auditarán los modelos de datos de las aplicaciones críticas para asegurar la compatibilidad con el sistema de orquestación basado en Structured Outputs y la lógica de penalizaciones FATAL no compensables exigida por la UGR.
