# 2025-11-08
# CAMPUSTUDIONLINE --TEMP
# APIKEYS_ROTATION_AND_QUARENTAINE_FAILURE
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
*  **Session:** Diagnóstico y Corrección de la Caducidad Inconsistente de Resultados de Autoevaluación
*  **Description:** Auditar y corregir la lógica de purgado de resultados de autoevaluaciones (`purge_and_penalize_corrections`) para resolver la inconsistencia entre la fecha de expiración mostrada y el mensaje de caducidad prematura, garantizando la coherencia del estado para el usuario.

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
