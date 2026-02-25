# 2025-11-08
# CAMPUSTUDIONLINE --TEMP
# APIKEYS_ROTATION_AND_QUARENTNINE_FAILURE
## MAMC
*  **Session:** Investigación y Corrección del Fallo en la Rotación y Cuarentena de API Keys
*  **Description:** Sesión de depuración para diagnosticar y resolver una posible regresión en el sistema de rotación de `APIKeys` de la aplicación `content_automation`. El síntoma principal es que solo una clave entra en cuarentena y la clave activa no rota correctamente, impactando la generación de contenido.

# 2025-11-09
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*   **Session:** Resolución de Incidencias en Indicadores de Evaluación
*   **Description:** Solucionar cuatro incidencias en el sistema de autoevaluaciones: 1) Ausencia de badges en 'Contenidos Libres', 2) Eliminación de leyenda en 'Mi Explorador Personal', 3) Restauración de badges en 'Sala de Estudio', y 4) Añadir feedback visual para el cooldown del botón de solicitar evaluación.

# 2025-11-09
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Refactorización del Sistema de Indicadores de Estado de Autoevaluaciones
*  **Description:** Rediseñar la lógica de propagación de estados de `assessment` para que los indicadores (`badges`) reflejen correctamente los estados de los nodos hijos en las vistas jerárquicas (`academic_directory`, `search`, `contents`), incluyendo estados de fallo y un nuevo estado "Múltiple".

# 09/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Corrección de Sintaxis ORM en la Propagación de Estados de Autoevaluaciones
*  **Description:** Refactorizar la función 'annotate_with_assessment_states' en 'assessment/utils.py' para utilizar las clases de lookup explícitas de Django (Exact, GreaterThan) en las condiciones 'When', solucionando el 'FieldError' causado por una sintaxis de consulta incorrecta y asegurando la correcta visualización de los badges de estado.

# 2025-11-09
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Refactorización de la Lógica de Badges de Autoevaluación y Corrección de Consulta ORM
*  **Description:** La sesión se centrará en corregir un `FieldError` en la función `annotate_with_assessment_states` del archivo `assessment/utils.py`. La causa es una sintaxis incorrecta en la construcción de consultas complejas del ORM de Django. La solución, identificada en la sesión anterior, consiste en reemplazar los `lookups` implícitos por palabra clave con el uso explícito de las clases `Exact` y `GreaterThan` para asegurar la correcta comparación de valores en las subconsultas, resolviendo así la propagación incorrecta de estados de las autoevaluaciones.

# 09/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Diagnóstico de Fallo en Generación de Autoevaluaciones
*  **Description:** Investigar y resolver la causa por la que las nuevas autoevaluaciones pasan a estado 'FAILED' de forma inmediata, utilizando la shell de Django y los logs de Celery para un análisis empírico.

# 10/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Diagnóstico y Corrección de Fallo en Generación de Autoevaluaciones
*  **Description:** La sesión se centrará en investigar por qué las nuevas autoevaluaciones fallan de forma inmediata. El plan de acción se basa en el método empírico: se inspeccionará el estado del objeto Assessment en la base de datos y se revisarán los logs de Celery para identificar la causa raíz del error y proceder a su corrección.

# 2025-11-10
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Mantenimiento y Mejora del Sistema de Autoevaluaciones con IA y Celery
*  **Description:** Continuar con la refactorización del sistema de autoevaluaciones (Fases 2 y 3), centrando la lógica en el modelo ContentCopy, aplicando las migraciones de base de datos necesarias y mejorando la experiencia de usuario de los indicadores de estado en la Sala de Estudio.

# 11/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Diagnóstico del Bucle Infinito en Tareas Celery de Autoevaluaciones
*  **Description:** Investigar y resolver por qué las autoevaluaciones generadas por IA en la app `assessment` permanecen indefinidamente en estado `PROCESSING`, analizando la tarea Celery (`assessment/tasks.py`), los logs y la comunicación con la API externa para asegurar la correcta transición a estados finales (`COMPLETED` o `FAILED`).

# 2025-11-11
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Diagnóstico del Bucle Infinito en el Procesamiento de Evaluaciones de IA
*  **Description:** Analizar la tarea Celery en assessment/tasks.py y los logs del sistema para identificar la causa raíz por la que las autoevaluaciones generadas por IA no finalizan, quedándose atascadas en el estado 'PROCESSING'.

# 11/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Corrección del Temporizador de Evaluaciones y Diagnóstico del Bucle de Procesamiento
*  **Description:** La sesión se centrará en dos objetivos principales. Primero, se abordará un problema de experiencia de usuario (UX) en el que el temporizador de cuenta regresiva de las evaluaciones se muestra de forma estática. Se investigará el código JavaScript y la transmisión de datos desde Django para solucionarlo. En segundo lugar, se retomará la investigación original para diagnosticar por qué las evaluaciones quedan indefinidamente en estado de "procesamiento", lo que implicará un análisis de las tareas y logs de Celery.

# 11/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Corrección del Temporizador de Evaluaciones y Diagnóstico de Bucle de Procesamiento
*  **Description:** La sesión se centrará en dos objetivos: primero, corregir el temporizador de cuenta regresiva en las autoevaluaciones, asegurando que la `expiration_date` se propague correctamente al frontend; y segundo, diagnosticar la causa por la cual las evaluaciones pueden quedar atascadas en el estado 'PROCESSING', investigando los logs de Celery y el flujo de la tarea asíncrona.

# 12/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Diagnóstico de Inyección Dinámica de Scripts en el Módulo de Autoevaluaciones
*  **Description:** Localizar y erradicar la causa de la carga duplicada del script `assessment_status_handler.js`, que impide el correcto funcionamiento del temporizador de las autoevaluaciones, mediante el análisis de código Python y la inserción de sondas en las plantillas.

# 2025-11-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Validación Final y Cierre del Hito 6: Sistema de Autoevaluaciones
*  **Description:** Realizar una comprobación final del sistema de autoevaluaciones para verificar la ausencia de regresiones tras la corrección del temporizador. Si la validación es exitosa, proceder a actualizar la documentación del proyecto para marcar el Hito 6 como COMPLETADO.

# 2025-11-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC
*  **Session:** Reparación Crítica del Generador de Contenidos y Optimización del Admin
*  **Description:** Sesión de emergencia para corregir la regresión en `orchestrator/tasks.py` que causaba bucles de alucinación en el contenido. Se reparó la lógica de visibilidad de materiales en el Directorio Académico (`academic_directory/views.py`) tras diagnosticar la invisibilidad de 'Alemán I' (UAL). Se ejecutó una purga selectiva de contenidos basura y se optimizó el rendimiento del panel de administración en las aplicaciones `contents` y `chat` mediante `list_select_related` para solucionar el cuello de botella de consultas N+1.

# 13/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Diagnóstico y Corrección de Filtrado de Categorías en la Vista de la Sala de Estudio
*  **Description:** La sesión se centrará en resolver un error visual donde la categoría de contenido libre 'Contenidos en CampuStudiOnline' aparece incorrectamente en la sección de contenido académico. Siguiendo un enfoque empírico, se desarrollará un script de diagnóstico para inspeccionar los querysets de la vista `user_copies_list` y determinar la causa raíz del filtrado incorrecto antes de proponer una solución.

# 13/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Diagnóstico y Corrección del Botón 'Realizar Evaluación' en la Sala de Estudio
*  **Description:** Sesión dedicada a solucionar un problema de usabilidad donde el botón 'Realizar Evaluación' no se comporta como se espera. Se utilizará un script de diagnóstico en la shell de Django para verificar los estados de las evaluaciones existentes y se auditará la lógica de la vista `get_assessment_context` en `assessment/utils.py` para implementar una solución que sincronice el estado del botón con la disponibilidad real de la evaluación.

# 2025-11-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Diagnóstico y Corrección de Comportamientos Anómalos en Navegación de Sala de Estudio
*  **Description:** Abordar dos incidencias críticas en la Sala de Estudio: un error 'Not Found' transitorio al acceder a nuevas 'ContentCopy' y la aparición de copias en grados incorrectos debido a un filtrado erróneo por 'ContentHashFamily'. La sesión se centrará en analizar y corregir las vistas y lógicas de filtrado pertinentes para restaurar la coherencia en la navegación.

# 2025-11-14
# CAMPUSTUDIONLINE --TEMP
# ASSESSMENT_NOTIFICATION_TEMPLATE_FIX
## CYC
*  **Session:** Corrección del Contexto en Plantillas de Notificación de Autoevaluaciones.
*  **Description:** Solucionar el error `VariableDoesNotExist` en las notificaciones de autoevaluación (`assessment`) asegurando que el contexto (`context`) pasado a las plantillas (`.txt`, `.html`) contenga las variables `content_title` y `action_url`.

# 2025-11-14
# CAMPUSTUDIONLINE --TEMP
# UI_BADGE_ERRORS_FIX
## CYC
*  **Session:** Corrección de la Lógica de Visualización de Badges de Autoevaluación
*  **Description:** Diagnosticar y solucionar los errores en la presentación de los indicadores de estado de las autoevaluaciones (Assessment) en la vista de la Sala de Estudio, asegurando que se muestren correctamente según su contexto jerárquico.

# 14/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Validación Integral del Sistema de Autoevaluaciones con IA
*  **Description:** Esta sesión se centrará en realizar una validación completa y exhaustiva del sistema de autoevaluaciones con IA. Se probará el flujo de trabajo completo, desde la creación y generación de la evaluación, pasando por la realización del test, su posterior corrección y la visualización final de los resultados, para asegurar su estabilidad y correcto funcionamiento antes de continuar con nuevas funcionalidades.

# 15/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## DEPCRI-VTLUI
*  **Session:** Depuración de Errores Post-Refactorización en Vistas, Tareas y UI
*  **Description:** Resolución de `VariableDoesNotExist` en `content_detail`, corrección de contexto en notificaciones de `assessment` y refactorización de la lógica de badges en la sala de estudio.

# 15 de noviembre de 2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## MAMC
*  **Session:** Refactorización del Orquestador de Tareas Asíncronas e Implementación de la App 'orchestrator'
*  **Description:** Crear la nueva aplicación 'orchestrator', migrar los modelos 'ApiKey' y 'AutomationSettings', centralizar la lógica de tareas en 'global_orchestrator_task', actualizar Celery Beat y refactorizar la app 'assessment' para su integración con el nuevo sistema.

# 2025-11-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## EDC
*  **Session:** Refactorización de la App 'assessment' para Integración con 'orchestrator'
*  **Description:** Continuar con la refactorización de la app 'assessment', corrigiendo el diseño del modelo Assessment para mantener los estados de fallo reintentables. Se modificará la lógica de las tareas asíncronas para delegar la gestión de reintentos al orquestador central y se aplicarán las migraciones correspondientes.

# 2025-11-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Desarrollo del Sistema de Autoevaluaciones con IA
*  **Description:** Implementación y refinamiento del módulo 'assessment', enfocado en la generación, gestión y visualización de autoevaluaciones personalizadas mediante la API de Gemini.

# 13/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Refactorización del Sistema de Autoevaluaciones con IA para Robustez y Resiliencia
*  **Description:** Implementar un sistema de reintentos con exponential backoff en la tarea Celery, gestionar errores fatales de forma explícita y mejorar los estados del modelo y la interfaz de usuario para proporcionar un feedback claro sobre los fallos en la generación de autoevaluaciones.

# 2025-11-11
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Diagnóstico del Bucle Infinito en el Procesamiento de Evaluaciones de IA
*  **Description:** Analizar la tarea Celery en assessment/tasks.py y los logs del sistema para identificar la causa raíz por la que las autoevaluaciones generadas por IA no finalizan, quedándose atascadas en el estado 'PROCESSING'.

# $(date +'15-11-2025')
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Depuración de Visualización de ContentCopy en Sala de Estudio
*  **Description:** Investigar y solucionar la incorrecta visualización de una copia de estudio en su contexto académico correspondiente, analizando modelos, vistas y datos en la BBDD.

# 16/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Refactorización de la Vista de Copias de Estudio para Contexto Académico
*  **Description:** Implementar una lógica de despacho en la vista `user_copies_list` para diferenciar entre la navegación de contenido libre y la navegación académica, solucionando el error de visualización que ignora el `subject_context` de las `ContentCopy`. Esto implica refactorizar las URLs y adaptar la plantilla correspondiente.

# 16/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Estabilización y Verificación de la Navegación Jerárquica en la Sala de Estudio
*  **Description:** Solución del error 'VariableDoesNotExist' en la vista de detalle de contenido para estabilizar la plataforma. Verificación empírica posterior de la refactorización de la navegación jerárquica académica en la sala de estudio, asegurando el correcto funcionamiento de las rutas y los indicadores de autoevaluación.

# 2025-11-14
# CAMPUSTUDIONLINE --TEMP
# UI_BADGE_ERRORS_FIX
## CYC
*  **Session:** Corrección de la Lógica de Visualización en Indicadores de Estado de Autoevaluaciones
*  **Description:** Diagnosticar y corregir la lógica de renderizado de los badges de estado para las autoevaluaciones en la Sala de Estudio, asegurando que se muestren correctamente según la jerarquía académica.

# 2025-11-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Estabilización de BBDD: Sincronización de Migraciones para la App 'Orchestrator'
*  **Description:** Resolver el error 'ProgrammingError: Table doesn't exist' para el modelo AutomationSettings mediante la aplicación de las migraciones pendientes de la app 'orchestrator', restaurando así la funcionalidad del panel de administración de automatización.

# 16/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Estabilización del Motor de Tareas Asíncronas: Corrección de FieldError en `assessment`
*  **Description:** Sesión dedicada a localizar y corregir un FieldError crítico en la app 'assessment', causado por una referencia a un campo 'updated_at' inexistente en el modelo Assessment. El objetivo es restaurar la funcionalidad del panel de control de automatización y el procesamiento de tareas en segundo plano.

