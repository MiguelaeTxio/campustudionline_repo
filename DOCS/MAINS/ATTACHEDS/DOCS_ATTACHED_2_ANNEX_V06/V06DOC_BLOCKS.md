<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_BLOCKS.md -->
# V06DOC_BLOCKS - CATÁLOGO DE MOTORES DE EVALUACIÓN (V1.1 - REFACTORIZACIÓN UGR)

## 1. BLOQUES DE EVALUACIÓN OBJETIVA Y TÉCNICA\n\n*   **EV-TRA-PRECISION-TECH (Motor de Precisión Terminológica FTI-UGR) [NUEVO 2026]**
    *   **Mecánica:** Evaluación basada en la jerarquía de errores de la FTI.
    *   **Categoría A (Sentido):** Contrasentido (-2.0), Sin sentido (-1.5), Falso sentido (-1.0).
    *   **Categoría B (Terminología):** Uso de lemas no especializados en dominios técnicos. Penalización: -0.5.
    *   **Categoría C (Gramática y Estilo):** Inadecuación de registro y errores ortotipográficos (OLE 2010). Penalización: -0.2.

*   PRM-STRIKE (Respuesta Múltiple con Penalización Progresiva):
    *   Mecánica: Fórmula de corrección por azar UGR [Aciertos - (Errores/(N-1))].
    *   Calidad: Generación de distractores basados en errores conceptuales comunes.
    *   Parámetro: PUN_REST (Activo).
    *   **EXCEPCIÓN CRÍTICA — SUB-LIN-INSTR (CertAcles / CLM-UGR):** Este motor queda DESACTIVADO para el subarquetipo SUB-LIN-INSTR en las destrezas SD_READ y SD_LIST. La Guía Oficial del Candidato CLM-UGR establece explícitamente que las respuestas incorrectas en Comprensión de Lectura y Comprensión Auditiva NO restan puntuación. El motor W-OBJ-STRIKE en INSTR opera en modo NO_NEGATIVE_MARKING (PUN_REST: Inactivo).

*   RBT-CANON (Respuesta Breve de Precisión Terminológica):
    *   Mecánica: Validación por lexemas nucleares y palabras clave obligatorias.
    *   Calidad: No admite paráfrasis en niveles MAIOR o PROF.
    *   Parámetro: TERM_PREC (Máximo).

*   **RBT-SHORT-LANG (Respuesta Breve Lingüística - UGR/CertAcles) [REFACTORIZADO V4.2]**
    *   **Mecánica:** Validación de precisión léxica y morfología exacta.
    *   **Extensión:** 1-4 palabras (Filtro automático).
    *   **Módulo de Trazos (Minor/Iniciación):** En lenguas no latinas, el motor valida el ductus (orden y dirección de trazos) y la integridad grafémica del carácter mediante comparación de patrones OCR. La desviación del ductus normativo penaliza el ítem en un 50%.

*   RPP-TRAZA (Resolución Procedimental con Arrastre de Error):
    *   Mecánica: Calificación multietapa con validación de la coherencia lógica.
    *   Calidad: Permite puntuación parcial si el desarrollo es correcto pese a un error inicial.
    *   Parámetro: STEP_TRAZA (Activo).

## 2. BLOQUES DE SEGURIDAD Y ANÁLISIS CRÍTICO

*   CDS-KILL (Checklist Dicotómico de Seguridad Crítica):
    *   Mecánica: Verificación de pasos irrenunciables (Puntos de Control Crítico).
    *   Calidad: La omisión de un paso de seguridad anula la sección completa.
    *   Parámetro: KILL_SWITCH (Activo).

*   DRA-HOLO (Rúbrica Analítica Holística - Acreditación UGR/CertAcles):
    *   **Mecánica:** Evaluación criterial mediante rúbrica de 4 ejes con escala de 0 a 2.5 puntos por eje (Total: 10 pts).
    *   **Ejes de Evaluación (Standard UGR):**
        1. **Adecuación al encargo:** Cumplimiento de la extensión, registro formal/informal y objetivos comunicativos del input.
        2. **Cohesión y Coherencia:** Estructura lógica del texto, uso eficaz de marcadores del discurso y puntuación.
        3. **Riqueza y Variedad Léxica:** Precisión terminológica y uso de expresiones idiomáticas según el nivel MCERL.
        4. **Corrección Gramatical:** Control de estructuras simples y complejas; ausencia de errores sistemáticos o fosilizados.
    *   **Parámetro de Penalización:** FORM_PEN (Hasta -2.5 puntos por fallos en ortografía técnica).
