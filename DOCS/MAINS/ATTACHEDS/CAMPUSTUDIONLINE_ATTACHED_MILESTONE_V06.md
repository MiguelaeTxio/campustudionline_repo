### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

---

### ESTADO TÉCNICO POST-SESIÓN (RESOLUCIÓN DE PERSISTENCIA ATÓMICA)

**Estado:** ESTABILIZADO. Se ha erradicado la causa raíz de la pérdida de progreso.

**Logros de la Sesión:**
1.  **Diagnóstico Empírico:** Se confirmó que `assessment.save()` sin argumentos en el worker de Celery sobrescribía los cambios realizados por `.update()` SQL, borrando el `questions_cache`.
2.  **Blindaje "Iron-Clad Plus":** 
    *   Refactorización del orquestador para usar **Surgical Saves** (`update_fields`).
    *   Implementación de **Persistencia Física (JSON)** en `logs/assessment_recovery/` como redundancia ante fallos de base de datos o rollbacks de transacción.
3.  **Higiene Arquitectónica:** 
    *   Se eliminó la duplicidad crítica borrando el archivo zombie `assessment/tasks.py`. Toda la lógica reside ahora en `orchestrator`.
    *   Se eliminó el uso del directorio `SWAP` para archivos de control de la plataforma, moviéndolos a `BASE_DIR/logs/`.
4.  **Saneamiento de UI:** Eliminado error de renderizado `VariableDoesNotExist` en el bloque de estado del assessment.

**HOJA DE RUTA PARA LA SIGUIENTE SESIÓN:**
1.  **Validación de Recuperación:** Forzar una interrupción de red/cuota durante la generación para verificar que el sistema recupera el 100% del progreso desde el archivo JSON de respaldo.
2.  **Monitorización de Logs:** Verificar que el nuevo mensaje informativo ("PAUSA: Pool agotado") aparece correctamente en el panel de administración cuando todas las claves están en cuarentena.

