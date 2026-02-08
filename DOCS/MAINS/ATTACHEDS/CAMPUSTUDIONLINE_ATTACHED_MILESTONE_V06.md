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

### PARTE MUTABLE PERO MANDATORIA EN TODOS LOS PCS

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE IMPLEMENTACIÓN - ESTRUCTURA BASE COMPLETADA)

## 1. RESUMEN TÉCNICO
Se ha establecido la arquitectura segregada del sistema. La aplicación `assessment_v2` ha sido creada e integrada. Los modelos de datos fundamentales (`SubscriptionPlan`, `UserSubscription`, `TokenUsage`, `CostLog`, `Exam`, `Submission`) han sido implementados y migrados a la base de datos, siguiendo las especificaciones de los anexos V06DOC.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
Continuación de la **Fase 2: Implementación Alpha**. El objetivo es dotar de lógica al esqueleto creado, implementando los servicios de validación y el motor de generación.

### TAREAS DE IMPLEMENTACIÓN (MOTOR Y SERVICIOS)
1.  **Servicio de Cuotas y Planes (`services/quotas.py`):**
    *   Implementar lógica para verificar `daily_exam_limit` y `weekly_exam_limit` consultando `UserSubscription` y `TokenUsage`.
    *   Implementar decoradores o mixins para validación de acceso.
2.  **Fábrica de Exámenes (`services/engine/factory.py`):**
    *   Crear la clase `ExamFactory` responsable de orquestar la creación del objeto `Exam`.
    *   Implementar la lógica de selección de estrategia basada en el `archetype_id`.
3.  **Estrategias de Generación (`services/engine/strategies/`):**
    *   Definir la interfaz base `BaseAssessmentStrategy` en `base.py`.
    *   Implementar la primera estrategia concreta: `LanguagesStrategy` (`languages.py`) correspondiente al Arquetipo 1 (CertAccles).
4.  **Integración con Gemini (Preliminar):**
    *   Configurar los prompts de sistema para el Arquetipo 1 en `CONTENT_PROMPTS.md` (o archivo dedicado si se requiere).