*   BMT-SHIFT (Mediación y Transferencia de Registro):
    *   Mecánica: Adaptación de información técnica a lenguaje divulgativo o viceversa.
    *   Calidad: Evaluación de la fidelidad informativa y adecuación al destinatario.

*   ILC-CONTEXT (Interpretación de Contexto y Datos Brutos):
    *   Mecánica: Inferencia basada en sets de datos (analíticas, gráficos, balances).
    *   Calidad: Valida la capacidad de diagnóstico/decisión, no la lectura del dato.

*   EV-PALE (Transcripción y Exégesis de Fuentes Primarias):
    *   Mecánica: Transcripción exacta y comentario crítico de fuentes originales.
    *   Calidad: Rigor en normas de edición crítica y datación.

## 3. BLOQUES LINGÜÍSTICOS ESTRUCTURALES (NUEVO V1.1)

*   CLO-OPEN (Open Cloze / Rellenado Abierto):
    *   Mecánica: Completar huecos en un texto sin opciones visibles. Evalúa gramática y colocaciones precisas.
    *   Calidad: Validación estricta de lema/morfología. Se apoya en el motor RBT-SHORT-LANG.
    *   Widget: W-TXT-CLOZE (Modo Input).

*   CLO-MULTI (Multiple Choice Cloze / Rellenado Selectivo):
    *   Mecánica: Completar huecos eligiendo entre 4 opciones semánticas/gramaticales.
    *   Calidad: Distractores basados en "False Friends" o errores comunes de hispanohablantes.
    *   Widget: W-TXT-CLOZE (Modo Dropdown).

*   MAT-LINK (Matching / Emparejamiento):
    *   Mecánica: Vincular párrafos con títulos (Reading) o hablantes con ideas (Listening).
    *   Widget: W-MIX-MATCH.

*   DIA-INTERACT (Interacción Dialéctica Asistida por UniversIA):
    *   Mecánica: Simulación de conversación, entrevista oral o mediación evaluada en tiempo real.
    *   Calidad: Evaluación de fluidez, registro léxico, adecuación pragmática y capacidad de reacción.
    *   Widget: W-COMM-DIALOG.

## 4. MOTORES ESPECIALIZADOS PHILO (UGR) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR]

*   **EV-DIAC-VAL (Motor de Validación Diacrónica / Evolución Fonética):**
    *   **Mecánica de Evaluación por Estadios:** El motor no valida solo el resultado final, sino la **secuencia lógica y cronológica** de cambios. Cada estadio evolutivo intermedio (ej. latín vulgar, romance medieval, español áureo) es un punto de control obligatorio.
    *   **Validación de Leyes Fonéticas:** El sistema exige la asignación correcta de la ley (apócope, síncopa, sonorización, vocalización) a cada cambio gráfico.
    *   **Módulo de Yod y Wau (UGR):** Capacidad específica para identificar y validar los cuatro tipos de Yod y su efecto metafónico o palatalizador. La clasificación errónea del tipo de Yod (I, II, III o IV) penaliza el estadio evolutivo en un 100%.
    *   **Criterio de Cronología Relativa:** Validación del orden de aplicación de las leyes. Si un estadio posterior contradice una ley fonética previa (ej: sonorización que ocurre después de una síncopa que eliminó el contexto intervocálico), el ítem se marca como fallido (FATAL).
    *   **Parámetros Técnicos:** `CHRONO_STRICT` (Activo) | `YOD_IDENTIFICATION` (Obligatorio).

