# Resumen de Sesión Temporal: Duplicación de Contenido en Creación de Tareas Libres (SOLUCIONADO)

---

## 1. Incidencia Detectada

Se identificó un comportamiento anómalo crítico en el módulo de automatización de contenido. Al crear manualmente una única tarea para la generación de contenido libre (ej. "Pink Floyd"), el sistema generaba múltiples instancias del `ContentMaterial` resultante.

---

## 2. Análisis y Resolución Empírica

- **Hipótesis Inicial (Incorrecta):** Se postuló que el error residía en el flujo de aprobación de `FreeContentRequest`.
- **Aclaración Empírica Clave:** El usuario (Miguel Ángel) especificó que el bug se manifestaba durante la **creación manual de una tarea libre desde cero**, invalidando la hipótesis inicial.
- **Análisis de Causa Raíz (Correcto):** La investigación sobre `content_automation/views.py` confirmó que la vista `create_free_task_view` carecía de un mecanismo de idempotencia. Múltiples peticiones POST, generadas por dobles clics en el botón de guardar, resultaban en la creación de múltiples objetos `PendingContentTask` para la misma solicitud.
- **Solución Implementada:** Se aplicó una solución de dos capas para erradicar el bug:
    1.  **Nivel de Base de Datos (`models.py`):** Se añadió una restricción `UniqueConstraint` al modelo `PendingContentTask`. Esta restricción impide la existencia de más de una tarea activa para contenido libre que comparta el mismo `course_title`, garantizando la unicidad a nivel de datos.
    2.  **Nivel de Aplicación (`views.py`):** La lógica de la vista `create_free_task_view` se envolvió en un bloque `try...except IntegrityError`. Esto permite capturar el intento de violación de la nueva restricción y mostrar un mensaje de error informativo al usuario, en lugar de provocar un fallo del sistema.

## 3. Resultado de la Sesión

La solución fue implementada, probada y verificada (`VBO.` del usuario). El bug de duplicación de contenido ha sido resuelto de forma definitiva.