# 2025-11-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** MAMC - Implementación de Controles Interactivos en Dashboard de Evaluaciones
*  **Description:** Desarrollar las vistas, URLs y modificaciones de plantilla necesarias para permitir la pausa, reanudación y cancelación de tareas de autoevaluación desde el nuevo "Centro de Control de Evaluaciones".

# 2025-11-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Corrección de Bug en la Interfaz del Centro de Control de Automatización
*  **Description:** Resolver la inconsistencia en la UI del 'Centro de Control de Automatización' que muestra un estado incorrecto del motor de tareas, impidiendo su arranque. El objetivo es auditar y corregir la vista y la plantilla correspondientes.

# 2025-11-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Diagnóstico y Corrección de Bug en la UI del Orquestador de Tareas
*  **Description:** Localizar y resolver la inconsistencia en la UI del nuevo módulo 'orchestrator' que impide el arranque del motor de tareas. La lógica ha sido migrada desde 'content_automation', por lo que se deben auditar las vistas, plantillas y modelos de 'orchestrator' para reflejar el estado real del motor.

# 2025-11-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Estabilización del Generador de Autoevaluaciones Asíncronas
*  **Description:** Auditar la lógica de estados en `orchestrator/tasks.py`, analizar los logs de Celery y consultar la base de datos para resolver el bucle o la omisión de la tarea `generate_assessment_from_content_task`.

# 17/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Estabilización del Sistema de Logging y Generación de Autoevaluaciones
*  **Description:** El objetivo principal es reparar el bucle de errores en el sistema de logging auditando `core/settings.py`. Una vez restaurada la telemetría, se diagnosticará y corregirá el fallo silencioso que impide a la tarea `generate_assessment_from_content_task` actualizar su estado final en la base de datos.

# 17/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Corrección de Importación y Estabilización del Módulo de Autoevaluaciones (Assessment)
*  **Description:** Sesión dedicada a resolver el `ModuleNotFoundError` en `assessment/views.py` causado por una importación incorrecta. El objetivo es aplicar el parche, recargar el servidor y realizar una prueba completa del flujo de generación de autoevaluaciones, verificando la correcta transición de estados en la base de datos y la ejecución exitosa de la tarea Celery.

# 17/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## EROTA
*  **Session:** Ejecución de la Refactorización del Orquestador de Tareas Asíncronas
*  **Description:** Aplicar el plan de acción definido en REFACTOR_MASTER_REPORT.md para eliminar referencias a módulos y modelos obsoletos en 'assessment' y 'content_automation', siguiendo un enfoque atómico archivo por archivo.

# 18/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## MAMC
*   **Session:** Refactorización Final del Orquestador y Corrección de Plantilla
*   **Description:** Finalizar el Hito 21 mediante la corrección de una referencia de URL obsoleta en `templates/admin/base_site.html`, cambiando el namespace `content_automation_admin` por `orchestrator`, completando así la migración de `content_automation` a `orchestrator`.

# 2025-11-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## EDC
*  **Session:** Implementación de Vistas Placeholder en el Orquestador
*  **Description:** Continuar con la refactorización del módulo `orchestrator`, implementando las vistas `Placeholder` restantes en `admin_views.py` para restaurar la funcionalidad completa del Centro de Control de Automatización.


# 19/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## EDC
*  **Session:** Refactorización del Orquestador: Recuperación y Estabilización
*  **Description:** Actualización de manifiestos tras reinicio de sesión y resolución de error crítico NoReverseMatch en la vista create_academic_task del orquestador.


# 19/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## NRA
*  **Session:** Dashboard Recovery and Namespace Fixes
*  **Description:** Fixing `NoReverseMatch` errors in orchestrator templates caused by obsolete namespaces. Verifying the complete content generation and assessment flow.


# 19/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## NRA
*  **Session:** Recuperación del Dashboard y Corrección de Namespaces
*  **Description:** Corrección de errores `NoReverseMatch` en plantillas del orquestador causados por namespaces obsoletos. Verificación del flujo completo de generación de contenido y evaluaciones.

# 20/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21
## CSO
*  **Session:** Reparación de Visibilidad de Logs en Orquestador
*  **Description:** Diagnóstico y corrección de la persistencia y visualización de logs de tareas asíncronas en el dashboard administrativo, resolviendo la incidencia de "logs invisibles" tras la refactorización de namespaces.


# 2025-11-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Reparación del Flujo de Ejecución de Evaluaciones
*  **Description:** Diagnóstico y corrección de fallos en los botones de acción "Realizar Evaluación" en la interfaz móvil, verificando la generación de URLs y la lógica de estado en el frontend.

# 2025-11-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## FIX_ASSESSMENT_EXECUTION
*  **Session:** Reparación de la Ejecución de Evaluaciones
*  **Description:** Diagnóstico y corrección del flujo de "Realizar Evaluación" en la interfaz de usuario, verificando la lógica de los botones, las URLs de redirección y el estado de las evaluaciones generadas.

# 20/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06
## CYC
*  **Session:** Diagnóstico y Reparación del Flujo de Ejecución de Evaluaciones
*  **Description:** Sesión dedicada a investigar y solucionar el bloqueo reportado en la acción "Realizar Evaluación". Se auditará la lógica del frontend (`assessment_status_handler.js`), la integridad de las URLs en las plantillas y la coherencia de los estados en el backend (`assessment/models.py` y `views.py`).


# 20/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06
## AES
* **Session:** Reparación del Flujo de Ejecución de Evaluaciones
* **Description:** Sesión dedicada a diagnosticar y corregir el fallo reportado en la acción "Realizar Evaluación" tras su generación. Se auditarán las plantillas, el manejo de estados en JavaScript (`assessment_status_handler.js`) y las rutas de Django para garantizar una transición fluida desde la notificación de "Evaluación Lista" hasta la interfaz de examen.

# 20/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# Hito 6
## EPI
*  **Session:** Estabilización del Proceso de Evaluaciones e Interfaz
*  **Description:** Corrección de la visualización de notificaciones (badges) en la interfaz de usuario y reparación de enlaces rotos en los logs del panel de administración del orquestador.


# 2025-11-21
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*   **Session:** Corrección de Enrutado Admin y Verificación de Logs
*   **Description:** Diagnóstico y resolución del error `NoReverseMatch` que provoca un fallo 500 en el panel de administración de evaluaciones. Verificación de la correcta persistencia de logs en `AssessmentSettings`.

# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## NRA
*  **Session:** Refactorización de la Navegación de Sala de Estudio: Implementación del Modelo Persistente UserStudyNavigation
*  **Description:** Se inicia la implementación del modelo UserStudyNavigation y el servicio NavigationTreeBuilder para desacoplar la visualización de la jerarquía académica de las consultas en tiempo real. El objetivo es mejorar el rendimiento y eliminar errores por cambios de slugs mediante un árbol JSON pre-calculado actualizado por señales.


# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## RNA
*  **Session:** Reparación Crítica en Search y Avance en Hito 22
*  **Description:** Sesión de emergencia para corregir el error de sintaxis en `search/views.py` que mantiene bloqueado el arranque de Django. Tras la reparación, se procederá a ejecutar las migraciones pendientes del módulo `contents` para consolidar la eliminación de la deuda técnica (Jerarquía Intelectual y Contenido Libre Legacy) y se avanzará en la implementación de la lógica de `UserStudyNavigation`.


# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## RNA
*  **Session:** Hito 22: Reparación Crítica en Search y Consolidación de Modelos
*  **Description:** Sesión de emergencia para corregir un error de sintaxis bloqueante en 'search/views.py' resultante de la refactorización previa. El objetivo inmediato es restaurar la operatividad de Django para ejecutar las migraciones pendientes en la aplicación 'contents', finalizando la limpieza de modelos obsoletos (Jerarquía Intelectual). Posteriormente, se procederá con la implementación de la lógica de navegación 'UserStudyNavigation'.

# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## CSO
*  **Session:** Hito 22: Reparación Crítica en Search y Consolidación de Modelos
*  **Description:** Sesión de emergencia para corregir un error de sintaxis bloqueante en 'search/views.py' resultante de la refactorización previa. El objetivo inmediato es restaurar la operatividad de Django para ejecutar las migraciones pendientes en la aplicación 'contents', finalizando la limpieza de modelos obsoletos (Jerarquía Intelectual). Posteriormente, se procederá con la implementación de la lógica de navegación 'UserStudyNavigation'.

# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## CSO
*  **Session:** Hito 22: Reparación Crítica en Search y Consolidación de Modelos
*  **Description:** Sesión de emergencia para corregir un error de sintaxis bloqueante en 'search/views.py' resultante de la refactorización previa. El objetivo inmediato es restaurar la operatividad de Django para ejecutar las migraciones pendientes en la aplicación 'contents', finalizando la limpieza de modelos obsoletos (Jerarquía Intelectual). Posteriormente, se procederá con la implementación de la lógica de navegación 'UserStudyNavigation'.


# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## CSO_NAV_REF_CLEAN
*  **Session:** Limpieza de Referencias Huérfanas Post-Migración de Navegación
*  **Description:** Ejecución de la Fase 7 del Hito 22. Auditoría y eliminación sistemática de código muerto y referencias a modelos eliminados (KnowledgeArea, Discipline, etc.) en vistas, procesadores de contexto y templates tras la migración exitosa a UserStudyNavigation. Preparación del backend para la integración del frontend.


# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22
## CYC
*  **Session:** H22: Reparación Crítica Navegación y Orquestador
*  **Description:** Ejecución de emergencia de la Fase 6 omitida: refactorización de `contents/study_room_views.py` para consumir `UserStudyNavigation` y eliminar dependencias legacy causantes de 404. Corrección de `TypeError: 'topic'` en `orchestrator/tasks.py` por campo obsoleto.

# 2025-11-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md
## EPI
*  Session: Estabilización de Navegación y Resolución de Ciclos en Contenido Libre
*  Description: Ejecución de la Fase 9 del Hito 22. Diagnóstico y corrección del error de redirección circular ("Pink Floyd") en la navegación de Contenido Libre tras la refactorización UserStudyNavigation. Verificación de integridad en la arquitectura de la Sala de Estudio.

*  **Session:** Hito 22 Fase 9: Corrección de Navegación Circular en Contenido Libre
*  **Description:** Sesión enfocada en la Fase 9 del Hito 22, destinada a la estabilización de la refactorización de navegación. Se abordará prioritariamente la resolución del error de "navegación circular" (Pink Floyd) detectado en los enlaces de Contenido Libre, asegurando la correcta jerarquía y accesibilidad en la nueva arquitectura centrada en el usuario.

*   **Session:** Resolución de Error de Integridad por Slug Duplicado en Generación de Contenido
*   **Description:** Análisis y corrección del fallo `IntegrityError 1062` en la tabla `contents_contentmaterial` durante la ejecución de tareas de orquestación. El objetivo es depurar la lógica de asignación de slugs vacíos y asegurar la unicidad mediante validación robusta en el modelo y señales.

# 2025-11-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md
## EPI
*  **Session:** Resolución de Integridad de Datos en Slugs de ContentMaterial
*  **Description:** Implementación de lógica robusta de generación de slugs únicos en el modelo ContentMaterial para mitigar errores de integridad (Duplicate entry 1062) durante la creación de contenido, asegurando la unicidad antes de la persistencia en base de datos.

*  **Session:** Reanudación Hito 6: Integración de Evaluaciones con Nueva Navegación
*  **Description:** Reactivación del desarrollo del sistema de autoevaluaciones tras la finalización del Hito 22. Se procederá a integrar el flujo de evaluaciones con el nuevo modelo UserStudyNavigation en la aplicación contents, eliminando la dependencia de la navegación jerárquica obsoleta y verificando la accesibilidad de las copias de estudio.


# 23/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Unificación de UI de Evaluación y Sistema de Logs
*  **Description:** Implementación del sistema de logs en el modelo Assessment para visibilidad en el admin y unificación de la lógica de estado de evaluación en el frontend (Lista de Copias, Sidebar y Tarjetas) para garantizar coherencia visual con la NavBar.

# 2025-11-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Reparación Sistema Autoevaluación: Logs Mudos y Navegación Desincronizada
*  **Description:** Sesión de emergencia para corregir fallos críticos en el Hito 6. Se implementará la escritura atómica en `event_log` dentro de las tareas de Celery para solucionar la ausencia de logs. Además, se auditará y reparará la lógica de señales y caché en `assessment/signals.py` y `contents/services/navigation_builder.py` para resolver la desincronización en la navegación.


# 2025-11-23
# CAMPUSTUDIONLINE --ROADMAP
# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)
## EPI
*  **Session:** Reparación de Logs de Evaluación y Sincronización de Navegación
*  **Description:** Implementación de escritura atómica en el event_log para tareas de Celery y corrección de la desincronización en la barra de navegación y sidebar mediante auditoría de señales y caché.

# 2025-11-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Reparación Logs y Navegación Assessment
*  **Description:** Sesión crítica de depuración del Hito 6. Se aborda la falta de persistencia en los logs del modelo Assessment (fallo silencioso en tareas de Celery) y la desincronización de la navegación de usuario (Sidebar/NavBar) tras la generación de autoevaluaciones. Se revisará la transaccionalidad en orchestrator/tasks.py y assessment/signals.py.


# 2025-11-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V03.md
## EDC
* Session: Reactivación del Ecosistema de Chat Contextual
* Description: Análisis e implementación de la nueva arquitectura de chat basada en el contexto de estudio (Hito 3). Se abordará la refactorización de los modelos de chat para vincularlos automáticamente a asignaturas y categorías, eliminando la creación manual de salas y estableciendo activadores automáticos en la creación de usuarios y copias de contenido.

# 2025-11-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md
## NRA
*  **Session:** Recuperación de Visibilidad de API Keys y Gestión de Logs
*  **Description:** Sesión enfocada en resolver la regresión visual de las API Keys en el orquestador y diseñar el sistema de offloading de logs a local, cumpliendo los objetivos del Hito 5.

