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
# ESTADO: EN PROGRESO (FASE 2: LÓGICA DE NEGOCIO COMPLETADA)

## 1. RESUMEN TÉCNICO
Se ha implementado el "Cerebro" del sistema de evaluación v2. La infraestructura de cuotas es operativa, permitiendo una gestión precisa de la frecuencia de uso por plan de suscripción. Se ha establecido el patrón Factory y la primera estrategia concreta (Idiomas), asegurando un estándar de "Calidad Total" (C-Level) para todos los niveles de usuario.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
Inicio de la **Fase 3: Integración de Flujo y UI**. El objetivo es conectar la lógica de backend con la interfaz de usuario y el motor asíncrono.

### TAREAS DE IMPLEMENTACIÓN (VISTAS Y TAREAS)
1.  **Vista de Creación de Examen (`views.py`):**
    *   Implementar `ExamCreateView` (FormView/CreateView).
    *   Integrar `QuotaService.check_exam_eligibility` como guardián de la vista.
2.  **Orquestación Asíncrona (`tasks.py`):**
    *   Definir la tarea Celery `generate_exam_task`.
    *   Lógica: Obtener estrategia -> Generar estructura -> Llamada a Gemini -> Guardar JSON en `Exam.structure`.
3.  **Frontend Base (Templates):**
    *   Crear el template de "Preparando Evaluación" con polling/HTMX para detectar el cambio de estado del examen de `GENERATING` a `READY`.
4.  **Refinamiento de Prompts:**
    *   Expandir `LanguagesStrategy.get_system_prompt` con las directrices de los documentos V06DOC_METADATA y V06DOC_LEVELS.
