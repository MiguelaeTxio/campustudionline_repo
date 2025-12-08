# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Estado:** **EN CRISIS / BLOQUEO TÉCNICO**

## Bitácora de Sesión (08/12/2025)
*   **Incidencia:** El sistema de orquestación ignora los tiempos de espera (`countdown`, `eta`) debido a un desfase de zona horaria entre Django y Celery, provocando bucles infinitos de reintentos.
*   **Estado del Código:** El archivo `orchestrator/tasks.py` ha sufrido múltiples parches fallidos. Se desconoce el estado exacto de la lógica de contadores y tiempos.

## Hoja de Ruta (Siguiente Sesión)

### 1. AUDITORÍA FORENSE COMPLETA (MÁXIMA Y ÚNICA PRIORIDAD)
*   **Objetivo:** Determinar la causa raíz de la degradación del código en `orchestrator/tasks.py`.
*   **Metodología:** **Comando S** (Generación de archivo en servidor -> Descarga local -> Carga al asistente).
*   **Paso 1 (Usuario):** Ejecutar el comando `git log -p orchestrator/tasks.py > {SERVER_SWAP}/TASKS_AUDIT_FULL.txt`.
*   **Paso 2 (Usuario):** Descargar y cargarme el archivo `{SERVER_SWAP}/TASKS_AUDIT_FULL.txt`.
*   **Paso 3 (Asistente - YO):** Analizaré el historial de cambios del archivo.
*   **Paso 4 (Asistente - YO):** Presentaré un informe detallado de hallazgos y un plan de acción correctivo.
*   **Restricción:** No se propondrá ni una sola línea de código hasta que el usuario apruebe el plan de acción derivado del análisis de la auditoría.

