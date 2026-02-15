### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
La próxima sesión debe cargarse con los siguientes documentos para garantizar el contexto completo del Estándar de Máxima Calidad:
*   V06DOC_ARCHETYPES.md
*   V06DOC_SUBARCHETYPES.md
*   V06DOC_SUBDIVISIONS.md
*   V06DOC_BLOCKS.md
*   V06DOC_WIDGETS.md
*   V06DOC_METADATA.md
*   V06DOC_LEVELS.md
*   V06DOC_TEMPLATES.md
*   V06DOC_STRUCTURE.md
*   V06DOC_LOGIC_MAPPING.md

### PARTE MUTABLE PERO MANDATORIA EN TODOS LOS PCS

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE 3: CONSOLIDACIÓN DE INTERFAZ Y ENTREGA)

## 1. RESUMEN TÉCNICO DE LA SESIÓN
Se ha realizado una reconstrucción estructural profunda alineada con el Santo Grial (v06DOC):
*   **Mapeo Relacional:** Refactorizado el modelo de datos en 'assessment_v2/models/main.py' para sustituir el JSON plano por tablas relacionales ('ExamSection', 'ExamItem').
*   **Automatización Pedagógica:** Implementado el 'AcademicDeductor' (logic.py) para clasificar exámenes mediante regex según 'V06DOC_LOGIC_MAPPING'.
*   **Segregación de Orquestación:** Refactorizada 'generate_exam_task' en 'orchestrator/tasks.py' para gestionar la persistencia relacional y el control de costes mediante 'TrackingService'.
*   **Motor de Calificación:** Integrada la fórmula de penalización interna [Aciertos - (Errores/(N-1))] en 'LanguagesStrategy' según 'V06DOC_BLOCKS'.
*   **Estandarización UI:** Creado el motor de renderizado de widgets en 'exam_take.html' y el primer componente funcional: 'W-OBJ-STRIKE'.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
**FUENTE DE VERDAD ABSOLUTA:** Es **MANDATORIO** utilizar la constelación documental **v06DOC** para completar la interfaz.

### TAREAS CRÍTICAS (ORDEN OBLIGATORIO)
1.  **Cierre del Ciclo de Usuario (Frontend JS):**
    *   Implementar en 'exam_take.html' el script JS que recolecte respuestas de widgets y realice el 'POST' a 'ExamSubmitView'.
2.  **Visualización de Resultados (Exam Report):**
    *   Crear 'ExamReportView' y la plantilla 'exam_report.html' para mostrar el desglose de calificación y el feedback del reporte.
3.  **Captura Real de Consumo:**
    *   Actualizar 'gemini_service.py' para retornar metadatos de tokens y vincularlos al 'TrackingService' desde la tarea de Celery.
