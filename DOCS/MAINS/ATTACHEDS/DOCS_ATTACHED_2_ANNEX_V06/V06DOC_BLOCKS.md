# V06DOC_BLOCKS - CATÁLOGO DE MOTORES DE EVALUACIÓN (V1.1)

## 1. BLOQUES DE EVALUACIÓN OBJETIVA Y TÉCNICA

*   PRM-STRIKE (Respuesta Múltiple con Penalización Progresiva):
    *   Mecánica: Fórmula de corrección por azar UGR [Aciertos - (Errores/(N-1))].
    *   Calidad: Generación de distractores basados en errores conceptuales comunes.
    *   Parámetro: PUN_REST (Activo).

*   RBT-CANON (Respuesta Breve de Precisión Terminológica):
    *   Mecánica: Validación por lexemas nucleares y palabras clave obligatorias.
    *   Calidad: No admite paráfrasis en niveles MAIOR o PROF.
    *   Parámetro: TERM_PREC (Máximo).

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
    *   Calidad: Validación estricta de lema/morfología.
    *   Widget: W-TXT-CLOZE (Modo Input).

*   CLO-MULTI (Multiple Choice Cloze / Rellenado Selectivo):
    *   Mecánica: Completar huecos eligiendo entre 4 opciones semánticas/gramaticales.
    *   Calidad: Distractores basados en "False Friends" o errores comunes.
    *   Widget: W-TXT-CLOZE (Modo Dropdown).

*   MAT-LINK (Matching / Emparejamiento):
    *   Mecánica: Vincular párrafos con títulos (Reading) o hablantes con ideas (Listening).
    *   Widget: W-MIX-MATCH.

*   DIA-INTERACT (Interacción Dialéctica Asistida por UniversIA):
    *   Mecánica: Simulación de conversación, entrevista oral o mediación evaluada en tiempo real.
    *   Calidad: Evaluación de fluidez, registro léxico, adecuación pragmática y capacidad de reacción.
    *   Widget: W-COMM-DIALOG.