# 2025-11-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md
## CSO
* Session: Unificación UX/UI y Navegación
* Description: Implementación de mejoras de interfaz de usuario centradas en la estandarización visual de botones, corrección de literales en la Sala de Estudio y reubicación estratégica del acceso al Explorador en la barra de navegación principal.


# 2025-11-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md
## CSO
*  **Session:** Unificación UX/UI: Estandarización de botones y mejoras en navegación
*  **Description:** Sesión centrada en la mejora de la Experiencia de Usuario (UX) y la Interfaz de Usuario (UI). Se abordará la estandarización visual de los botones en toda la plataforma, asegurando coherencia en tamaño, paleta de colores y leyendas. Se corregirán literales confusos en la Sala de Estudio. Además, se reubicará el acceso al Explorador a la barra de navegación principal (NavBar) mediante un icono tipo hamburguesa y se ajustará el contexto de navegación en dicha sección.


# 2025-11-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md
## CSO
*  **Session:** Mantenimiento V05: Corrección de Indicadores de Estado en Evaluaciones
*  **Description:** Corrección de la inconsistencia en los badges de notificación de la NavBar relativa a las autoevaluaciones. Se ajustará la lógica de visualización (probablemente en `_navbar_indicators.html` y sus dependencias) para asegurar que el spinner de "En progreso" aparezca inmediatamente tras la solicitud (`REQUESTED`), y no solo durante la corrección, mejorando el feedback al usuario.


# 2025-11-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md
## PLUTO
*  **Session:** Corrección de Redundancia en Visualización de Contenidos
*  **Description:** Eliminación de la duplicidad del texto de resumen en la vista de detalle de contenidos, donde se renderiza tanto en la tarjeta de cabecera como en el cuerpo principal. Se modificará la plantilla `content_detail.html`.


# 2025-11-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md
## AAAA
*  **Session:** Refactorización de Tours Interactivos Shepherd.js tras Cambios de UI
*  **Description:** Auditoría y reparación de los scripts de tours guiados (Shepherd.js) que han quedado obsoletos debido a cambios estructurales recientes en la interfaz (NavBar, Sidebar y unificación de vistas). El objetivo es actualizar los selectores del DOM en los archivos home_tour.js, content_detail_tour.js y study_room_tour.js para restaurar la funcionalidad de la ayuda interactiva en el Home, el Detalle de Contenido y la Sala de Estudio.

# 2025-11-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V07.md
## CYC
*  **Session:** Implementación de Sistema de Reporte de Errores y App Feedback
*  **Description:** Inicio del Hito 7. Desarrollo del backend para ContentReport y la aplicación de feedback. Integración de botón de reporte en el frontend de contenidos.


# 2025-11-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V08.md
## EPI
*  **Session:** Estandarización de Imagen Corporativa en Emails
*  **Description:** Inicio de la sesión para auditar y estandarizar las plantillas de correo electrónico del sistema, asegurando coherencia visual y técnica mediante la implementación de una plantilla base HTML responsiva y la migración de notificaciones existentes en los módulos de feedback, usuarios y evaluación.


# 2025-11-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V23.md
## MAMC
*  **Session:** Implementación de Cumplimiento Normativo (RGPD/LSSI) - Hito 23
*  **Description:** Inicio de las tareas del Hito 23 enfocadas en el cumplimiento legal. Se abordará la creación de vistas y plantillas para Aviso Legal, Política de Privacidad y Cookies, la implementación del banner de consentimiento de cookies en el frontend y la actualización de los formularios de registro de usuarios para incluir la aceptación obligatoria de términos.


# 2025-11-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V14.md
## EDC
*  **Session:** Corrección Visual en Privacidad y Refactorización DRY de Favoritos
*  **Description:** Sesión centrada en la resolución de la regresión visual en el formulario de configuración de privacidad del usuario (Tarea 4.1). Posteriormente, se abordará la deuda técnica identificada en la gestión de favoritos (Tarea 2.3), centralizando la lógica de anotación 'is_favorite' en una utilidad común para eliminar la duplicidad de código existente entre las aplicaciones 'contents', 'academic_directory' y 'search'.


# 2025-11-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V02.md
## NRA
*  **Session:** Reactivación Hito 2: Optimización SEO
*  **Description:** Reanudación de las tareas de optimización para motores de búsqueda (SEO) definidas en el Hito 2. El objetivo es implementar mejoras en la visibilidad pública de la plataforma, incluyendo sitemaps y meta-tags, para potenciar el posicionamiento orgánico del contenido académico y los materiales de estudio.


# 2025-11-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V13.md
## PLUTO
*  **Session:** Generación de Documentación Técnica - Hito Final 2
*  **Description:** Reactivación del Hito Final 2 para la elaboración de la documentación técnica del proyecto "La Enciclopedia Galáctica". La sesión se centrará en el análisis de la arquitectura de datos para desarrollar el Manual de Arquitectura y la Referencia de Componentes.


# 2025-11-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V18.md
## AAAA
*  **Session:** Corrección de Error en Creación de Contenido Libre - Campo Author Inexistente
*  **Description:** Se aborda un error crítico reportado durante la creación de contenido libre (biografías), donde la instanciación de `ContentMaterial` falla por un argumento inesperado 'author'. Se investigará `contents/models.py` y la lógica de creación de tareas en `orchestrator` para alinear los argumentos con la definición del modelo, restaurando la funcionalidad de generación de contenido libre.


# 2025-11-28
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V13.md
## CYC
*  **Session:** Reanudación Hito Final 2: Documentación Técnica
*  **Description:** Reactivación del Hito Final 2 tras la finalización de las intervenciones de hotfix crítico. La sesión se centrará en avanzar con la redacción del "Manual de Arquitectura" y la "Referencia de Componentes" para conformar la documentación técnica del proyecto, analizando los modelos de datos principales.


# 2025-11-29
# CAMPUSTUDIONLINE --ROADMAP (Emergency Fix)
# CAMPUSTUDIONLINE_DB_CRISIS_RESOLUTION_SESSION_SUMMARY.md
## PCS
*  **Session:** Resolución de Crisis de Base de Datos (Quota Exceeded)
*  **Description:** Reducción exitosa del tamaño de la BBDD de 34.5GB a 1.9GB mediante reconstrucción de tabla. Implementación de truncado de logs preventivo. Registro de bugs para próxima sesión.

# 2025-11-29
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## MAMC
*  **Session:** Resolución de Incidencias en Admin Users y Personal Workspace
*  **Description:** Corrección del Error 500 en la vista de modificación de usuarios en el panel de administración, provocado por discrepancias entre los campos de `UserProfile` definidos en `users/admin.py` y el modelo actual. Subsanación del `TemplateSyntaxError` en `contents/templates/contents/personal_workspace.html` debido a una carga incorrecta o ausente de la etiqueta `static`.


# 30/11/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## EDC
*  **Session:** Optimización de Vista de Publicaciones y Refinamiento UI
*  **Description:** Implementación de paginación en la sección 'Mis Publicaciones' para prevenir sobrecarga del sistema. Eliminación de mensajes de estado redundantes en vistas sin jerarquía de directorios.

# 2025-11-30
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## NRA
*  **Session:** Depuración de Integridad en Árbol de Carpetas Favoritas
*  **Description:** Análisis y resolución del error crítico `Column 'depth' cannot be null` en el modelo `FavoriteFolder` durante la creación automática de carpetas al copiar contenido. Se auditará la implementación de `get_or_create` en la vista `study_room_views.py` para asegurar la compatibilidad con la estructura jerárquica del modelo, sustituyendo la creación estándar por los métodos de inserción de nodos de árbol requeridos.


# 2025-11-30
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## PLUTO
*  **Session:** Implementación de Seguridad DRM en Frontend y UX Loading Spinner
*  **Description:** Abordaje de dos mejoras críticas de experiencia y seguridad. Primero, la implementación de medidas disuasorias contra la copia no autorizada de contenido (DRM Frontend) mediante ofuscación CSS, marcas de agua dinámicas y bloqueo de eventos de teclado/ratón en las vistas de detalle de material de estudio, adaptadas tanto para escritorio como para navegadores móviles. Segundo, la integración de un indicador de carga ("Loading Spinner") global para estandarizar el feedback visual durante las transiciones y peticiones asíncronas en toda la plataforma, activando el protocolo PAIR para asegurar consistencia con los recursos existentes (e.g., preloader.css).


# 2025-12-01
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Estabilización del Motor de Generación de Contenido y Diagnóstico Celery
*  **Description:** Diagnóstico y resolución de incidencias en el motor de generación de contenido (Celery). Análisis de bucles infinitos en tareas de contenido libre y fallos en el parser de respuestas de IA. Implementación de mejoras de robustez en el parsing y límites de reintentos para protección de cuota API.


# 2025-12-01
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CYC
*  **Session:** Soporte y Mantenimiento V24 - Monitorización y Consultas
*  **Description:** Sesión de continuidad bajo el hito de soporte y mantenimiento. El sistema ha alcanzado una estabilidad operativa tras las correcciones en el orquestador y los parsers de contenido. El objetivo de la sesión es atender consultas puntuales, realizar verificaciones de estado o abordar incidencias emergentes durante la fase de monitorización pasiva.


# 2025-12-04
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## MAMC
*  **Session:** Sesión de Monitorización y Mantenimiento Correctivo (Hito 24)
*  **Description:** Continuación de las tareas de soporte bajo el Hito 24 "Ruegos y Preguntas". Tras la estabilización de los flujos de generación de contenido, manejo de errores de copyright (Recitation) y mejoras en la orquestación, esta sesión se dedica a la atención de nuevas incidencias, consultas de arquitectura o ajustes menores que surjan de la operación en producción o pruebas de usuario. Se mantiene el estado de alerta pasiva.


# 2025-12-07
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## NRA
*  **Session:** Continuidad de Soporte y Mantenimiento Correctivo
*  **Description:** Sesión de mantenimiento bajo el hito V24 enfocada en la monitorización del sistema y resolución de incidencias a demanda.


# 2025-12-07
# CAMPUSTUDIONLINE --ROADMAP # CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CSO
*  **Session:** Continuación Depuración Sidebar y Monitorización de Mantenimiento
*  **Description:** Sesión bajo el Hito 24 centrada en resolver la inconsistencia visual persistente en la barra lateral de navegación (Sidebar), investigando posibles causas en caché, renderizado o transmisión de datos al frontend tras las correcciones de backend previas. Se mantiene la vigilancia operativa para mantenimiento correctivo.


# 2025-12-07
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## PLUTO
*  **Session:** Mantenimiento y Soporte: Monitorización Post-Despliegue
*  **Description:** Sesión de continuidad bajo el hito de soporte. Seguimiento tras la resolución de inconsistencias en la Sidebar y mejoras de UX. El sistema se encuentra en fase de monitorización pasiva a la espera de nuevas incidencias o tareas de mantenimiento correctivo.


# 2025-12-07
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CYC
*  **Session:** Soporte y Mantenimiento - Fase de Monitorización
*  **Description:** Sesión de continuidad bajo el hito V24. El sistema se encuentra estabilizado tras las correcciones críticas de gestión de cuotas y almacenamiento. Se mantiene la vigilancia activa y se atienden solicitudes de mantenimiento correctivo o dudas puntuales sobre la arquitectura actual.


# 07/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## EPI
*  **Session:** Sesión de Monitorización y Mantenimiento - Fase de Estabilización
*  **Description:** Inicio de sesión de continuidad en el hito de soporte. Tras la restauración de la lógica de asignación de cuotas de API y la resolución de la crisis de almacenamiento, el objetivo es monitorizar la estabilidad del sistema y atender nuevas solicitudes de mantenimiento o depuración que surjan.


# 08/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## MAMC
*  **Session:** Auditoría Forense de Orquestación y Sincronización Horaria Celery-Django
*  **Description:** Inicio de sesión de emergencia bajo protocolo de crisis. El objetivo único es realizar una auditoría forense del archivo `orchestrator/tasks.py` mediante el análisis de su historial de git (`git log -p`) para identificar la causa raíz de los bucles de reintentos y la corrupción lógica en el manejo de tiempos (`countdown`/`eta`). Se suspende cualquier generación de código hasta completar el análisis y aprobar un plan de acción.


# 2025-12-08
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## EDC
*  **Session:** Implementación de Modelo de Datos Resiliente para Orquestación de Tareas
*  **Description:** Se procede a la implementación de los campos de control de resiliencia en el modelo PendingContentTask de la aplicación orchestrator. El objetivo es prevenir bucles infinitos y mejorar la gestión de errores de API mediante la adición de contadores persistentes (global_actuation_count, consecutive_api_errors), marcas de tiempo de error (last_api_error_at), rastreo de claves fallidas (last_error_api_key) y latidos (last_heartbeat). Esta modificación establece la base para la reingeniería del orquestador, permitiendo un control de flujo robusto y la detección de tareas zombies.


# 08/12/2025
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## EDC
*  **Session:** Implementación de Campos de Resiliencia y Control en Modelo PendingContentTask
*  **Description:** Se procede a modificar `orchestrator/models.py` para integrar los campos de control de fallos definidos en la auditoría forense (`global_actuation_count`, `consecutive_api_errors`, `last_api_error_at`, `last_error_api_key`, `current_step`, `last_heartbeat`). Esta modificación establece la base de datos necesaria para la posterior refactorización del orquestador, dotando a las tareas de memoria persistente frente a reinicios y bucles infinitos, y permitiendo una gestión granular de errores de API.

# 08/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## NRA
*  **Session:** Análisis Forense del Orquestador y Depuración de Celery
*  **Description:** Ejecución de análisis forense sobre los logs de Celery y el código fuente de `orchestrator` para identificar la causa raíz de la inoperatividad persistente. Verificación de la integridad de los datos en `PendingContentTask` y `AutomationSettings` tras las últimas migraciones. Depuración de la lógica de reanudación y gestión de errores en `generate_full_course_task`.

