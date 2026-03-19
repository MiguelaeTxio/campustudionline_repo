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

*   DRA-HOLO (Rúbrica Analítica Holística - Especialización FTI UGR):
    *   **Mecánica:** Evaluación en 4 ejes específicos para Traducción Literaria (0-10 pts).
    *   **Ejes de Evaluación:**
        1. **Fidelidad Estilística:** Captación del tono y registro del autor original.
        2. **Transferencia Estética:** Recreación del efecto literario (metáfora, ritmo).
        3. **Gestión de Culturemas:** Resolución de referentes culturales e ironía.
        4. **Calidad Lingüística Meta:** Riqueza léxica y elegancia formal (RAE/ASALE).
    *   **Parámetro:** FORM_PEN (Hasta -2.5 puntos).
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

*   **EV-NORM-ANALYSIS (Motor de Análisis de Desviaciones): [REFACTORIZADO UGR 2025/26]**
    *   **Mecánica:** Detección de infracciones prescriptivas (RAE/ASALE) y contraste con el uso real mediante Corpus (CORPES XXI/CREA).
    *   **Calidad:** Evalúa la identificación del fenómeno antinormativo (ej. laísmo, dequeísmo), la corrección y la justificación basada en el DPD o la Gramática Académica.

*   **EV-DIAC-VAL (Motor de Validación Diacrónica):**
    *   **Mecánica:** Validación de secuencias de cambio lingüístico y leyes fonéticas históricas.
    *   **Calidad:** El motor evalúa la identificación del paso fonético intermedio (etimología) y el rigor en la transcripción.

*   **EV-NORM-ANALYSIS (Motor de Análisis de Desviaciones):**
    *   **Mecánica:** Detección y corrección de infracciones de la norma académica RAE/ASALE.
    *   **Calidad:** El motor evalúa no solo el error, sino la capacidad de explicar la norma subyacente que ha sido vulnerada.

*   **EV-TRA-PRECISION (Motor de Precisión Terminológica):**
    *   **Mecánica:** Validación de equivalencias terminológicas en dominios especializados (Derecho, Medicina, Técnica).
    *   **Calidad:** Evalúa la univocidad en la lengua de llegada y el uso correcto de glosarios técnicos.
