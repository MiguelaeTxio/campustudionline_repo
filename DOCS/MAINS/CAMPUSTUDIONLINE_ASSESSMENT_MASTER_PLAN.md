# PLAN MAESTRO DE EVALUACIONES: EMULACIÓN DE ESTÁNDARES UGR

**Objetivo Estratégico:** Crear un emulador de exámenes que replique fielmente la experiencia, rigor y estructura de la Universidad de Granada (UGR). Un alumno no debe percibir diferencia técnica o pedagógica entre un examen oficial y uno de CampuStudiOnline.

---

## 1. ARQUITECTURA DE CLASIFICACIÓN (EL RECTOR)
El sistema clasifica cada asignatura en uno de los 5 Departamentos de Evaluación basados en competencias, no solo en el nombre del grado.

### ARQUETIPO 1: LOGIC_AND_TECH (Ciencias Exactas e Ingeniería)
*   **Foco:** Resolución de problemas y lógica formal.
*   **Estructura:** 4 Preguntas de desarrollo técnico.
*   **Requisitos:** Uso de LaTeX para fórmulas y bloques de código/pseudocódigo para algoritmos.

### ARQUETIPO 2: CEFR_LANGUAGES (Centro de Lenguas Modernas - CLM)
*   **Foco:** Las 4 destrezas del Marco Común Europeo (Listening, Speaking, Reading, Writing).
*   **Estructura Multimodal:** Requiere botones de [PLAY] y [GRABACIÓN AUTOMÁTICA].

### ARQUETIPO 3: SOCIO_LEGAL (Derecho y Ciencias Sociales)
*   **Foco:** Aplicación normativa y análisis de casos.
*   **Estructura:** Test de conceptos, Resolución de Caso Práctico y Análisis Crítico.

### ARQUETIPO 4: HEALTH_SCIENCES (Ciencias de la Salud)
*   **Foco:** Razonamiento clínico y protocolos de actuación.

### ARQUETIPO 5: HUMANITIES_ARTS (Artes y Humanidades)
*   **Foco:** Dialéctica, análisis de fuentes primarias y estética.

---

## 2. REGLAS DE ORO DE IMPLEMENTACIÓN (INMUTABLES)
1.  **Detección de Idioma Nativa:** TTS y transcriptor con acento correcto según asignatura.
2.  **Etiquetas de Control Frontend:** `[---AUDIO-REQUIRED---]` y `[---RECORDING-REQUIRED---]`.
3.  **Grabación Inteligente:** Auto-stop tras (Estimación IA + 15 segundos).
4.  **Transcripts Limpios:** Solo texto hablado, sin acotaciones ni instrucciones.
5.  **Persistencia de Clasificación:** El arquetipo guardado en BBDD es inamovible tras la primera generación.

---

## 3. HOJA DE RUTA TÉCNICA (Control de Progreso en Anexo de Hito)
1. Refactor de Orchestrator: Persistencia de Arquetipo y Gestión de Reintentos.
2. Implementación de Estrategia CEFR_LANGUAGES (Frontend y Prompt Multimodal).
3. Implementación de Estrategia LOGIC_AND_TECH (LaTeX y Pseudocódigo).
4. Implementación de Estrategia SOCIO_LEGAL (Casos Prácticos).
5. Implementación de Estrategia HEALTH_SCIENCES (Escenarios Clínicos).
6. Implementación de Estrategia HUMANITIES_ARTS (Análisis Dialéctico).
