# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO - REFACTORIZACIÓN DOCUMENTAL COMPLETADA (V3.1)

## LOGROS DE LA SESIÓN ACTUAL (FINALIZADO)
*   Refactorización íntegra de la constelación documental para el subarquetipo **SUB-LIN-MINOR** (Modelo Minor / Iniciación UGR).
*   Inyección de los motores **RBT-GRAPH-VAL** (Validación de Trazos) y **MAT-CULT-LINK** (Asociación Cultural) en V06DOC_BLOCKS.md.
*   Establecimiento del **Mandato de Bloqueo Caligráfico** en V06DOC_WIDGETS.md para lenguas no latinas.
*   Actualización de la secuencia genética obligatoria (SD_GRAPH, SD_GRAM, SD_READ_MIN, SD_CULT) conforme a la Facultad de Filosofía y Letras de la UGR.

## HOJA DE RUTA PARA LA PRÓXIMA SESIÓN (LEY SUPREMA - NO INVENTAR NADA)

**OBJETIVO MANDATORIO:** Sincronización técnica de la arquitectura Django con la nueva base documental Minor.

### FASE 1: ACTUALIZACIÓN DE MODELOS (assessment_v2/models/main.py)
*   **Tarea:** Inyectar en la clase `Subdivision` del modelo `ExamSection` las nuevas constantes:
    *   `SD_GRAPH`: 'Grafía y Fonética'
    *   `SD_GRAM`: 'Estructura Base'
    *   `SD_READ_MIN`: 'Lectura Adaptada'
    *   `SD_CULT`: 'Contexto Sociocultural'
*   **Validación:** Ejecutar `python manage.py makemigrations` y `migrate`.

### FASE 2: VALIDACIÓN EN DJANGO ADMIN
*   **Tarea:** Verificar que los nuevos tipos de subdivisión son seleccionables manualmente en el Admin de `ExamSection`.

### FASE 3: AUDITORÍA DE ESTRATEGIAS (Detección de Impacto)
*   **Tarea:** Analizar la carpeta `assessment_v2/services/engine/strategies/` para identificar dónde se instanciarán estas nuevas subdivisiones en la próxima fase de implementación.

**FUENTES DE REFERENCIA:** Documentación satélite refactorizada en la sesión NRA.