# 2025-12-10
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## PLUTO
*  **Session:** Restauración del Mecanismo de Content Gating y Efecto Fade-out
*  **Description:** Corrección de una regresión en la aplicación 'contents'. Se busca restaurar el comportamiento para usuarios no autenticados (visitantes) al intentar acceder a detalles de contenido o áreas restringidas como la Sala de Estudio. El objetivo es recuperar la visualización parcial del contenido con un efecto de desvanecimiento (fade-out) y el enlace de llamada a la acción (CTA) para el registro, que actualmente no se están renderizando correctamente.


# 2025-12-11
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## PLUTO
*  **Session:** Soporte y Mantenimiento de Plataforma - Hito 24
*  **Description:** Sesión dedicada al mantenimiento correctivo integral y soporte técnico bajo el Hito 24. Incluye la monitorización de la estabilidad del orquestador tras la refactorización reciente y la resolución de incidencias técnicas en cualquier módulo de la plataforma, priorizando la estabilidad y la experiencia de usuario.


# 2025-12-11
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Soporte Continuo: Mantenimiento Correctivo y Monitorización
*  **Description:** Sesión de continuidad bajo el Hito 24 (Ruegos y Preguntas). Enfoque en mantenimiento correctivo integral y monitorización de la estabilidad del orquestador y la UX, tras las recientes optimizaciones de búsqueda y correcciones críticas en el orquestador.


# 2025-12-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Inicio de Sesión de Soporte y Mantenimiento - Hito 24
*  **Description:** Inicio de sesión estándar bajo el Hito de Soporte y Mantenimiento (V24). El sistema se encuentra en estado de espera para recibir instrucciones específicas de mantenimiento correctivo, monitorización o resolución de dudas (Ruegos y Preguntas). Se han cargado los contextos del proyecto CampuStudiOnline.


# 2025-12-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CYC
*  **Session:** Corrección Crítica Redis DB Index Out of Range
*  **Description:** Resolución de bloqueo en Celery/Redis (`kombu.exceptions.OperationalError: DB index is out of range`). Tras la migración a Redis DB 1 indicada en la bitácora anterior, el servicio rechaza la conexión. Se prioriza la corrección de `core/settings.py` para restaurar la operatividad de la mensajería y el orquestador antes de proceder con las tareas de mantenimiento programadas.


# 2025-12-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V26.md
## EPI
*  **Session:** Corrección de textos de interfaz en lista de conversaciones privadas
*  **Description:** Se aborda la eliminación de textos estáticos en inglés en la vista de lista de conversaciones de la aplicación messaging. Se modificará la lógica de la vista para recuperar el último mensaje y se actualizará la plantilla para mostrarlo, cumpliendo con la Regla de Oro del Idioma (UI en castellano).


# 2025-12-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V25.md
## PLUTO
*  **Session:** Hito 25: Inicio de Estrategia Meta Ads e Infraestructura de Tracking
*  **Description:** Subsanación de inconsistencia documental creando el anexo del Hito 25 (V25). Inicio de la implementación de la estrategia de Meta Ads. Se define la hoja de ruta técnica que incluye la implementación híbrida de seguimiento (Pixel + CAPI), configuración de eventos estándar de conversión y preparación de templates para Landing Pages.


# 2025-12-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V25.md
## MAMC
*  **Session:** Implementación de Eventos de Conversión Meta Ads: Lead, ViewContent e InitiateCheckout
*  **Description:** Continuación del Hito 25. Implementación de eventos de conversión estándar de Meta (Pixel + CAPI) en puntos clave de la navegación: 'ViewContent' en materiales de estudio, 'Lead' en formularios de contacto e 'InitiateCheckout'. Se extenderá la lógica de tareas asíncronas centralizada para soportar estos nuevos eventos server-side.


# 2025-12-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V25.md
## EDC
*  **Session:** Verificación de Eventos y Feed para Meta Ads
*  **Description:** Validación técnica de la implementación del catálogo de productos y la transmisión de eventos (CAPI/Pixel) para el lanzamiento de la campaña. Revisión de modelos implicados en la generación del feed y conversiones.


# 2025-12-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V25.md
## NRA
*  **Session:** Verificación de Eventos Meta CAPI y Preparación de Campaña
*  **Description:** Continuación del Hito 25. Tras la corrección del feed de catálogo, el objetivo es verificar la correcta recepción y deduplicación de eventos (ViewContent, Lead, RequestAssessment) en el Events Manager de Meta. Se asistirá en la validación de la implementación híbrida (Pixel + CAPI) y se comenzará con la preparación de los activos para la campaña.


# 2025-12-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Hito 24: Auditoría del Orquestador de Contenido y Estrategia de IA
*  **Description:** Sesión enfocada en la validación empírica de los controles de flujo del orquestador de contenido (pausa/reanudación) y el análisis de la priorización de tareas en Celery. Se abordará también la investigación de cuotas de la API de Gemini para evaluar la viabilidad de nuevos modelos.


# 2025-12-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CYC
*  **Session:** Mantenimiento y Estabilidad del Sistema (Hito 24)
*  **Description:** Sesión dedicada a la vigilancia operativa y resolución de incidencias bajo demanda, priorizando la estabilidad de la plataforma y la experiencia de usuario según las directrices del Hito 24.


# 2025-12-16
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Sesión de Mantenimiento y Soporte - Hito 24
*  **Description:** Inicio de sesión bajo el Hito 24 (Ruegos y Preguntas). El sistema está configurado para priorizar la estabilidad y la atención de incidencias bajo demanda. Se consolidan las tareas de orquestación híbrida y gestión de costes. Preparada para intervenciones de mantenimiento correctivo o evolutivo.


# 2025-12-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V27.md
## CYC
*  **Session:** Hito 27: Optimización de UX y Onboarding
*  **Description:** Corrección del documento maestro para reflejar el hito actual. Inicio de los trabajos de mejora en la interfaz y experiencia de usuario para el módulo de autoevaluaciones, incluyendo auditoría de visibilidad y onboarding guiado.


# 2025-12-16
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V27.md
## EPI
*  **Session:** Optimización UX Evaluaciones: Diagnóstico y Visibilidad
*  **Description:** Inicio de la fase de ejecución del Hito 27. Se abordará la auditoría de visibilidad de la funcionalidad de autoevaluaciones. El objetivo es identificar barreras de usabilidad en el Dashboard y la barra de navegación que impiden el descubrimiento de la función. Se procederá al análisis de las plantillas actuales y se planificarán las modificaciones visuales y de flujo (CTA, Tours) para mejorar el onboarding.


# 2025-12-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V28.md
## PLUTO
*  **Session:** Hito 28: Arranque de UniversIA - Definición e Infraestructura
*  **Description:** Inicio del Hito 28. Se abordará la implementación del asistente contextual 'UniversIA'. En esta sesión, nos centraremos en la definición táctica del 'System Prompt' y la personalidad del asistente, así como en la preparación de la infraestructura backend para la integración con la API de Google Gemini (aprovechando el SDK existente). También se planteará el diseño inicial del widget flotante para la interfaz de usuario.


# 2025-12-17
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
# PLUTO
*  **Session:** Soporte y Mantenimiento: Inicio de Sesión de Ruegos y Preguntas
*  **Description:** Inicio de sesión bajo el hito de soporte continuo. Carga de documentos maestros y establecimiento del contexto para abordar deuda técnica, bugs menores o nuevas peticiones del usuario según surjan. Estado actual del hito: EN PROGRESO.


# 17/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## MAMC
*  **Session:** Sesión de Soporte: Monitorización UniversIA y Mantenimiento Continuo
*  **Description:** Inicio de sesión de mantenimiento bajo el hito V24. El foco principal es la revisión post-despliegue del asistente 'UniversIA', incluyendo monitorización de logs y consumo de cuotas. Se mantiene un backlog abierto para resolver deuda técnica, bugs menores y peticiones de calidad de vida (QoL) que surjan.


# 2025-12-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Soporte y Mantenimiento: Monitorización UniversIA y Backlog
*  **Description:** Continuación del hito de soporte. Análisis de logs tras el despliegue del asistente UniversIA, monitorización de cuotas de API y gestión de deuda técnica o nuevas peticiones.


# 2025-12-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Soporte y Mantenimiento: Monitorización UniversIA y Backlog
*  **Description:** Continuación del hito de soporte. Análisis de logs tras el despliegue del asistente UniversIA, monitorización de cuotas de API y gestión de deuda técnica o nuevas peticiones.


# 2025-12-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Resolución de Incidencias y Mantenimiento Correctivo (V24)
*  **Description:** Sesión orientada a la resolución de incidencias ad-hoc y tareas de mantenimiento dentro del marco del Hito V24. Se han cargado los documentos de sesión y se ha verificado el estado del backlog táctico. El objetivo principal es abordar la deuda técnica y las peticiones pendientes para asegurar la estabilidad operativa de la plataforma CampuStudiOnline.

# 2025-12-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md
## AAAA
*  **Session:** Extensión Global de UniversIA (Hito V29)
*  **Description:** Re-orientación estratégica de la sesión tras la decisión de universalizar UniversIA. Se ha pausado el Hito V24 y se ha activado el Hito V29. Se ha creado el anexo correspondiente y actualizado el Documento Maestro. El objetivo técnico es implementar una lógica de discriminación de contexto para que el asistente ofrezca soporte de navegación en toda la plataforma y ayuda pedagógica exclusiva en la Sala de Estudio.


# 20/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Sesión de Mantenimiento y Soporte V24 - Resolución de Incidencias Ad-hoc
*  **Description:** Inicio de sesión bajo el hito V24 (Ruegos y Preguntas). Se establece la carga del entorno para el proyecto CAMPUSTUDIONLINE en dispositivo Android. El objetivo principal de la interacción es la gestión de deuda técnica, bugs menores y peticiones específicas según el backlog dinámico del hito.


# 20/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V30.md
## CYC
*  **Session:** Hito 30: Modelado del Sistema de Afiliados y Lógica de Registro
*  **Description:** Inicio de la implementación técnica del sistema de recomendación comercial. Se procederá a: 1) Analizar y definir los modelos de datos para los códigos de recomendación (RecommendationCode) y su relación con los usuarios (Comerciales y Afiliados). 2) Implementar la lógica de validación de códigos durante el proceso de registro de nuevos usuarios. 3) Diseñar el sistema de traza de conversiones mediante signals para eventos clave (registro, primera copia, primera evaluación).

# 2025-12-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V30.md
## EPI
*  **Session:** Implementación Arquitectura Datos Atribución Comercial
*  **Description:** Inicio Hito 30. Fase 1: Definición de modelos para sistema de referidos. Creación de `RecommendationCode` en `users` y actualización de `UserProfile` con flags de incentivos y campo `referred_by`.


# 2025-12-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## AAAA
*  **Session:** Sesión de Mantenimiento y Soporte (Hito 24)
*  **Description:** Reactivación del Hito 24 tras restauración de versión correcta. Sesión dedicada a la resolución de incidencias, deuda técnica y peticiones ad-hoc según el backlog dinámico de soporte.


# 2025-12-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md
## CYC
*  **Session:** Creación App Schedule y Modelo AcademicEvent
*  **Description:** Inicio del Hito 31. Inicialización de la aplicación 'schedule' para la agenda académica. Definición del modelo 'AcademicEvent' con soporte para diferentes tipos de eventos (Examen, Clase, Entrega, Estudio, Otro), validaciones de integridad temporal y relaciones con usuarios y asignaturas. Registro en Django Admin y configuración inicial en settings.


# 2025-12-24
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md
## EPI
*  **Session:** Reparación Frontend Agenda y Verificación Alertas
*  **Description:** Diagnóstico y resolución del bloqueo crítico en el frontend de la aplicación 'schedule' (pantalla en blanco, fallo de renderizado FullCalendar). Verificación del endpoint '/api/feed/'. Validación integral del sistema de notificaciones proactivas (Celery Beat, Push, Email) para eventos académicos.


# 25/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md
## EPI
*  **Session:** Hotfix: Optimización del Protocolo PADP y Manifiestos
*  **Description:** Intervención de mantenimiento del sistema. Se ha diagnosticado y resuelto el desbordamiento del manifiesto de proyecto causado por la indexación no filtrada de archivos estáticos. Se ha parcheado el archivo 'SYSTEM_PROMPTS.md' implementando un filtrado estricto por extensiones en el protocolo 'PADP'. Se han regenerado los manifiestos de Sistema y Proyecto con la nueva configuración para restaurar la operatividad del protocolo PISA en futuras sesiones.


# 25/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md
## PLUTO
*  **Session:** UniversIA: Branding, Interactividad y Skill Agenda
*  **Description:** Implementación de mejoras visuales y funcionales para el asistente UniversIA según la hoja de ruta 'Extension de UniversIA'. Se abordarán tres frentes: 1) Actualización de la identidad visual del botón flotante en la interfaz base. 2) Implementación de funcionalidad 'Long Press to Drag' en JavaScript para permitir el reposicionamiento del asistente. 3) Desarrollo de la lógica backend en 'services.py' para la interpretación de comandos de lenguaje natural destinados a la creación de eventos en la agenda académica (Schedule).


# 2025-12-25
# CAMPUSTUDIONLINE --CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md
## MAMC
*  **Session:** Diagnóstico de UniversIA en Web y Auditoría de Entorno
*  **Description:** Sesión dedicada a resolver la discrepancia de funcionamiento de UniversIA entre CLI (funcional) y entorno Web (fallo). Se auditará la inyección de variables de entorno en WSGI, la estructura del historial de chat para el SDK de Gemini y la persistencia de metadatos de contexto.


# 2025-12-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md
## MAMC
*  **Session:** Diagnóstico y Corrección de UniversIA en Entorno Web
*  **Description:** Sesión centrada en la investigación y resolución del fallo crítico donde el asistente UniversIA funciona en CLI pero falla en entorno Web (WSGI). Se auditará la carga de variables de entorno, la compatibilidad del historial del SDK de Gemini y la persistencia del contexto.


