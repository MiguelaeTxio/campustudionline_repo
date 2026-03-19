<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_BLOCKS.md -->
# V06DOC_BLOCKS - CATÁLOGO DE MOTORES DE EVALUACIÓN (V1.1 - REFACTORIZACIÓN UGR)

## 1. BLOQUES DE EVALUACIÓN OBJETIVA Y TÉCNICA

*   PRM-STRIKE (Respuesta Múltiple con Penalización Progresiva):
    *   Mecánica: Fórmula de corrección por azar UGR [Aciertos - (Errores/(N-1))].
    *   Calidad: Generación de distractores basados en errores conceptuales comunes.
    *   Parámetro: PUN_REST (Activo).

*   RBT-CANON (Respuesta Breve de Precisión Terminológica):
    *   Mecánica: Validación por lexemas nucleares y palabras clave obligatorias.
    *   Calidad: No admite paráfrasis en niveles MAIOR o PROF.
    *   Parámetro: TERM_PREC (Máximo).

*   **RBT-SHORT-LANG (Respuesta Breve Lingüística - UGR/CertAcles) [NUEVO]**
    *   **Mecánica:** Validación estricta de precisión léxica y gramatical.
    *   **Restricción:** Longitud obligatoria de **1 a 4 palabras**. Cualquier respuesta fuera de este rango se califica como 0 automáticamente.
    *   **Calidad:** El motor valida lemas y morfología exacta según el contexto del texto (gap-filling).

*   RPP-TRAZA (Resolución Procedimental con Arrastre de Error):
    *   Mecánica: Calificación multietapa con validación de la coherencia lógica.
    *   Calidad: Permite puntuación parcial si el desarrollo es correcto pese a un error inicial.
    *   Parámetro: STEP_TRAZA (Activo).

## 2. BLOQUES DE SEGURIDAD Y ANÁLISIS CRÍTICO

*   CDS-KILL (Checklist Dicotómico de Seguridad Crítica):
    *   Mecánica: Verificación de pasos irrenunciables (Puntos de Control Crítico).
    *   Calidad: La omisión de un paso de seguridad anula la sección completa.
    *   Parámetro: KILL_SWITCH (Activo).

*   DRA-HOLO (Disertación con Rúbrica Analítica Holística):
    *   Mecánica: Evaluación en 4 ejes: Rigor, Estructura, Terminología y Forma.
    *   Calidad: Penalización directa por deficiencias en el registro académico o faltas.
    *   Parámetro: FORM_PEN (Hasta -2.5 puntos).
    *   **Taxonomía de Errores UGR (Inyectada):**
        1. **ERR_TRANS (Transferencia):** Calcos de la lengua materna (L1) que afectan al significado.
        2. **ERR_NORM (Norma):** Violaciones de la gramática, ortografía o morfología normativa.
        3. **ERR_REG (Registro):** Uso de lenguaje inapropiado para el contexto (ej. coloquial en un ensayo).
        4. **ERR_COH (Cohesión):** Fallos en el uso de conectores y estructuración del discurso.

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

## 4. MOTORES ESPECIALIZADOS PHILO (UGR)
*   **EV-DIAC-VAL (Motor de Validación Diacrónica):**
    *   **Mecánica:** Validación de secuencias de cambio lingüístico y leyes fonéticas históricas.
    *   **Calidad:** El motor evalúa la identificación del paso fonético intermedio (etimología) y el rigor en la transcripción.

*   **EV-NORM-ANALYSIS (Motor de Análisis de Desviaciones):**
    *   **Mecánica:** Detección y corrección de infracciones de la norma académica RAE/ASALE.
    *   **Calidad:** El motor evalúa no solo el error, sino la capacidad de explicar la norma subyacente que ha sido vulnerada.

*   **EV-TRA-PRECISION (Motor de Precisión Terminológica):**
    *   **Mecánica:** Validación de equivalencias terminológicas en dominios especializados (Derecho, Medicina, Técnica).
    *   **Calidad:** Evalúa la univocidad en la lengua de llegada y el uso correcto de glosarios técnicos.