*   **EV-PALE (Motor de Transcripción y Exégesis de Fuentes Primarias):**
    *   **Mecánica de Doble Validación (UGR):**
        1.  **Nivel Paleográfico (Literal):** Validación de grafemas históricos respetando la grafía original (u/v, i/j, s larga, cedilla, doble f inicial).
        2.  **Nivel Crítico (Resolución Braquigráfica):** Evaluación del desarrollo de abreviaturas. El alumno debe expandir la abreviatura (ej: "p" con tilde > "por" / "q" con tilde > "que") siguiendo las normas de edición de la UGR.
    *   **Detección de Nexos y Ligaduras:** Validación de la correcta interpretación de nexos complejos (ej: ct, st en gótica) y signos de abreviación específicos para desinencias latinas (-us, -rum).
    *   **Exégesis Crítica:** Capacidad para comparar la transcripción con el aparato crítico y detectar "lectio difficilior" (lectura más difícil, generalmente preferida en crítica textual).
    *   **Parámetro:** `BRAQUI_RESOLVE` (Activo).

*   **EV-NORM-ANALYSIS (Motor de Análisis de Desviaciones Panhispánicas):**
    *   **Mecánica:** Detección de infracciones prescriptivas (RAE/ASALE) y contraste con el uso real mediante Corpus (CORPES XXI/CREA).
    *   **Calidad:** Evalúa la identificación del fenómeno antinormativo (ej. laísmo, dequeísmo, queísmo, leísmo de cosa), la corrección y la justificación basada en el DPD o la Nueva Gramática de la Lengua Española (NGLE).
    *   **Uso de Fuentes:** El motor debe citar la norma vulnerada para proporcionar el feedback académico exigido en la UGR.

*   **EV-TRA-PRECISION (Motor de Precisión Terminológica en Traducción):**
    *   **Mecánica:** Validación de equivalencias terminológicas en dominios especializados basándose en glosarios técnicos y diccionarios de especialidad.
    *   **Calidad:** Evalúa la univocidad en la lengua de llegada y la adecuación al registro meta.

## 5. MOTORES ESPECÍFICOS PARA EL MODELO INSTRUMENTAL (UGR 2026) [ADICIÓN QUIRÚRGICA - FIDELIDAD 100%]

Esta sección define la configuración técnica de los motores de evaluación cuando se activan bajo el subarquetipo SUB-LIN-INSTR (CertAcles / CLM-UGR).

### A. MOTOR DE MEDIACIÓN LINGÜÍSTICA (BMT-SHIFT - INSTRUMENTAL) [ACTUALIZADO v5.0]
*   **Nota de Alcance:** A partir de la versión 5.0, la Mediación Lingüística (SD_MEDI) NO constituye una destreza independiente en el subarquetipo SUB-LIN-INSTR. El motor BMT-SHIFT en contexto INSTR queda reservado como componente auxiliar de SD_WRIT (Tarea 2 — Nivel B2) cuando el tipo textual del encargo exige la síntesis o adaptación de información de un estímulo fuente (ej. informe o reseña con datos). No genera sección de examen autónoma ni cuenta como destreza separada en el cómputo de superación.
*   **Mecánica de Evaluación (Auxiliar SD_WRIT):** El motor actúa como auditor de transferencia informativa dentro de la tarea de producción escrita. Evalúa la capacidad del alumno para procesar un estímulo fuente (gráfico, tabla o texto técnico) e integrarlo adecuadamente en su producción escrita, adaptando el registro al destinatario especificado en el encargo.
*   **Criterios de Calificación (Integrados en DRA-HOLO):**
    1. **Fidelidad Informativa:** La IA detecta y penaliza la omisión de datos críticos presentes en la fuente o la inclusión de información no verificable.
    2. **Adecuación de Registro:** Se evalúa la simplificación del lenguaje técnico y la adecuación al destinatario. Estos criterios se integran en los ejes "Cumplimiento de la Tarea" y "Competencia Lingüística General" de la rúbrica DRA-HOLO.
*   **Motor Autónomo (SUB-LIN-TRA-TECH / SUB-LIN-TRA-LIT):** El motor BMT-SHIFT mantiene su configuración autónoma completa (con umbral de éxito independiente y evaluación de Fidelidad Informativa al 50% + Adecuación de Registro al 50%) exclusivamente para los subarquetipos de Traducción.

