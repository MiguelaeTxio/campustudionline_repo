# Plan de Estabilización y Reseteo de Contenido

## 1. Diagnóstico del Incidente

La solución al bloqueo del motor de automatización requirió un cambio estructural en el modelo `ContentMaterial` (de `ForeignKey` a `ManyToManyField`). El proceso de migración de la base de datos falló, resultando en una pérdida de los datos de relación y la desincronización del código de la aplicación.

## 2. Decisión Estratégica

Tras el fallo de la migración y la corrupción de datos resultante, se ha tomado la decisión estratégica de **NO RESTAURAR DESDE UNA COPIA DE SEGURIDAD**.

En su lugar, se procederá con un **RESETEO COMPLETO Y PURGA TOTAL de todo el contenido de la plataforma** para validar la nueva arquitectura sobre una base de datos limpia y controlada.

## 3. Hoja de Ruta para la Próxima Sesión (Estabilización)

La prioridad máxima es ejecutar la purga y validar la funcionalidad de la nueva arquitectura end-to-end.

1.  **PURGA TOTAL DE CONTENIDOS (NO NEGOCIABLE):** El primer paso **obligatorio** será ejecutar un script en la `shell` para eliminar todos los objetos de los siguientes modelos:
    *   `ContentMaterial` (y por tanto, `ContentCopy` y `Annotation` en cascada)
    *   `PendingContentTask`
    *   `ContentRequest`
    *   `FreeContentRequest`

2.  **RESETEO DE INDICADORES ACADÉMICOS:** Se ejecutará un script para actualizar a `False` todos los flags `has_public_content` en los modelos `Subject`, `Degree`, `Branch` y `University`.

3.  **AUDITORÍA Y CORRECCIÓN FINAL DEL CÓDIGO:**
    *   Verificar que las correcciones en `contents/admin.py` y `content_automation/views.py` están aplicadas.
    *   **Eliminar la señal obsoleta `sync_duplicate_subjects_on_content_creation`** del archivo `contents/signals.py`, que es la causa del último error `ManyRelatedManager`.

4.  **VERIFICACIÓN DE ESTRUCTURA:** Confirmar que la estructura de la base de datos es la correcta (`ManyToManyField`) y que la aplicación web carga sin errores tras las correcciones.

5.  **PRUEBA DE GENERACIÓN (END-TO-END):**
    *   Iniciar el motor de automatización.
    *   Verificar que se crea **una** tarea para una asignatura con duplicados (ej. "Álgebra").
    *   Confirmar que, tras la generación exitosa, el `ContentMaterial` resultante se vincula correctamente a **todas** las `Subject` llamadas "Álgebra".
    *   Verificar que el motor continúa su ciclo sin detenerse.

