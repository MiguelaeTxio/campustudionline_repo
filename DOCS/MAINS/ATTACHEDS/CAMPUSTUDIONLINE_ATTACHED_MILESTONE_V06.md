### PARTE INMUTABLE (MANDATORIA EN TODOS LOS PCS)

**DIRECTRIZ DE CARGA OBLIGATORIA (LEY DE CONTINUIDAD):**
Al iniciar cualquier sesión de trabajo sobre el sistema de evaluaciones, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del Emulador UGR:
1.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md
2.  /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md

---

# ANEXO: HITO 06 - SISTEMA DE AUTOEVALUACIONES CON IA
# ESTADO: EN PROGRESO (FASE DE ESTABILIZACIÓN Y RESILIENCIA)

## 1. RESUMEN TÉCNICO ACUMULADO (SESIÓN PLUTO)
- **Eliminación de Ceguera:** Implementada la segmentación física (*slicing*) en `assessment/utils.py`. El orquestador ya no envía el contenido total, sino solo el rango seleccionado por el usuario.
- **Inyección Académica:** Todas las estrategias (`factory.py`) ahora reciben y procesan el `syllabus` y los `learning_objectives` del `Subject`.
- **Blindaje de Integridad (Gatekeeper):**
    - **Duplicados:** El orquestador valida que no existan opciones repetidas y que haya exactamente 4 distractores en tipos de test.
    - **Memoria de Sesión:** Se implementó `already_covered` para evitar que la IA pregunte el mismo concepto en ítems diferentes del mismo examen.
- **UI & UX:**
    - Unificación de etiquetas de subida a **"Subir archivo (Foto)"**.
    - Configuración de MathJax 3 para renderizado de fórmulas en línea (`$`) en exámenes y Sala de Estudio.
    - Eliminación del botón de reporte automático para simplificar el flujo hacia feedback manual.
- **Resiliencia API:** Implementado cooldown de 75s ante errores de cuota para proteger el pool de 102 claves Gemini de bloqueos masivos.

## 2. HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: RE-ARQUITECTURA DE ESTRATEGIA HUMANIDADES
- **Tarea:** La estrategia actual es demasiado genérica. Se debe refactorizar `humanities_strategy.py` para alejarse del ensayo libre y forzar una estructura de:
    1. Análisis de Fragmento (Fuente primaria).
    2. Relación con el Contexto Histórico/Cultural del syllabus.
    3. Debate crítico sobre tesis predefinidas.

### PASO 2: CORRECCIÓN DE IDIOMA E INMERSIÓN
- **Tarea:** Atender la anomalía "son del inglés". Auditar por qué en itinerarios `MINOR` o para lenguas latinas (Italiano/Francés) la IA introduce términos o estructuras anglófonas.
- **Acción:** Endurecer el prompt de `languages_strategy.py` para prohibir cualquier token en inglés si la lengua objetivo es diferente, y asegurar que la inmersión híbrida (Instrucciones en ES / Contenido en Lang) sea estricta.

### PASO 3: AUDITORÍA DEL FLUJO DE CORRECCIÓN
- **Tarea:** Una vez estabilizada la generación, auditar `correct_assessment_task` para asegurar que el feedback de la IA sea coherente con el nuevo nivel académico de las preguntas.
