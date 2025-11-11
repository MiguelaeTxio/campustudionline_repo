# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 11/11/2025 (CYC)

**Objetivo Inicial:** Corregir el temporizador de cuenta regresiva de las autoevaluaciones.

**Desarrollo y Descubrimientos Clave:**
La sesión se centró en una exhaustiva investigación empírica para localizar la causa raíz del fallo del temporizador. A pesar de múltiples verificaciones y correcciones en la cadena lógica (backend, base de datos, JavaScript y plantillas), el problema persistió, revelando una contradicción empírica:

1.  **Verificación del Backend:** Se confirmó que la lógica en `assessment/tasks.py` y `assessment/utils.py` era correcta, y que la fecha de expiración se guardaba correctamente en la base de datos y se enviaba al contexto de la plantilla.
2.  **Verificación del Frontend:** Se corrigió el JavaScript (`assessment_status_handler.js`) para asegurar que leía el atributo `data-` correcto.
3.  **Investigación de Integración:** La inspección del HTML renderizado (`view-source`) demostró que la plantilla recibía los datos correctos del backend, pero también reveló que el script `assessment_status_handler.js` se estaba cargando dos veces.
4.  **Causa Raíz Postulada:** Se determinó que una modificación previa había introducido erróneamente una carga global del script en `base.html`, causando la duplicación.
5.  **Contradicción Final:** A pesar de las correcciones aplicadas y de las búsquedas exhaustivas (`grep`) en todo el proyecto, que confirmaron que la carga del script no estaba presente de forma estática en las plantillas, la evidencia empírica final (`view-source`) seguía mostrando la carga del script.

**Estado Final:** El problema del temporizador **sigue sin resolverse**. La investigación concluyó en una contradicción irresoluble: el script se carga, pero no se encuentra ninguna referencia a su carga en el código fuente del proyecto. La causa debe ser un mecanismo de inyección dinámica que no ha podido ser localizado durante esta sesión.

## Hoja de Ruta para la Próxima Sesión

1.  **Fase 1: Diagnóstico de Inyección Dinámica.**
    *   **Objetivo:** Localizar el mecanismo exacto que está inyectando la etiqueta `<script>` para `assessment_status_handler.js` en el HTML final.
    *   **Plan:**
        *   Realizar búsquedas `grep` no literales (ej. por partes como "handler", ".js", etc.) en los archivos Python del proyecto, especialmente en `views`, `context_processors` y `templatetags`, para encontrar código que genere etiquetas de script dinámicamente.
        *   Insertar "sondas" (comentarios HTML únicos) en puntos clave de la jerarquía de plantillas (`base.html`, plantillas incluidas) para determinar en qué bloque exacto se está produciendo la inyección al inspeccionar el `view-source`.

