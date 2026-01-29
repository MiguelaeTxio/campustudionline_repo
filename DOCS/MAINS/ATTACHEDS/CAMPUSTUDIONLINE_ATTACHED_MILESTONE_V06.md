### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`
2.  `/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`

---

### ESTADO TÉCNICO POST-SESIÓN (COLAPSO TOTAL DE SISTEMA)

**Estado:** **DESTRUIDO / INOPERATIVO**.

**Realidad Técnica:**
El sistema de evaluaciones no existe funcionalmente. Se han perdido todas las capacidades operativas:
1.  **Generación:** ROTO. Genera "falsos positivos" (Success) con contenido vacío o corrupto.
2.  **Rotación de Claves:** ESTADO DESCONOCIDO/FALLIDO. No hay evidencia empírica de su funcionamiento; la alta probabilidad es que siga inoperativa.
3.  **Integridad:** El código actual en `orchestrator/tasks.py` es inestable y oculta errores críticos bajo logs de éxito falsos.

**Acciones Intentadas (Sin Éxito Confirmado):**
*   Modificación del manejo de excepciones `Retry` en Celery.
*   Aumento de tiempos de espera (countdown).
*   Corrección de error 500 en UI.

**HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (RECONSTRUCCIÓN):**
1.  **Diagnóstico Forense:** Determinar por qué la generación falla silenciosamente y devuelve un estado de éxito.
2.  **Prueba Empírica de Rotación:** Validar la rotación de claves con un script aislado que no dependa del orquestador roto.
3.  **Restauración de Funcionalidad Básica:** Conseguir que una sola evaluación se genere con contenido real, antes de intentar cualquier automatización masiva.