# 26/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md
## EDC
*  **Session:** Restauración de UI y Refactorización de Lógica de Borrado en Agenda Académica
*  **Description:** Sesión técnica orientada a la reversión de los cambios visuales en el módulo Schedule que afectaron la integridad del layout de FullCalendar. Se trabajará en la eliminación de atributos 'onclick' globales para el borrado de eventos, sustituyéndolos por un sistema de gestión de eventos en el DOM más robusto y encapsulado. Asimismo, se optimizará la visualización móvil para evitar solapamientos y se unificarán las respuestas AJAX en el backend para asegurar la consistencia en las operaciones de creación, edición y eliminación de eventos académicos.

# 2025-12-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md
## NRA
*  **Session:** Debugging Pantalla Blanca Borrado Eventos Schedule
*  **Description:** Investigación y resolución del bloqueo técnico en el módulo Schedule donde el borrado de eventos provoca una pantalla blanca. Verificación del flujo AJAX con la estrategia de bypass de cabeceras (is_ajax=true) para evitar redirecciones 302 erróneas y garantizar respuestas JSON. Refinamiento final de UI móvil.


# 2025-12-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V32.md
## CSO
*  **Session:** Integración de UniversIA y Agenda en el Sistema de Visitas Guiadas
*  **Description:** Ejecución del Hito 32. Se actualizará el tour de la página de inicio para incluir la explicación detallada de los roles del asistente UniversIA (Global vs Contextual). Se creará un nuevo tour específico para el módulo de Agenda (Schedule) explicando la navegación y gestión de eventos. Se registrarán los cambios en la plantilla base.


# 27/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CAMA
*  **Session:** Hito 24: Sistema de Ruegos y Preguntas - Sesión de Soporte
*  **Description:** Sesión de guardia bajo el Hito 24. El objetivo es atender incidencias, dudas o mantenimientos correctivos no planificados en la plataforma CampuStudiOnline. Se cargan los modelos base de usuarios y contenidos como contexto inicial, quedando a la espera de instrucciones específicas del usuario para abordar la tarea requerida.


# 2025-12-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## AAAA
*  **Session:** Sesión de Continuidad: Refinamiento del Scraping de Datos (Hito 20)
*  **Description:** Inicio de la sesión para retomar el Hito 20 centrado en el refinamiento del proceso de scraping de datos. Se procederá a analizar el anexo correspondiente para determinar las tareas técnicas pendientes y se cargarán los modelos fundamentales para asegurar la integridad de la lógica de persistencia.
# 2025-12-28
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## CYC
*  **Session:** Ingesta de Datos Académicos UCO y Deduplicación
*  **Description:** Desarrollo del comando de gestión `import_uco_data` para la ingesta masiva de la estructura académica y contenidos de la Universidad de Córdoba desde `uco_data_final.json`. Clasificación por ramas de conocimiento, creación de jerarquía (Universidad, Rama, Grado, Asignatura) y persistencia de metadatos (objetivos, temario, bibliografía). Ejecución de validación de integridad y deduplicación mediante `calculate_content_hashes`.


# 2025-12-29
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## EPI
*  **Session:** Ingesta de Datos UCO: Fase PC y Fusión
*  **Description:** Implementación y ejecución del protocolo de cosecha de datos de la UCO en entorno local (PC) para superar las limitaciones de memoria en Android. Creación del script `uco_harvester_pc.py` con soporte para los 8 arquetipos de navegación HTML detectados y aplicación de la matriz de exclusión estricta. Fusión posterior de los datos cosechados con el respaldo de contenidos (`uco_data_backup.json`) y preparación de la carga masiva en servidor mediante `uco_pdf_processor.py` e `import_uco_data`.


# 30/12/2025
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## PLUTO
*  **Session:** Ingesta de Datos UCO - Cambio de Estrategia a Carga Manual
*  **Description:** Sesión enfocada en la ingesta de datos de la Universidad de Córdoba tras la purga completa de sus registros en la base de datos. Se abandona el descubrimiento automático por Selenium en favor de una carga hardcodeada de 31 URLs de planificación recopiladas manualmente. El objetivo es implementar el script UCO_HARVESTER_V19 para procesar la estructura de acordeones y tablas de la UCO, aplicando filtros agresivos de exclusión de contenidos no académicos. Se toma conocimiento de un cambio de planes inminente en la hoja de ruta por parte del usuario.

# 2025-12-30
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## MAMC
*  **Session:** UCO Ingesta V19: Scraping Dirigido
*  **Description:** Implementación de mecanismo de ingesta para la Universidad de Córdoba mediante scraping dirigido por lista manual de URLs. Desarrollo del script 'UCO_HARVESTER_V19' para procesamiento local, integrando lógica de extracción de planificaciones académicas con BeautifulSoup, selectores de año por acordeón y filtrado estricto de asignaturas. Generación de JSON maestro para posterior carga en servidor.


# 2025-12-30
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## MAMC
*  **Session:** UCO Ingesta V19: Scraping Dirigido
*  **Description:** Implementación de mecanismo de ingesta para la Universidad de Córdoba mediante scraping dirigido por lista manual de URLs. Desarrollo del script 'UCO_HARVESTER_V19' para procesamiento local, integrando lógica de extracción de planificaciones académicas con BeautifulSoup, selectores de año por acordeón y filtrado estricto de asignaturas. Generación de JSON maestro para posterior carga en servidor.


# 2026-01-03
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V33.md
## AAAA
*  **Session:** Optimización UX Envío Circulares
*  **Description:** Refactorización del formulario de envío de correos administrativos en `global_settings`. Eliminación de la inyección oculta de saludos/despedidas en el backend. Implementación de pre-poblado en el formulario para garantizar que el administrador tenga control total y visible sobre el contenido final del correo ("Lo que ves es lo que envías"), evitando duplicidades en los textos.


# 2026-01-03
# CAMPUSTUDIONLINE --# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V34.md
## CYC
*  **Session:** Optimización Open Graph y Rebranding Twitter a X
*  **Description:** Diagnóstico y corrección de la generación de imágenes para compartir (Open Graph) en `contents/utils.py`. Verificación de URLs absolutas en metatags. Actualización de iconografía obsoleta de Twitter por "X" en toda la plataforma.


# 2026-01-03
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V33.md
## PLUTO
*  **Session:** Hito 33 - Fase 2: Visibilidad de Suscripciones y Auditoría
*  **Description:** Exposición de preferencias RGPD en Admin y auditoría de listas de distribución.


# 2026-01-04
# CAMPUSTUDIONLINE --ROADMAP
# SYSTEM_PROMPTS_REPAIR
## CYC
*  **Session:** Reparación de System Prompts y Limpieza de Raíz
*  **Description:** Sesión destinada originalmente a hoja de ruta, desviada a mantenimiento crítico del sistema. Se detectó y corrigió un conflicto en el protocolo `PIEE -> A`, estableciendo obligatoriamente la concatenación del lado del cliente (`Client Side`) y prohibiendo scripts en el servidor para descargas. Se modificó `SYSTEM_PROMPTS.md` para blindar el protocolo `PMA` (exigiendo `heredoc` y `re`, prohibiendo `python -c`) y se añadió una directriz de higiene vinculante para forzar la ubicación de scripts temporales en `{SERVER_SWAP}`. Adicionalmente, se saneó la raíz del proyecto `CampuStudiOnline` moviendo archivos basura y scripts huérfanos a `TRASH_BIN`.

# 2026-01-04
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md
## EPI
*  **Session:** Hardening de Frontend y Ajuste de Comportamiento para UniversIA
*  **Description:** Implementación de bloqueos de seguridad en la interfaz de chat de UniversIA para prevenir inyecciones de texto masivas (copiar/pegar). Refinamiento del prompt del sistema para restringir respuestas académicas fuera de la Sala de Estudio, instruyendo al asistente para derivar al usuario al flujo de trabajo correcto.


# 2026-01-04
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## PLUTO
*  **Session:** Planificación de Ingesta ESAD Córdoba
*  **Description:** Se ha definido la estrategia de ingesta para la ESAD Córdoba. Se utilizará un enfoque asistido por IA para el scraping inicial (generación de JSON) seguido de un Management Command personalizado en Django para la persistencia de datos, simplificando la lógica respecto a importadores masivos previos (UCO/UGR) al tratarse de un único grado y rama.


# 2026-01-04
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## MAMC
*  **Session:** Ingestión de Datos Académicos ESAD Córdoba
*  **Description:** Implementación del flujo de ingestión de datos para la ESAD Córdoba (Hito 20). Se procederá a la generación del dataset JSON estructurado correspondiente al Grado en Escenografía y al desarrollo del comando de gestión 'import_esad_data.py' en la aplicación 'academic_structure'. Este comando consumirá el dataset para poblar la base de datos con la nueva jerarquía académica (Universidad, Rama, Grado, Cursos y Asignaturas), utilizando la lógica de importación existente como referencia.


# 2026-01-05
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V36.md
## NRA
*  **Session:** Hito 36: Creación de la Sala de Traducción y Servicios de IA
*  **Description:** Inicio del desarrollo del módulo 'translation_room'. Configuración de la aplicación Django, routing y estructura base. Implementación de servicios de traducción usando Gemini API con soporte para documentos (PDF/DOCX) sin persistencia en BD. Integración con UniversIA y desarrollo de interfaz HTMX.

# 2026-01-05
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md
## CSO
*  **Session:** Procesamiento de Video para Publicidad Meta
*  **Description:** Desarrollo de un script de Python para aplicar efectos de desenfoque (blur) y marca de agua "CampuStudiOnline" a material videográfico para campañas publicitarias en Meta Ads, en el contexto de soporte y mantenimiento (Hito 24).


# 06/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## CSO
*  **Session:** Hito 20: Recolección Exitosa de Datos UMA (Clean Data)
*  **Description:** Harvester UMA v1.2 completado con éxito. Se han recolectado 1428 asignaturas válidas tras aplicar filtros de limpieza (exclusión de TFG, Prácticas, Movilidad, etc.). El script es autónomo, navega la jerarquía completa (Centro -> Grado -> Asignatura) y genera un JSON normalizado listo para integración.


# 2026-01-06
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## AAAA # --SYSTEM -->
*  **Session:** Integración Definitiva de Datos UMA
*  **Description:** Ejecución del proceso de recolección corregido para la Universidad de Málaga mediante script local. Generación y validación del dataset JSON completo. Importación de datos al sistema mediante Management Command y verificación de la jerarquía académica completa en base de datos.


# 07/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## PLUTO # --SYSTEM -->
*  **Session:** Refinamiento Scraper UMA "Tulipán" y Extracción PDF
*  **Description:** Implementación del script de scraping unificado "Tulipán" para la UMA, integrando navegación jerárquica (Centros/Grados) con selectores CSS estrictos (`table.t-Report-report`) para filtrar ruido. Incorporación del motor de parsing de PDF para generar JSON compatible con `academic_structure`.


# 08/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## MAMC # --SYSTEM -->
*  **Session:** Refinamiento de Datos UMA y Clasificación RUCT
*  **Description:** Purga estructural de registros UMA para eliminar duplicados y años fantasma. Reimportación de datos con lógica de clasificación RUCT estricta, validación de IDs de curso reales, normalización de nombres y filtrado de ruido (TFG, Prácticas). Verificación de integridad estructural en nuevos grados.


# 08/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## MAMC # --SYSTEM -->
*  **Session:** Refactorización y Limpieza de Datos UMA bajo Estándar RUCT
*  **Description:** Ejecución de purga estructural de datos de la UMA para eliminar inconsistencias. Implementación de lógica de importación con clasificación RUCT, limpieza de nombres y validación de IDs de curso. Verificación de integridad en grados de nueva creación.


# 08/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## EDC
*  **Session:** Depuración de Sesión APEX y Refinamiento del Scraping UMA
*  **Description:** Sesión dedicada a resolver el bloqueo técnico en la extracción universal de datos de la Universidad de Málaga (UMA). Se analizará la hipótesis de la salvaguarda de estado de sesión en Oracle APEX que impide el uso del parámetro '-1'. El objetivo es diseñar un mecanismo de navegación que emule el estado de sesión correcto o, en su defecto, implementar una captura iterativa por cursos que garantice la integridad total del JSON de origen, incluyendo el primer curso y asignaturas transversales.

# 2026-01-09
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## NRA
*   **Session:** UMA Scraping: Debugging APEX Session State
*   **Description:** Investigación del bloqueo en recolección de datos UMA (parámetro -1). Diagnóstico de salvaguardas de sesión Oracle APEX. Implementación de script de prueba para navegación persistente y estrategia de fallback iterativa por cursos para garantizar la integridad de la extracción de datos.


# 2026-01-10
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## CSO # --SYSTEM -->
*  **Session:** Inicio de Integración UJA - Reconocimiento y Harvester
*  **Description:** Análisis de la estructura web de la Universidad de Jaén. Creación del script inicial uja_harvester.py para la extracción de catálogo de grados y asignaturas. Adaptación de estrategias de scraping local para entorno Android/Termux.


# 2026-01-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## CAMA # --SYSTEM -->
*  **Session:** Adquisición y Normalización de Datos UAL
*  **Description:** Inicio de la Fase 1: Andalucía Oriental (UAL). Desarrollo de la estrategia de extracción para la Universidad de Almería, incluyendo scripts de reconocimiento (ual_harvester.py) y normalización (clean_ual_local.py) para asegurar la integridad de los datos antes de su importación a la estructura académica.


# 2026-01-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## CAMA # --SYSTEM -->
*  **Session:** Iniciando la Conquista del Este: Scraping de la UAL
*  **Description:** Inicio de la recolección de datos para la Universidad de Almería. Desarrollo del harvester inicial (ual_harvester.py) y scripts de normalización e importación para integrar la oferta académica de la UAL en la plataforma.


# 2026-01-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## AAAA # --SYSTEM -->
*  **Session:** Recuperación de Scraping UAL: Estrategia SPA y API Reverse Engineering
*  **Description:** Análisis y re-implementación de la estrategia de adquisición de datos para la Universidad de Almería (UAL). Se abordará la limitación técnica previa (sitio Angular/SPA) mediante ingeniería inversa de las peticiones API (XHR) para evitar el renderizado de JS pesado, o alternativamente mediante simulación de navegador local, asegurando la compatibilidad con el entorno de ejecución local.