### B. CONFIGURACIÓN DE RÚBRICA DRA-HOLO (CERTACLES B1/B2) [CORREGIDO v5.0 - FIDELIDAD 100% UGR]
*   **Estructura de Evaluación (Cinco Criterios Institucionales CLM-UGR):**
    1. **Cumplimiento de la Tarea (Task Achievement):** Adecuación al tipo textual solicitado (carta, email, informe, ensayo, narración, reseña), cumplimiento de la extensión léxica obligatoria (**200-250 palabras para Tarea B1 / 250-300 palabras para Tarea B2**) y cobertura de todos los puntos de control informativos especificados en el enunciado. (0 - 2.0 pts).
    2. **Coherencia y Cohesión:** Estructura lógica del texto, uso eficaz de marcadores del discurso, organización en párrafos con progresión temática clara y puntuación adecuada. (0 - 2.0 pts).
    3. **Competencia Lingüística General:** Capacidad de expresión global: fluidez, naturalidad y adecuación del registro (informal/neutro para B1; formal añadido para B2). (0 - 2.0 pts).
    4. **Corrección Gramatical:** Control de estructuras simples y complejas. Se penalizan especialmente los errores fosilizados (concordancia sujeto-verbo, tiempos verbales básicos, uso de preposiciones). (0 - 2.0 pts).
    5. **Dominio y Riqueza de Vocabulario:** Precisión terminológica, variedad léxica y uso de expresiones idiomáticas según el nivel MCERL. En B2 se exige el uso de colocaciones y vocabulario abstracto. (0 - 2.0 pts).
*   **Penalización Formal (FORM_PEN):** Descuentos automáticos sobre la nota bruta: -0.1 pts por cada falta de ortografía; -0.05 pts por cada error ortotipográfico (tildes, signos de puntuación). Umbral de exclusión: más de 5 faltas de ortografía en una sola tarea → anulación de la tarea (Nota: 0.0 — FAIL_LOGIC: FATAL en esa tarea).
*   **Regla de No-Compensación entre Tareas:** Cada tarea se evalúa de forma independiente. La nota global de SD_WRIT es la media de ambas tareas, pero si una tarea es anulada por el umbral de exclusión de faltas, la destreza completa queda marcada como no superada.

### C. MOTOR DE VALIDACIÓN AUDITIVA (LISTENING RIGOR)
*   **Control de Acceso:** El motor de reproducción de audio se bloquea herméticamente tras la segunda audición completa. El sistema registra el timestamp de cada reproducción para evitar manipulaciones de caché.
*   **Validación de Ítems (RBT-SHORT-LANG):** Para las tareas de completado de esquemas o toma de notas, el motor valida respuestas de 1 a 4 palabras. Aplica un algoritmo de *Fuzzy Matching* con una tolerancia de distancia de Levenshtein mínima para errores tipográficos que no afecten al lema (ej. omisión de una letra muda), pero mantiene rigor absoluto en la semántica del concepto.

### D. BAREMO DE PENALIZACIÓN FORMAL (FORM_PEN - INSTRUMENTAL) [CORREGIDO v5.0 - FIDELIDAD 100% UGR]
En cumplimiento de la normativa del CLM-UGR, se aplican descuentos automáticos sobre la nota bruta de la producción escrita (SD_WRIT únicamente — la Mediación NO es destreza independiente en SUB-LIN-INSTR):
*   **Faltas de Ortografía:** -0.1 puntos por cada error ortográfico.
*   **Tildes y Puntuación:** -0.05 puntos por cada error ortotipográfico (incluyendo puntuación ortotipográfica técnica).
*   **Umbral de Exclusión Unificado:** La presencia de más de 5 faltas de ortografía en una sola tarea conlleva la anulación inmediata de esa tarea (Nota: 0.0 — FAIL_LOGIC: FATAL en esa tarea). Este umbral es coherente con el declarado en V06DOC_SUBARCHETYPES.md y V06DOC_LEVELS.md para SUB-LIN-INSTR.
*   **Nota de Coherencia Documental:** Este baremo aplica exclusivamente a SD_WRIT. Las destrezas SD_READ y SD_LIST no aplican penalizaciones por respuesta incorrecta (NO_NEGATIVE_MARKING activo). La destreza SD_SPEAK es evaluada mediante rúbrica analítica DIA-INTERACT sin baremo de faltas ortográficas.
