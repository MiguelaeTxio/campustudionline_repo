### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md
2.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE DE ESTABILIZACIÓN Y RESILIENCIA)

## 1. RESUMEN TÉCNICO ACUMULADO (SESIÓN MAMC)
- **Semáforo de Concurrencia (Mutex):** Implementado en `orchestrator/tasks.py`. El sistema ahora garantiza la ejecución serial de evaluaciones para evitar errores 429 (Resource Exhausted) y proteger la salud del pool de claves Gemini.
- **Segregación del Flujo de Corrección:** Refactorizada la tarea `correct_assessment_task`. Ahora delega el prompt de evaluación en la Factory de estrategias, permitiendo criterios pedagógicos específicos para Lenguas y Humanidades.
- **Blindaje de Contexto (Humanidades):** La estrategia de Humanidades ahora obliga a la IA a transcribir íntegramente las fuentes primarias dentro del enunciado para evitar que el alumno trabaje "a ciegas".
- **Blindaje Idiomático (Lenguas):** Implementadas restricciones negativas estrictas en `languages_strategy.py` para erradicar el inglés en itinerarios no anglófonos.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: ERRADICACIÓN DE HARDCODEO EN UI (INMERSIÓN DINÁMICA)
- **Tarea:** Eliminar cadenas como "READING / TEXTO DE REFERENCIA" de las plantillas HTML (`take_assessment_languages.html` y `take_assessment.html`).
- **Lógica:** Implementar el método `get_ui_labels` en todas las estrategias.
- **Inmersión:**
    - Itinerario MINOR: Etiquetas según documentación.
    - Itinerario MAIOR: Etiquetas según documentación.

### PASO 2: AUDITORÍA DE PERSISTENCIA
- **Tarea:** Verificar que los cambios en `prompt_data` (especialmente `ui_labels`) se persisten correctamente durante todo el ciclo de vida de la evaluación (Generación -> Realización -> Corrección).
