# Hito 22: Refactorización de Navegación de Sala de Estudio (User-Centric)

**Estado:** EN PROGRESO (Fase 6 Completada - Backend Operativo)

**Progreso de la Sesión:**
*   **Reparación Crítica:** Corrección de errores de sintaxis bloqueantes en `search/views.py` y corrección de `contents/admin.py`.
*   **Sincronización DB:** Ejecución exitosa de la migración `0019` usando `SeparateDatabaseAndState`, eliminando las tablas legacy (`KnowledgeArea`, `Discipline`, etc.) y creando `UserStudyNavigation`.
*   **Backend de Navegación:** Implementación del servicio `contents/services/navigation_builder.py` y conexión de señales en `contents/signals.py`.
*   **Planificación:** Actualización del Plan Maestro de Refactorización para incluir fases de barrido de código huérfano.

**Hoja de Ruta para la Siguiente Sesión:**
*   **NOTA PISA:** Cargar obligatoriamente el documento dedicado: .
1.  **FASE 7: Barrido de Referencias Huérfanas (PRIORIDAD)**
    *   Ejecutar auditoría de código (grep) para localizar imports de modelos eliminados.
    *   Limpiar `contents/views.py`, `study_room_views.py` y `core/context_processors.py`.
    *   Verificar que no queden referencias rotas en templates.
2.  **FASE 8: Integración Frontend**
    *   Exponer el árbol JSON (`UserStudyNavigation`) al contexto del usuario.
    *   Implementar el componente visual del árbol de navegación.

