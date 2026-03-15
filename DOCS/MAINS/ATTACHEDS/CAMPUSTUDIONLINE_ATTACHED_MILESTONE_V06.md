# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN

**Objetivo Principal:** Solucionar la filtración de datos crudos (diccionarios Python) y metadatos sensibles (respuestas correctas) en la vista de realización del examen (`assessment_v2/templates/assessment_v2/exam_take.html`), implementando un renderizado correcto y limpio para el componente de opciones múltiples.

**Directrices de Implementación (Fuente de la Verdad):**
1.  **Auditoría de Renderizado:** La plantilla `exam_take.html` está volcando directamente objetos JSON generados por la IA en lugar de iterar sobre ellos. Esto expone el esquema interno (ej: `{'id': 'A', 'text': '...', 'is_correct': True, 'feedback': '...'}`).
2.  **Iteración de Opciones:** Para el widget `W-OBJ-STRIKE` (Respuesta Múltiple), se debe iterar obligatoriamente sobre el array de opciones (`{% for opcion in item.content.options %}`) renderizando botones de tipo `radio` asociados a su `item.uuid`.
3.  **Ocultación de Metadatos Críticos:** Queda **ESTRICTAMENTE PROHIBIDO** renderizar en el HTML las claves `is_correct` y `feedback` durante la realización del examen. Esta información solo debe estar disponible en la vista de resultados (`exam_report.html`). Su exposición actual permite al alumno ver la respuesta correcta antes de enviar el formulario.
4.  **Consistencia UI:** Asegurar que los radio buttons y las etiquetas se renderizan con las clases de Bootstrap/UniversIA correspondientes para mantener el diseño responsivo.

Esta hoja de ruta guiará el inicio de la próxima sesión de forma ineludible.
