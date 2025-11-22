# Hito 22: Refactorización de Navegación de Sala de Estudio (User-Centric)

**Estado:** EN PROGRESO (Fases 7 y 8 Completadas - FASE 6 PENDIENTE Y CRÍTICA)

**Resumen de la Sesión:**
*   **Fase 7 (Limpieza):** Se eliminaron referencias huérfanas a modelos legacy (`Topic`, etc.) en `contents/views.py`.
*   **Fase 8 (Frontend):** Se implementó el componente visual `_navigation_sidebar.html` y se integró en `base.html` y `context_processors.py`. El árbol de navegación se visualiza correctamente.
*   **DIAGNÓSTICO DE ERROR CRÍTICO (404):** Se confirmó que la **Fase 6** (Adaptación de Vistas Backend) fue omitida erróneamente. `contents/study_room_views.py` sigue usando lógica legacy (`get_object_or_404` contra tablas), provocando errores 404 al navegar.
*   **DIAGNÓSTICO ORQUESTADOR:** Se detectó un error bloqueante en `orchestrator/tasks.py` (`TypeError: 'topic'`) que impide la generación de nuevo contenido.

**Hoja de Ruta para la Siguiente Sesión (PRIORIDAD ABSOLUTA):**
1.  **EJECUCIÓN DE FASE 6 (Recuperación):** Refactorizar `contents/study_room_views.py` (vista `user_copies_list`) para consumir exclusivamente `UserStudyNavigation` (JSON) y eliminar validaciones contra DB legacy. **Esto solucionará los 404.**
2.  **REPARACIÓN ORQUESTADOR:** Modificar `orchestrator/tasks.py` para eliminar la asignación del campo eliminado `topic`.
3.  **Verificación Final:** Confirmar navegación fluida sin 404 y reanudación de tareas de Celery.

