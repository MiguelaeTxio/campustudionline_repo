# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 15/11/2025 (PCS - FALLIDA)

**Objetivo:** Investigar y solucionar una anomalía en la visualización de `ContentCopy` en la "Sala de Estudio", donde una copia creada desde una asignatura específica se mostraba incorrectamente bajo la disciplina de la asignatura prototipo de su `ContentHashFamily`.

**Desarrollo y Depuración Empírica:**
La sesión ha sido un proceso de depuración complejo que ha permitido descartar múltiples hipótesis erróneas hasta aislar la causa raíz definitiva del problema.

1.  **Hipótesis Descartada #1: Error en la Creación.** Se postuló que la lógica de creación de la copia (`create_content_copy`) era defectuosa. **RESULTADO EMPÍRICO:** Falso. Una auditoría de la base de datos (`manage.py shell`) demostró inequívocamente que la `ContentCopy` se crea correctamente, con su campo `subject_context` apuntando a la asignatura correcta ("Grado en Lenguas Modernas y sus Literaturas"). **La integridad de los datos en la BBDD es correcta.**

2.  **Hipótesis Descartada #2: Error en el Flujo de Datos.** Se postuló que las plantillas del Directorio Académico no enviaban el contexto de la asignatura a la vista de detalle, y esta a su vez a la vista de creación. **RESULTADO EMPÍRICO:** Parcialmente cierto pero irrelevante para el error final. Se realizaron modificaciones en `urls.py`, `views.py` y plantillas para asegurar el flujo de `subject_pk`, pero el problema persistió, demostrando que la causa no estaba en el envío de datos, sino en su procesamiento.

3.  **Causa Raíz Identificada:** El fallo reside **exclusivamente** en la lógica de la vista `contents/study_room_views.py`, función `user_copies_list`. Esta vista, responsable de renderizar la "Sala de Estudio", ignora por completo el campo `subject_context` (que es correcto) y, en su lugar, basa su lógica de agrupación en la jerarquía temática del `ContentMaterial` original. Esta es la razón por la que una copia correctamente asociada a "Lenguas Modernas" se visualiza erróneamente bajo "Estudios Franceses".

**Estado Final:** No se ha aplicado ninguna corrección funcional. El problema persiste, pero su causa ha sido aislada sin lugar a dudas. Las propuestas de modificación (`PMA`) fueron denegadas por estar basadas en análisis incorrectos o ser destructivas.

## Hoja de Ruta para la Próxima Sesión

**Objetivo:** Implementar una "vista inteligente" en `user_copies_list` que solucione el error de visualización de forma definitiva, respetando la funcionalidad existente.

**Plan de Acción Atómico:**
1.  **Refactorizar `study_room_urls.py`:** Crear un conjunto de rutas explícitas y separadas para la navegación de copias académicas (ej: `/academic/university/branch/...`).
2.  **Refactorizar `user_copies_list`:** Convertir la vista en un despachador que, según la URL, ejecute una de dos lógicas de consulta distintas:
    *   **Lógica Académica:** Navegará usando la jerarquía estructural (`Universidad -> Rama -> Titulación`) obtenida del `subject_context` de las `ContentCopy`.
    *   **Lógica de Contenido Libre:** Mantendrá la navegación por `Categoría Maestra`, que ya funciona.
3.  **Adaptar la plantilla `copy_list.html`:** Modificar la plantilla para que pueda renderizar la salida de ambas lógicas.