# 2026-01-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V37.md
## CYC # --SYSTEM -->
*  **Session:** Migración a Gemini 3 Flash y Actualización de SDK
*  **Description:** Actualización de dependencias a google-genai>=1.51.0 y refactorización de gemini_service.py para soportar el modelo gemini-3-flash. Implementación de thinking_level y gestión de persistencia de Thought Signatures para evitar errores en sesiones multi-turno. Auditoría de prompts de contenido.


# 2026-01-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## EPI # --SYSTEM -->
*  **Session:** Auditoría de Asignaturas Genéricas y Revisión de Estado Git
*  **Description:** Auditoría de la base de datos para identificar y cuantificar asignaturas genéricas (Prácticas, TFG, etc.) importadas erróneamente antes de su eliminación. Revisión del estado del repositorio para alinear fases de scraping.

*  **Action:** Purga de asignaturas genéricas (TFG, Prácticas, Eventos).
*  **Audit:** Auditoría de asignaturas tipo 'Proyecto'.
# 2026-01-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
## PLUTO # --SYSTEM -->
*  **Session:** Organización Infraestructura Scraping y Fase 2
*  **Description:** Reestructuración del directorio /web_scrapping/ segregando scripts por zonas (East/West). Análisis y desarrollo de estrategias de extracción para Universidades de Sevilla, Huelva y Cádiz.


# 14/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Especialización de Autoevaluaciones por Meta-Categorías (Idiomas, Ciencias, Humanidades)
*  **Description:** Inicio de la fase de especialización del motor de autoevaluaciones. Se planifica la implementación de un clasificador de asignaturas para distinguir entre Idiomas, Ciencias Exactas y Humanidades, permitiendo la generación de exámenes con prompts adaptados (problemas matemáticos, redacción de idiomas, análisis humanístico). Se auditarán los modelos y servicios de Gemini para integrar el tipo de asignatura.


# 2026-01-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Implementación de Clasificación Lógica de Asignaturas para Evaluaciones Especializadas
*  **Description:** Inicio de la fase de especialización del motor de evaluaciones. Se desarrollará un clasificador de asignaturas (Lenguas, Ciencias Exactas, Humanidades) para adaptar los prompts de generación de exámenes. Auditoría de modelos actuales y preparación de servicios de IA.


# 14/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA # --SYSTEM -->
*  **Session:** Corrección Crítica de Prompts de Evaluación y Blindaje Frontend Multimedia
*  **Description:** Sesión dedicada a la rectificación urgente del sistema de autoevaluaciones (Assessment). Se refactorizará core/services/prompt_generators.py para imponer el castellano en la interfaz, parametrizar el idioma de la asignatura y corregir la inyección de etiquetas de control ([---TRANSCRIPT---], [---TAGS---]) para evitar conflictos con Markdown. En el frontend (take_assessment.html), se implementará ocultación CSS forzosa para los textos de Listening y se inyectarán atributos de idioma para el TTS. Finalmente, se validará el flujo de subida de audio al backend.


# 2026-01-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Reconstrucción de Autoevaluaciones: Super-Arquetipos y Blindaje DB
*  **Description:** Implementación de lógica de saneamiento en `orchestrator` para prevenir desbordamiento de columnas (Error 1406). Integración de estándares pedagógicos (CertACLES, EUR-ACE, MECES) en `prompt_generators.py` para generación de exámenes contextualizados por disciplina. Validación de flujo server-side en `assessment`.


# 2026-01-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Re-arquitectura de Assessment para el Motor UGR y Pipeline de IA
*  **Description:** Inicio de la Fase 1 del Hito 6. La sesión se centra en la re-arquitectura del modelo 'Assessment' en la aplicación homónima para CampuStudiOnline. Se sustituirá la segmentación fija por un JSONField 'selection_range' que permita la selección dinámica de temas basada en el 'master_schema' de 'contents'. Asimismo, se integrarán campos para persistir los estímulos generados por la IA (reading_stimulus, listening_transcript), sentando las bases para el pipeline de generación de tres pasos diseñado para emular evaluaciones de nivel universitario.


# 2026-01-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** Fase 1 Autoevaluaciones UGR: Modelo y Selección de Temas
*  **Description:** Inicio de la reconstrucción del sistema de autoevaluaciones (V4) bajo el estándar UGR.
Objetivos de la sesión:
1. Modificación del modelo `Assessment`: eliminación de `target_segment` y adición de `selection_range` (JSONField) para selección granular de temas.
2. Adición de campos de persistencia de estímulos: `reading_stimulus` y `listening_transcript`.
3. Preparación de la lógica para el parseo del `master_schema` en la vista de configuración.


# 2026-01-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO # --SYSTEM -->
*  **Session:** Reparación de Emergencia en Generadores de Prompts y Validación del Pipeline
*  **Description:** Restauración de funciones críticas desaparecidas en `core/services/prompt_generators.py` para resolver el `ImportError` que bloquea WSGI. Validación del flujo de generación de evaluaciones, asegurando la persistencia de `reading_stimulus` y optimizando la carga en frontend. Verificación de rotación atómica de claves API.


# 2026-01-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Reparación de Emergencia en Generadores de Prompts y Desbloqueo WSGI
*  **Description:** Sesión crítica para resolver un ImportError en tasks.py causado por funciones faltantes en prompt_generators.py. Se procederá a la restauración mandatoria de las funciones generate_stimulus_creation_prompt y generate_ugr_questions_prompt para desbloquear el servidor WSGI. Posteriormente se validará el pipeline de generación de evaluaciones y la persistencia de estímulos de lectura.

# 2026-01-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** Validación Empírica de Arquetipos de Evaluación AI y Blindaje LaTeX
*  **Description:** Verificación funcional de la clasificación semántica de asignaturas (Ciencias, Idiomas, Humanidades) y la eficacia del escudo LaTeX en la generación de JSON. Ejecución de pruebas unitarias para confirmar la integridad estructural de los exámenes generados y la correcta renderización de fórmulas matemáticas. Auditoría de tiempos de respuesta del clasificador.


# 2026-01-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** Implementación de Tribunales de Humanidades y Refactorización de Enrutador
*  **Description:** Refactorización de la lógica en `assessment/tasks.py` para establecer la bifurcación directa en Humanidades y Ciencias Exactas, utilizando el contenido filtrado como fuente única. Implementación de los cinco arquetipos de tribunales especializados en `prompt_generators.py` (Jurídicas, Artes, Pensamiento, Historia, Filología) asegurando la estructura de tres bloques (Test, Práctico, Ensayo). Validación de prompts de idiomas.


# 2026-01-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Fix: Classifier Rules - Philology vs Languages (Andalucía Context)
*  **Description:** Implementación de reglas de negocio estrictas en 'classifier.py' para contexto geográfico andaluz. Reclasificación forzosa de asignaturas de 'Español/Lengua/Literatura' como HUMANITIES/PHILOLOGY para evitar la activación errónea de interfaces de idiomas extranjeros en asignaturas de filología hispánica.


# 2026-01-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** Ajuste de Reglas de Clasificación en Autoevaluaciones (Hito 6)
*  **Description:** Refinamiento del clasificador de asignaturas (`classifier.py`) para distinguir correctamente entre Filología Hispánica (Humanidades) e Idiomas Extranjeros, implementando reglas de exclusión geográfica y lingüística específicas. Verificación de la UI resultante.


# 2026-01-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Hito 6: Reparación Crítica de Generadores y Verificación de Estrategia de Idiomas
*  **Description:** Reparación de urgencia del SyntaxError en 'prompt_generators.py'. Verificación del flujo 'Split-Call' en evaluaciones de idiomas y validación de la limpieza de archivos adjuntos efímeros.


# 2026-01-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA # --SYSTEM -->
*  **Session:** Recuperación de Orchestrator e Implementación de Evaluación Multimodal
*  **Description:** Restauración crítica del archivo `orchestrator/tasks.py` desde backup para solucionar error de sintaxis en WSGI. Re-implementación quirúrgica de la generación de audio nativo, inyección de terminología UGR y corrección multimodal, asegurando la integridad sintáctica del código.


# 2026-01-18
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO # --SYSTEM -->
*  **Session:** Reparación Imports Orchestrator y Lógica Examen Idiomas (Listening/Speaking)
*  **Description:** Resolución del ImportError crítico en orchestrator/tasks.py verificando la segregación de lógica de prompts en las estrategias de evaluación (Languages, Sciences, Humanities). Implementación de la lógica específica para exámenes de idiomas: módulo Listening (reproducción de audio y respuesta multimodal) y módulo Speaking (grabación temporizada automática). Investigación e implementación de estándares de acreditación (referencia UGR) para la estructura de preguntas.


# 2026-01-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA # --SYSTEM -->
*  **Session:** Implementación del Arquetipo de Evaluación LOGIC_AND_TECH
*  **Description:** Implementación de la estrategia LOGIC_AND_TECH en el sistema de evaluación (sciences_strategy.py). Enfoque en la generación de problemas técnicos que requieran resolución mediante fórmulas LaTeX y bloques de código o pseudocódigo, validando estrictamente la prohibición de preguntas puramente teóricas. Adaptación de prompts para asignaturas de Ingeniería, Criptografía y Programación.


# 2026-01-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Implementación Estrategia SOCIO_LEGAL
*  **Description:** Implementación del arquetipo de evaluación SOCIO_LEGAL en humanities_strategy.py. Desarrollo de la estructura de examen tipo 'Tribunal Legal' (Conceptos, Casos Prácticos, Ensayos) e integración de validación normativa en los prompts.


# 2026-01-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Implementación Estrategia Evaluación Salud (HEALTH_SCIENCES)
*  **Description:** Desarrollo del módulo `health_strategy.py` siguiendo el Arquetipo 4 del Plan Maestro. Investigación previa de modelos de examen UGR en Ciencias de la Salud. Implementación de lógica para generación de casos clínicos y protocolos. Integración en el sistema de estrategias segregadas.


# 2026-01-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Implementación de Persistencia CEFR y Finalización de Estrategia de Humanidades
*  **Description:** Implementación de la captura dinámica del nivel CEFR en el orquestador para evitar hardcoding. Refinamiento final de la estrategia de Humanidades (Arquetipo 5) y validación de pruebas cruzadas según Plan Maestro.


# 2026-01-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** Optimización UX Evaluación: Markdown, LaTeX y Controles Audio
*  **Description:** Mejora integral de la experiencia de usuario en el módulo de evaluaciones (assessment). Corrección del renderizado de Markdown en preguntas y barra lateral. Implementación de soporte para fórmulas matemáticas (LaTeX/MathJax). Mejora de controles de audio (reproducir, pausar, detener) en ejercicios de idiomas. Depuración de lógica de generación para evitar preguntas duplicadas en secciones.


# 23/01/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Re-arquitectura de Esqueletos de Autoevaluación y Sincronización de Rotación de ApiKeys
*  **Description:** Inicio de la fase de re-arquitectura técnica del sistema de evaluaciones (Hito 6). La sesión se centra en la segregación de la lógica de creación de esqueletos, extrayéndola de tasks.py hacia las estrategias individuales (Fase A: Flujo Atómico). Simultáneamente, se realizará una auditoría mediante PAIR para sincronizar el sistema de rotación y cuarentena de ApiKeys con el motor de generación de contenidos, garantizando robustez ante errores 429. Finalmente, se preparará la validación del renderizado LaTeX para el arquetipo LOGIC_AND_TECH.


# 2026-01-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA # --SYSTEM -->
*  **Session:** Validación Empírica Sistema Evaluaciones y Estabilización Arquitectónica
*  **Description:** Sesión centrada en la validación "Atomic Flow" del sistema de evaluaciones. Se verificará la correcta clasificación de asignaturas (Minor de Chino) bajo el arquetipo CEFR_LANGUAGES, asegurando la generación del esqueleto de 4 bloques (Reading, Listening, Writing, Speaking). Se auditará el renderizado LaTeX en arquetipos científicos y la funcionalidad de los widgets de subida de archivos. Objetivo final: consolidar la arquitectura de evaluaciones antes del despliegue masivo.


# 2026-01-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Validación Empírica del Arquetipo Minor (Chino) y Auditoría LaTeX
*  **Description:** Verificación del flujo de clasificación del Rector para asignar CEFR_LANGUAGES a asignaturas de idiomas (Chino). Validación de UX para widgets de lectura y subida de archivos en la fase de evaluación. Auditoría de renderizado LaTeX en arquetipo LOGIC_AND_TECH.


# 2026-01-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** Validación Empírica de Clasificación y Estrategias de Evaluación UGR
*  **Description:** Ejecución de pruebas para verificar la correcta asignación de arquetipos (específicamente CEFR_LANGUAGES para Chino) por el Rector. Validación de la generación de esqueletos (Fase A) y renderizado UX para asignaturas Minor. Auditoría de soporte LaTeX en arquetipos de ciencias.


# 2026-01-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** EPI - Evolución UX de Evaluación: Dualidad de Entrada y Estímulo Persistente
*  **Description:** Implementación de INPUT_DUALITY para permitir envío simultáneo de texto y archivo en preguntas abiertas. Despliegue del mecanismo STIMULUS_STICKY para acceso persistente a materiales de referencia (Reading/Listening) mediante modal. Refinamiento de la Fase B para forzar audio MP3 y validación del esqueleto del arquetipo Chino B1.


# 2026-01-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO # --SYSTEM -->
*  **Session:** Refinamiento UI/UX: Iconografía de Audio y Carga
*  **Description:** Sustitución de etiquetas de texto por iconografía FontAwesome en reproductor/grabador, rediseño visual del input de archivo, eliminación de campos redundantes en bloques duales y homogeneización de botones flotantes.


