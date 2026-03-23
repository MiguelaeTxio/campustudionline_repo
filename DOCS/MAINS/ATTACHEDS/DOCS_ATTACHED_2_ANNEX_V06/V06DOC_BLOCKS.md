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