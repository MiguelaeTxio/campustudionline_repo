# ANEXO: HITO 06 - REFACTORIZACIÓN ASÍNCRONA Y OPTIMIZACIÓN UX (HOJA DE RUTA DEFINITIVA)
# ESTADO: EN PROGRESO

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN

1. **Refactorización de Arquitectura de Evaluación (Desacoplamiento):**
   - Modificar `assessment_v2/views.py` y `admin_views.py`: Eliminar cualquier llamada bloqueante a `AcademicDeductor` o `generate_text_content`.
   - Modificar `ExamFactory`: Permitir inicialización de `Exam` con `archetype_id=NULL` para soportar creación inmediata en BBDD.
   - Implementar modal de aviso asíncrono en el frontend tras la selección de temario.

2. **Optimización del Pipeline de Generación (Asincronía):**
   - Refactorizar `generate_exam_task` en `orchestrator/tasks.py`:
     - El proceso de IA debe iniciarse exclusivamente dentro de la tarea Celery.
     - Implementar "Batch-Atómico": Agrupar subdivisiones con mismo `layout_mode` en una única llamada API.
     - Reducir tamaño del prompt: Pasar solo IDs de ítems en lugar de objetos JSON completos.

3. **Blindaje y Calidad de Contenido:**
   - Refinar prompts: Ajustar parámetros de temperatura (cercana a 0.2) y *top-p* para eliminar tono pedagógico excesivo.
   - Blindaje de Lista Blanca: En `HumanitiesStrategy`, forzar la exclusividad de caracteres según `target_language_code`.

4. **Notificaciones y Estado:**
   - Implementar polling ligero para actualizar el estado del objeto `Exam` en la UI de "Lista de copias de estudio".
