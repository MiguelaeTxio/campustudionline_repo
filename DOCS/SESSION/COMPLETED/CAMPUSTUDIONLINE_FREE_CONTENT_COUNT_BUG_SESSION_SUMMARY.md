# Sumario de Sesión Temporal: Bug en Conteo de Contenidos Libres

## 1. Contexto del Descubrimiento

Durante la sesión `UI_BUTTON_STATUS_FIX`, se ha detectado una inconsistencia de datos entre la vista pública del directorio de contenidos y el dashboard administrativo.

## 2. Análisis Empírico del Problema

- **Evidencia A (Vista Pública):** La captura de pantalla del "Directorio de Contenidos Libres" para la categoría "Lingüística y Filología" muestra la existencia de múltiples temas (Chino Mandarín, Griego, etc.), confirmando que hay `ContentMaterial` catalogados como libres.
- **Evidencia B (Dashboard Admin):** La captura de pantalla del "Centro de Control de Contenidos" muestra la métrica "Contenidos Libres" con un valor de **cero (0)**.

- **Discrepancia:** El panel de administración no está contando correctamente los materiales de contenido libre existentes en la base de datos.

## 3. Hipótesis Principal

La causa más probable del error es una consulta incorrecta en la vista `task_dashboard_view` (ubicada en `content_automation/views.py`). La lógica actual para determinar qué es un "contenido libre" (probablemente `subject__isnull=True`) no se corresponde con la forma en que estos contenidos están realmente estructurados o clasificados en la base de datos.

## 4. Hoja de Ruta para la Sesión de Corrección

La sesión de depuración se iniciará con el comando: **`PISA CAMPUSTUDIONLINE --TEMP FREE_CONTENT_COUNT_BUG`**.

El plan de acción será el siguiente:

1.  **PASO 1: Aislamiento del Código Problemático:**
    *   **Acción:** Solicitar y analizar el archivo `content_automation/views.py`.
    *   **Objetivo:** Localizar la línea exacta donde se calcula la variable `free_content_count` para la plantilla del dashboard.

2.  **PASO 2: Verificación Empírica en la Base de Datos:**
    *   **Acción:** Crear y ejecutar un script en la `shell` de Django.
    *   **Objetivo 1:** Ejecutar la misma consulta del `views.py` para confirmar que devuelve 0.
    *   **Objetivo 2:** Investigar el modelo `ContentMaterial` para encontrar el criterio de filtrado correcto que identifique inequívocamente el contenido libre (ej. por `Topic`, por `is_public` y `subject__isnull`).
    *   **Objetivo 3:** Formular una nueva consulta que devuelva el número correcto de contenidos libres.

3.  **PASO 3: Implementación de la Corrección:**
    *   **Acción:** Ejecutar un protocolo `PMA` sobre `content_automation/views.py`.
    *   **Objetivo:** Reemplazar la consulta defectuosa por la nueva consulta validada empíricamente en el paso anterior.

4.  **PASO 4: Verificación Funcional:**
    *   **Acción:** Recargar el servidor y la página del "Centro de Control de Contenidos".
    *   **Objetivo:** Confirmar visualmente que la métrica "Contenidos Libres" muestra ahora el valor correcto, coincidiendo con la realidad de los datos.