# 2026-01-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC # --SYSTEM -->
*  **Session:** Estabilización del Subsistema Multimedia de Evaluaciones y Reparación de UI de Audio
*  **Description:** Sesión centrada en la estabilización de la Fase 2 del Hito 6. Se abordará la reparación definitiva de la inestabilidad en el reproductor TTS y la grabadora de audio, solucionando las paradas aleatorias y colisiones de eventos en dispositivos móviles. Se corregirá la inyección de CSS para la visualización de las ondas de sonido (feedback visual) y se refactorizará assessment_media_utils.js para eliminar deuda técnica. Objetivo: UX robusta en evaluación de idiomas.


# 2026-01-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Evaluación Multimodal: Auditoría de Corrección, Optimización de Feedback IA y Mantenimiento de Audio
*  **Description:** Sesión centrada en la validación del motor de corrección de la Fase B, asegurando el procesamiento correcto de archivos MP3 y archivos adjuntos (imágenes/PDF) tras la implementación de la dualidad de input. Se ajustarán los prompts del sistema para ofrecer feedback pedagógico específico según el widget utilizado (especialmente para corrección de caligrafía y escritura manual). Además, se verificarán las rutinas de limpieza de archivos temporales de audio para prevenir la saturación del servidor.


# 2026-01-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA # --SYSTEM -->
*  **Session:** Refactorización de Plantilla de Idiomas y Widgets Multimedia (UGR Standard)
*  **Description:** Implementación de la nueva lógica de renderizado en `take_assessment_languages.html` basada en la matriz S-Q-R (Source-Interaction-Response). Integración de widgets multimedia (Cassette) y lógica de escritura dual. Desarrollo del parser para Cloze Engine. Carga de documentos maestros del sistema de evaluación.


# 2026-01-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO # --SYSTEM -->
*  **Session:** Implementación de Lógica de Emparejamiento y Ordenación
*  **Description:** Ampliación del modelo de datos con tipos de interacción QT_MATCH y QT_ORDER, implementación de lógica de parsing en tasks.py, desarrollo de widgets específicos y adición de controles de parada en el reproductor de audio según la normativa UGR.


# 2026-01-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA
*  **Session:** Implementación de Strategy Factory y Arquetipos Lingüísticos UGR
*  **Description:** Implementación del patrón Strategy Factory para la gestión polimórfica de evaluaciones. Modificación del modelo Assessment para soportar itinerarios Maior/Minor. Integración de lógica de clasificación automática de idiomas y refactorización de esqueletos de generación según especificación UGR.


# 2026-01-26
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA # --SYSTEM -->
*  **Session:** Reparación de Emergencia - Arquetipo Idiomas y Lógica de Prompts
*  **Description:** Corrección crítica de la estrategia de idiomas: eliminación de meta-preguntas, refuerzo de la inmersión lingüística, limpieza de etiquetas técnicas en UI (Regex en orchestrator) y corrección del formato Cloze. Incluye reingeniería de prompts en languages_strategy.py.


# 2026-01-27
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Reparación de Emergencia: Fix Importación y Saneamiento de Evaluaciones
*  **Description:** Resolución crítica del bloqueo por ImportError en assessment/tasks.py mediante stubs de compatibilidad. Implementación de reglas estrictas de inmersión en languages_strategy.py y saneamiento de regex en el orquestador para eliminar metadatos técnicos. Mejora UX en plantillas Cloze.


# 2026-01-28
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** Estabilización del Emulador UGR: Corrección de Tarpit y Estrategia Universal
*  **Description:** Se abordará la reparación crítica del 'Tarpit' en Celery (assessment/tasks.py) causado por errores de firma, y la implementación definitiva de la estrategia de idiomas (languages_strategy.py) soportando itinerarios MAIOR/MINOR según la nueva Ley Técnica UGR. Se verificará la integridad de la generación de ítems y la sincronización jerárquica en el orquestador.


# 2026-01-28
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Corrección de Claves en Generación de Evaluaciones
*  **Description:** Armonización de claves de diccionario (label/section_label) en orchestrator/tasks.py para evitar KeyError durante la Fase A. Verificación de densidad UGR (17 ítems) y auditoría de inmersión lingüística en estrategias.


# 2026-01-28
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Depuración de Bucle Infinito en Generación de Evaluaciones
*  **Description:** Análisis forense y corrección del fallo crítico en `generate_assessment_from_content_task` que provoca reinicios infinitos tras errores de cuota. Auditoría de persistencia atómica para garantizar la reanudación efectiva del progreso y eliminación de tareas zombie.


# 2026-01-28
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** Diagnóstico de Persistencia Atómica en Assessment
*  **Description:** Investigación del fallo de persistencia en questions_cache durante ejecución Celery. Verificación de update() SQL y plan de contingencia con persistencia física.


# 2026-01-29
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC # --SYSTEM -->
*  **Session:** Validación de Recuperación de Evaluaciones y Monitorización de Logs
*  **Description:** Ejecución de pruebas de validación para el sistema de persistencia "Iron-Clad Plus". Verificación de mecanismos de recuperación por respaldo JSON ante escenarios de interrupción forzada. Monitorización de logs administrativos para estados de "Pool Agotado". Adhesión estricta a la Ley Técnica del Emulador UGR.


# 2026-01-29
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Diagnóstico y Reparación del Sistema de Generación de Evaluaciones
*  **Description:** Investigación de fallos de generación silenciosa (falsos positivos). Implementación de validación de integridad estricta en orchestrator/tasks.py y script de diagnóstico de rotación de claves API.


# 2026-01-30
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Auditoría Evaluación #297, Logs Eventos y Rotación Claves
*  **Description:** Verificación de contenido bilingüe en evaluación #297. Diagnosis de persistencia en event_log de generación atómica. Stress test de rotación de API Keys. Verificación de limpieza de JSONs de recuperación.


# 2026-01-31
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO # --SYSTEM -->
*  **Session:** Hito 06: Validación Lingüística HSK, Stress Test API y Auditoría Widgets
*  **Description:** Validación de la inmersión bilingüe en exámenes MINOR (Chino/Japonés) asegurando la ausencia de inglés. Ejecución de pruebas de estrés sobre la rotación de claves API. Auditoría de renderizado de widgets de ordenación y caligrafía. Verificación de limpieza de archivos de recuperación.


# 2026-02-01
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Validación Multilingüe y Arquetipo LOGIC_AND_TECH
*  **Description:** Ejecución de la validación cruzada para idiomas minoritarios y no latinos, confirmando la abstracción universal del motor. Auditoría de inmersión MAIOR. Inicio del desarrollo del arquetipo LOGIC_AND_TECH con soporte para LaTeX.


# 2026-02-01
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA
*  **Session:** Auditoría Forense y Estabilización del Arquetipo de Idiomas (UGR)
*  **Description:** Auditoría técnica de la evaluación #319 para 'Chino Minor: Intermedio 1', detectando un fallo crítico en la calibración de nivel por ignorar los objetivos académicos de la BBDD. Implementación de aviso de mantenimiento en la Sala de Estudio para proteger la UX. Definición de la estrategia de reparación basada en la inyección de 'learning_objectives' y 'course_content_outline' en el prompt de la IA para alcanzar el techo de calidad exigido por la UGR.


# 2026-02-01
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Alineación de Autoevaluaciones UGR: Del Syllabus Académico a la IA Generativa
*  **Description:** Sexta sesión del Hito 6 enfocada en la re-alineación del sistema de autoevaluaciones. Tras un diagnóstico forense, se determina que la estrategia de idiomas ignora los datos del syllabus ('learning_objectives'). Se establece la hoja de ruta para conectar el 'Selection Range' con el prompt de la IA. Se inicia el blindaje de los protocolos del sistema en el Total Commander para garantizar el cumplimiento estricto del idioma y la operativa de archivos.


# 2024-05-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Refinamiento Pedagógico y Lógica de Evaluación IA (Hito 6)
*  **Description:** Sesión enfocada en el avance del sistema de autoevaluaciones bajo el protocolo 'Atomic Flow'. Se trabajará en la lógica de generación de preguntas para cumplir con los arquetipos pedagógicos definidos (Modelo UGR) y la integración de widgets específicos (MATH_INPUT, AUDIO_RECORDER, etc.) según el área de conocimiento.
# 2026-02-01
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO # --SYSTEM -->
*  **Session:** AUDITORÍA Y REALINEACIÓN UGR PARA IDIOMAS
*  **Description:** Sesión crítica de reingeniería del sistema de evaluación para idiomas. Se procederá primero a la re-alineación documental, diferenciando explícitamente entre el modelo de Acreditación (CertAcles) y el de Grado Académico (UGR). Posteriormente, se auditará el flujo de datos para garantizar que el `course_content_outline` y `learning_objectives` del `Subject` se inyecten correctamente en la estrategia de generación, eliminando el hardcoding de nivel y asegurando una evaluación contextualizada al temario seleccionado.


# 2026-02-03
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Erradicación de Hardcodeo en UI e Inmersión Dinámica en Evaluaciones
*  **Description:** Implementación del método `get_ui_labels` en las estrategias de evaluación para eliminar cadenas estáticas en las plantillas HTML. Configuración de etiquetas dinámicas según el itinerario (Minor/Maior) para garantizar la inmersión lingüística correcta. Auditoría de la persistencia de `prompt_data` para asegurar la coherencia de las etiquetas durante todo el ciclo de vida de la evaluación.


# 2026-02-05
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Auditoría de Documentación UGR y Persistencia de Etiquetas
*  **Description:** Revisión de especificaciones de arquetipos contra realidad UGR. Verificación de persistencia de ui_labels en ciclo de vida de evaluación y unificación de criterios en documentación técnica.


# 2026-02-06
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Hito 6: Consolidación del Motor de Autoevaluaciones y Arquetipos Pedagógicos
*  **Description:** Sesión centrada en el avance del Hito 6. Se abordará la implementación técnica y lógica de los arquetipos de evaluación definidos (Logic, Languages, Health, etc.), asegurando la correcta integración entre el modelo de datos de `assessment`, el orquestador de tareas y la generación de contenido mediante Gemini.


# 2026-02-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** CampuStudiOnline: Fase Nuke - Eliminación y Reconstrucción de Autoevaluaciones (Hito 6)
*  **Description:** Inicio de la Fase Nuke del Hito 6. El objetivo es eliminar sistemáticamente toda la infraestructura previa de 'assessments' (modelos, estrategias, lógica en orchestrator y documentación obsoleta) para limpiar la deuda técnica. Se implementará un bloqueo en frontend (modal 'En Construcción') y se comenzará la documentación estricta de los nuevos arquetipos de acreditación UGR.


# 2026-02-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Fase Nuke: Re-arquitectura del Sistema de Autoevaluaciones UGR
*  **Description:** Inicio de la purga técnica del módulo de evaluaciones obsoleto. El plan de acción comprende la eliminación de estrategias y modelos antiguos, la desvinculación del orquestador y la desactivación del frontend mediante un modal informativo. Se establece la base para una nueva documentación exhaustiva basada en los arquetipos de acreditación de la Universidad de Granada, definiendo una estructura de archivos segregada y una lógica de carga selectiva de componentes pedagógicos.


# 2026-02-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO
*  **Session:** Inicio Implementación Assessment V2 - Creación App y Modelos Base
*  **Description:** Inicio de la Fase 2 del Hito 6. Creación de la aplicación `assessment_v2`. Configuración inicial en `settings.py`. Implementación de la estructura de modelos segregada: `plans.py` (Suscripciones), `tracking.py` (Costes API) y `main.py` (Exámenes). Generación de migraciones iniciales.


# 2026-02-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC # --SYSTEM -->
*  **Session:** Hito 6: Inicio Implementación Assessment V2
*  **Description:** Arranque de la fase de implementación Alpha del sistema de autoevaluación. Creación de la aplicación assessment_v2, integración en settings y definición de modelos de datos fundamentales (SubscriptionPlan, TokenUsage, Exam, Submission) según especificaciones de la UGR/UCO.


# 2026-02-08
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Hito 06: Implementación del Motor de Evaluación y Servicios de Cuotas
*  **Description:** Sesión centrada en la Fase 2 del Hito 06. Se procederá a la implementación de la lógica de negocio para el sistema de autoevaluación (v2).
Objetivos principales:
1. Implementación del servicio de cuotas (`services/quotas.py`) verificando `UserSubscription` y `TokenUsage`.
2. Desarrollo de la `ExamFactory` y orquestación de creación de exámenes.
3. Definición de la estrategia base y la implementación concreta `LanguagesStrategy`.
Carga de contexto obligatoria: Documentación técnica V06DOC y modelos de `assessment_v2`.


# 2026-02-10
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC # --SYSTEM -->
*  **Session:** Inicio Fase 3 Evaluación IA: Vistas, Orquestación y Frontend
*  **Description:** Implementación de la Fase 3 del Hito 6. Creación de `ExamCreateView` en `assessment_v2` integrando la validación de cuotas mediante `QuotaService`. Definición de tareas asíncronas en Celery (`orchestrator/tasks.py`) para la generación de estructuras de examen. Refinamiento de la estrategia de idiomas (`LanguagesStrategy`) y preparación de templates base para el flujo de estado del examen.


# 2026-02-12
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC # --SYSTEM -->
*  **Session:** Hito 6 Fase 3: Integración Backend-Frontend y Orquestación Asíncrona de Evaluaciones
*  **Description:** Implementación de la lógica de negocio para la creación de exámenes: desarrollo de `ExamCreateView` con integración de `QuotaService` para validación de límites. Configuración de la tarea asíncrona `generate_exam_task` en Celery para la generación de estructuras JSON mediante estrategias de IA. Preparación de endpoints y templates para el ciclo de vida del examen (Generación -> Polling -> Ready).


# 2026-02-13
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Hito 6: Refinamiento UX de Creación de Exámenes y Limpieza de Contenidos
*  **Description:** Finalización de la Fase 3 del Hito 6. Implementación de lógica de filtrado en TOC para excluir metadatos y títulos redundantes. Refinamiento de la UX en selectores de rango (lógica inversa y reinicio) en el formulario de creación. Validación del motor de deducción de arquetipos por Regex.

