# Resumen de Sesión: Resolución de Crisis de Base de Datos (Quota Exceeded)

**Fecha:** 29/11/2025
**Proyecto:** CAMPUSTUDIONLINE
**Hito:** 24 (Soporte y Mantenimiento)

## Objetivos
1.  Resolver la alerta crítica de PythonAnywhere sobre el exceso de cuota de disco en MySQL (34.5 GB usados vs 3 GB permitidos).
2.  Evitar la recurrencia del problema.

## Acciones Realizadas
1.  **Diagnóstico:**
    *   Se identificó que la tabla `orchestrator_pendingcontenttask` ocupaba 32.6 GB.
    *   La causa raíz fue la acumulación de logs detallados (`task_log`) con payloads JSON masivos y una fragmentación severa ("huecos") en el archivo InnoDB `.ibd`.
    *   Se confirmó que los datos *reales* eran insignificantes (~15 MB).

2.  **Resolución (The Guaranteed Way):**
    *   Se ejecutó un procedimiento drástico y seguro de **Volcado y Recarga** (`table_hard_reset_v3.py`):
        *   Exportación de datos (`mysqldump`).
        *   Borrado de tabla (`DROP`).
        *   Importación de datos (`RELOAD`).
    *   **Resultado:** El tamaño de la tabla bajó de 32.6 GB a **~2.6 MB**. El uso total de la DB bajó a **1.9 GB** (65% de la cuota).

3.  **Prevención:**
    *   Se aplicó un parche en `orchestrator/tasks.py` para truncar automáticamente cualquier payload JSON mayor a 2000 caracteres.

4.  **Mejoras Adicionales:**
    *   Se añadió la plantilla de prompts para la categoría **Botánica** en `DOCS/MAINS/CONTENT_PROMPTS.md`.

## Incidencias Pendientes (Registradas en Hito 24)
1.  **Error 500 en Admin:** Al editar usuarios, error por campos de `UserProfile` inexistentes.
2.  **Error Template:** `TemplateSyntaxError` en `contents/personal_workspace.html`.

## Estado Final
Sistema estable, base de datos optimizada y segura. Incidencias menores registradas para la próxima sesión.