# 2026-02-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** Hito 6: Reparación Admin, Engine Structure y Dashboard
*  **Description:** Se abordará la corrección del glitch visual en el admin, la implementación del método `generate_structure` en `BaseExamStrategy`, la integración de badges en el sidebar de contenidos y la creación del listado de exámenes en `assessment_v2`.


# 2026-02-14
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC # --SYSTEM -->
*  **Session:** Reparación Admin y Consolidación Engine Hito 6
*  **Description:** Corrección visual en admin/base_site.html. Implementación de generate_structure en BaseExamStrategy. Refactorización de tarea Celery para uso de Factory. Integración de badges en Sidebar y creación de Dashboard.


# 2026-02-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** Estandarización de Protocolos de IA para Evaluación
*  **Description:** Definición y refinamiento de la lógica de negocio para el sistema de autoevaluación (Hito 6), integrando los modelos de assessment_v2 con el orquestador y alineando los flujos de trabajo con la documentación satélite del hito.


# 2026-02-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Estandarización de Plantillas JSON y Lógica de Generación V2
*  **Description:** Consolidación de la arquitectura de evaluación V2 siguiendo el contrato 'UGR-Level'. Se inicia la integración de las estrategias de deducción (Logic Mapping) y la estructura de subdivisiones (Templates) para la generación de exámenes mediante IA. El objetivo es asegurar el cumplimiento de la matriz de intersección pedagógica definida en la constelación v06DOC, mapeando Arquetipos, Itinerarios y Niveles directamente desde la estructura académica para alimentar el motor de Gemini.

# 2026-02-15
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO # --SYSTEM -->
*  **Session:** Hito 06 F3: Cierre de Ciclo de Evaluación (Frontend JS, Reportes y Tracking)
*  **Description:** Implementación de la lógica final del ciclo de examen. Desarrollo del script JavaScript en 'exam_take.html' para la recolección de datos de widgets y envío POST. Creación de 'ExamReportView' y la plantilla 'exam_report.html' para la visualización de resultados y feedback. Integración de metadatos de consumo de tokens en 'gemini_service.py' vinculados a 'TrackingService'.


# 15/02/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Refactor de AcademicDeductor e Implementación de Calificación IA UniversIA
*  **Description:** Inicio de la fase final del Hito 6 centrado en la rectificación lógica del motor de deducción académica y la habilitación de la calificación por IA para bloques de producción (DRA-HOLO). Se contempla la inyección de lógica Kill-Switch para itinerarios de seguridad (ECOE) y el cierre del ciclo de UI con plantillas de examen y feedback detallado.


# 2026-02-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC # --SYSTEM -->
*  **Session:** Restauración del Dashboard del Orquestador y Validación Final de Assessment V2
*  **Description:** Fase 4 del Hito 6. Diagnóstico y reparación de la regresión en la visualización de logs del Dashboard. Validación funcional (Smoke Tests) de widgets críticos (Cálculo y Kill-Switch).

# 2026-02-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA # --SYSTEM -->
*  **Session:** Hito 06: Estabilización de Enrutamiento y Smoke Tests de Arquetipos
*  **Description:** Ejecución de la Fase 4 del Hito 6. Limpieza radical de conflictos de namespace en `core/urls.py` y `assessment_v2`. Verificación de inyección HTMX en el Dashboard. Validación de generadores de exámenes para arquetipos TECH y HEALTH.


# 2026-02-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO # --SYSTEM -->
*  **Session:** Validación Atómica de Motores TECH y HEALTH
*  **Description:** Ejecución de Smoke Tests para los arquetipos TECH (Bloque RPP-TRAZA) y HEALTH (Bloque CDS-KILL). Verificación de asignación de widgets W-TECH-CALC y lógica de Kill Switch. Auditoría de integración HTMX en Dashboard.


# 2026-02-16
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA # --SYSTEM -->
*  **Session:** Validación de Motores de Evaluación: Arquetipos TECH y HEALTH (RPP-TRAZA & CDS-KILL)
*  **Description:** Ejecución de Smoke Tests para los bloques de evaluación RPP-TRAZA (Ingeniería) y CDS-KILL (Salud). Verificación de la asignación de widgets específicos (W-TECH-CALC), lógica de calificación con peso en planteamiento (50%) y mecanismos de seguridad crítica (Kill Switch/Fatal Error). Auditoría de integración HTMX y logs en Dashboard V2.


# 2026-02-17
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA # --SYSTEM -->
*  **Session:** H06: Auditoría del Motor y Refinamiento de Feedback
*  **Description:** Sesión de auditoría técnica profunda sobre la arquitectura assessment_v2 para validar la alineación con la documentación V06. Implementación de la taxonomía de feedback y personalización de informes por rol.


# 18/02/2026
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Hito 6 Fase 6: Implementación del Bucle de Orquestación Segmentada
*  **Description:** Refactorización de orchestrator/tasks.py para implementar la generación iterativa de ítems bajo la arquitectura Skeleton-First. Integración con el método get_section_plan de las estrategias y gestión de memoria de contexto para evitar duplicidad en la generación de autoevaluaciones.


# 2026-02-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI # --SYSTEM -->
*  **Session:** Rectificación y Alineación Absoluta de Estrategias de Evaluación (V06)
*  **Description:** Implementación estricta de la arquitectura segregada definida en la documentación V06. Reescritura de las estrategias (Tech, Health, Social, Humanities) para garantizar la generación atómica de ítems, el cumplimiento de la Regla de Oro del Idioma (Castellano en UI) y la eliminación de metadatos técnicos en la salida. Limpieza de widgets hardcodeados en plantillas.

# 2026-02-19
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO
*  **Session:** Implementación Skeleton-First en Evaluación IA
*  **Description:** Sesión dedicada a la rectificación estructural del Hito 6. Se procederá a refactorizar el orquestador (orchestrator/tasks.py) para implementar el bucle iterativo atómico por sección (Skeleton-First), inyectando metadatos pedagógicos. Se adaptará la UI (exam_take.html) para carga dinámica de widgets y se implementará un protocolo de resiliencia (reintentos) en la clasificación IA para garantizar la estabilidad del sistema.


# 2026-02-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Sistema de Autoevaluaciones con IA
*  **Description:** Sesión orientada al desarrollo e integración del sistema de autoevaluaciones impulsado por IA. Se abordarán las tareas definidas en la constelación de documentos del Hito 6 para fortalecer el motor de evaluación (assessment_v2), validación de esquemas y la lógica transversal del proyecto.


# 2026-02-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Rectificación Estructural: Motor Evaluador IA
*  **Description:** Sesión crítica para subsanar la desalineación estructural (Skeleton-First) del motor de autoevaluaciones. Se refactorizará el orquestador (orchestrator/tasks.py) para generación iterativa atómica, se adaptará la UI (exam_take.html) a la carga dinámica de widgets y se implementará el protocolo de resiliencia ante fallos de la API.


# 2026-02-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06
## MAMC # --SYSTEM -->
*  **Session:** Hito 06: Refactorización Skeleton-First y Orquestación Atómica
*  **Description:** Implementación del patrón Skeleton-First en orchestrator/tasks.py. Modificación del bucle de generación para crear estructura (ExamSection) previa a la inyección atómica de ítems vía IA. Implementación de lógica de reintentos en logic.py y preparación de carga dinámica de widgets en exam_take.html. Objetivo: Desbloqueo del Hito 6 según Manifiesto V1.4.


# 2026-02-20
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC
*  **Session:** Implementación del Patrón Skeleton-First en el Orquestador de Exámenes
*  **Description:** Refactorización del orquestador (tasks.py) para separar la creación estructural (ExamSection) del llenado de contenido (ExamItem) mediante bucles iterativos y llamadas atómicas a la IA. Implementación de inyección de metadatos pedagógicos y sistema de reintentos para clasificación.


# 2026-02-21
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA
*  **Session:** Rectificación Estructural del Orquestador y UI de Evaluaciones (Hito 06)
*  **Description:** Inicio de la fase de rectificación crítica para alinear el código con la arquitectura Skeleton-First definida en la constelación V06. La sesión se centra en la refactorización del bucle de generación en 'orchestrator/tasks.py' para transmutarlo de un modelo monolítico a uno atómico por secciones, la implementación del sistema de reintentos en la clasificación de asignaturas y la dinamización de la interfaz de exámenes 'exam_take.html' mediante la carga de widgets bajo demanda según el contrato JSON. Se busca erradicar la desalineación sistémica y asegurar la inmersión lingüística normativa.

# 2026-02-21
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Refactorización Atómica del Hito 6: Skeleton-First y UI Dinámica
*  **Description:** En esta sesión se ha procedido a desbloquear el desarrollo del Hito 6 mediante una reestructuración profunda del sistema de autoevaluaciones. Se ha refactorizado el orquestador de tareas Celery para implementar un bucle iterativo de generación por secciones (Skeleton-First), garantizando la integridad relacional de la base de datos antes de las llamadas a la IA. Paralelamente, se ha rediseñado la interfaz de toma de exámenes para eliminar la lógica estática, implementando un renderizado dinámico de widgets compatible con los esquemas JSON de Gemini y superando la auditoría de calidad con djlint. Finalmente, se ha actualizado la documentación satélite y el roadmap para certificar el levantamiento del bloqueo técnico.

# 2026-02-21
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA # --SYSTEM -->
*  **Session:** Test Integración Académica Lenguas B2 y Persistencia Widgets
*  **Description:** Validación del modo de inmersión total mediante generación de examen de Lenguas B2. Verificación de persistencia de respuestas en widgets complejos y auditoría de creación de secciones Skeleton-First en BD.


# 2026-02-21
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## AAAA <!-- SYSTEM -->
*  **Session:** AUDITORIA_ARQUETIPOS_Y_TEST_ATOMIC_LOOP
*  **Description:** Auditoría de correspondencia entre estrategias Health y Technical con V06DOC_SUBARCHETYPES. Ejecución de test real de generación atómica en Celery verificando la vinculación de ítems a secciones. Pruebas del Rigor Engine inyectando respuestas para validar la evaluación y el resumen 'Voz del Catedrático'.

# 2026-02-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CYC
*  **Session:** Implementación de Sistema Anti-Abuso (Caducidad 24h)
*  **Description:** Implementación de la regla de caducidad de 24 horas para exámenes generados. Adición del campo expiration_date en el modelo Exam, lógica de cálculo tras estado READY en Celery, y ajuste en navigation_builder.py para filtrar evaluaciones caducadas.

# 2026-02-22
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EPI
*  **Session:** Test de Estrés y Validación Masiva de Subarquetipos V06
*  **Description:** Implementación y ejecución de un script de auditoría en entorno transaccional aislado (rollback) para someter a prueba de estrés al motor de evaluaciones. Se verificará la correcta deducción de identidad pedagógica (arquetipo y subarquetipo) y la generación atómica de exámenes sobre un muestreo representativo de 22 asignaturas reales, asegurando la robustez del sistema sin afectar la base de datos de producción.

# 2026-02-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO !<-- SE PONE EL ACRÓNIMO QUE ENTREGA EL USUARIO, JAMÁS SE PONE UNO INVENTADO POR EL MODELO # --SYSTEM -->!
*  **Session:** AUDITORÍA DE CUARENTENA Y ROTACIÓN EN MOTORES DE IA
*  **Description:** Análisis de asimetría en resiliencia entre tareas de generación de exámenes y cursos, implementación de cuarentena unificada para API Keys tras errores 429, ajuste de delays en orquestador para mitigación de Throttling RPM, y certificación final de subarquetipos (22/22) bajo ráfaga controlada.

# 2026-02-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## PLUTO
*  **Session:** AUDITORÍA DE CUARENTENA Y ROTACIÓN EN MOTORES DE IA
*  **Description:** Análisis de asimetría en resiliencia entre tareas de generación de exámenes y cursos, implementación de cuarentena unificada para API Keys tras errores 429, ajuste de delays en orquestador para mitigación de Throttling RPM, y certificación final de subarquetipos (22/22) bajo ráfaga controlada.

# 2026-02-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## MAMC
*  **Session:** Validación Final de Motores V06 y Corrección de Nominales
*  **Description:** Sesión enfocada en la validación final de los 22 motores del sistema de autoevaluación V06. Se procederá a corregir los nombres nominales de las asignaturas fallidas (SUB-LIN-LIT, SUB-SAN-CUID, SUB-HUM-HIST) en el comando de validación. Posteriormente, se ejecutará la prueba de carga para certificar el éxito bajo ráfaga controlada, auditar los logs para comprobar la resiliencia y rotación de claves API, y finalizar el Hito 06.


# 2026-02-23
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## EDC
*  **Session:** Depuración de Generación Skeleton-First y Firmas de Estrategias
*  **Description:** Resolución de TypeError en LanguagesStrategy, auditoría del contrato de firmas en estrategias de evaluación, prueba de generación completa desde UI y corrección de advertencias de sanitización HTML con Bleach.
# 2026-02-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## NRA <!-- SYSTEM -->
*  **Session:** Auditoría Integral de Desalineación (Hito 6)
*  **Description:** Diagnóstico de la ruptura entre la especificación documental (V06DOC_*) y la implementación del motor de autoevaluaciones (assessment_v2). Análisis de la inyección de contexto, persistencia atómica de ExamItem, y la falta de renderizado del arquetipo secuencial en la interfaz. Preparación para la reconstrucción del flujo orquestador-IA.

# 2026-02-24
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CSO
*  **Session:** Refactorización de Gemini Service y Validación End-to-End
*  **Description:** Depuración del core de IA añadiendo soporte para el argumento response_schema en core/services/gemini_service.py. Prueba de carga con generación atómica y validación de renderizado del section_stimulus en el panel lateral dinámico del frontend.


# 2026-02-25
# CAMPUSTUDIONLINE --ROADMAP
# CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md
## CAMA
*  **Session:** IMPLEMENTACIÓN DEL MOTOR DE PLANTILLAS DETERMINISTA
*  **Description:** Refactorización del orquestador y estrategias para inyectar contenido en un esqueleto de examen pregenerado por Python. Implementación del renderizado de estímulos en paneles laterales persistentes (layout_mode).

