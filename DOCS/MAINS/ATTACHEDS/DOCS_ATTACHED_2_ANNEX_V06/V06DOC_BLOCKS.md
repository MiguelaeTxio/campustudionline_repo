<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_BLOCKS.md -->
# V06DOC_BLOCKS - CATÁLOGO DE MOTORES DE EVALUACIÓN (V1.1 - REFACTORIZACIÓN UGR)

## 1. BLOQUES DE EVALUACIÓN OBJETIVA Y TÉCNICA\n\n*   **EV-TRA-PRECISION-TECH (Motor de Precisión Terminológica FTI-UGR) [NUEVO 2026]**
    *   **[CERTIFICADO v5.1 — 2026-04-21]** Jerarquía de errores verificada como coherente con la metodología de evaluación de la FTI-UGR (Guía Docente 252113T, aprobada 01/07/2025). El baremo numérico exacto (Categorías A/B/C) no está publicado en la Guía Docente — se entrega al alumnado por PRADO al inicio de curso — pero la estructura categorial A/B/C es el estándar reconocido internacionalmente en la FTI-UGR y coherente con la ISO 17100:2015.
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

*   **RBT-SHORT-LANG (Respuesta Breve Lingüística - UGR/CertAcles) [REFACTORIZADO V5.1]**
    *   **Mecánica:** Validación de precisión léxica y morfología exacta.
    *   **Extensión:** 1-4 palabras (Filtro automático).
    *   **Módulo de Trazos (SUB-LIN-MINOR — Lenguas No Latinas) [AMPLIADO v5.1 - FIDELIDAD 100% UGR]:**
        En el subarquetipo SUB-LIN-MINOR, cuando el `target_language_code` corresponde a una lengua no latina, el motor activa el Módulo de Trazos en colaboración con el widget W-CALLI-PAD. El módulo valida dos dimensiones independientes:
        1.  **Validación de Ductus (Orden y Dirección de Trazos):** El motor verifica que la secuencia de trazos capturada por W-CALLI-PAD se corresponde con el ductus normativo de la lengua objetivo. La referencia normativa aplicada por `target_language_code` es:
            - **Japonés (`ja`):** Norma MEXT (Ministerio de Educación japonés) para el orden de trazos de kana y kanji de uso común (jōyō kanji).
            - **Árabe (`ar`):** Norma de escritura cursiva del árabe estándar moderno (MSA), con validación de la unión correcta de grafemas en posición inicial, medial y final de palabra.
            - **Griego moderno (`el`):** Norma de escritura minúscula del griego moderno estándar, con validación de ligaduras y orden de trazos según la caligrafía escolar griega oficial.
            - **Checo (`cs`):** Validación de los diacríticos especiales (háček, čárka) como parte integral del trazo — la omisión o el posicionamiento erróneo de un diacrítico computa como falta caligráfica.
        2.  **Validación de Integridad Grafémica:** Comparación del carácter resultante con la base de patrones OCR de alta fidelidad (integrado con `gemini-2.5-flash`) para verificar la legibilidad y corrección formal del grafema, independientemente del ductus.
        *   **Baremo de Penalización del Módulo de Trazos:**
            - Ductus erróneo (orden/dirección incorrectos): penalización del **50%** sobre la puntuación del ítem caligráfico.
            - Integridad grafémica comprometida (carácter ilegible o irreconocible): **FAIL_LOGIC: FATAL** para ese ítem (nota 0.0).
            - Diacrítico omitido o mal posicionado (checo): penalización del **50%** sobre el ítem.
        *   **Activación Condicional:** El Módulo de Trazos se activa únicamente en la destreza SD_PHON_GRAPH del subarquetipo SUB-LIN-MINOR con `target_language_code` no latino. Para SUB-LIN-INSTR y para las lenguas latinas de MINOR (alemán, francés, inglés, polaco, portugués), este módulo permanece inactivo y RBT-SHORT-LANG opera en modo estándar de validación léxica.

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
*   **DRA-HOLO-LIT (Rúbrica Analítica Holística — Modo Literario TRA-LIT) [NUEVO v5.1 — 2026-04-21]**
    *   **Ámbito:** SUB-LIN-TRA-LIT exclusivamente. Configuración específica coherente con los criterios de evaluación de la Guía Docente 25211NJ (Literatura y Traducción Lengua B Inglés, FTI-UGR, aprobada 23/06/2025).
    *   **Mecánica:** Evaluación criterial mediante rúbrica de cuatro ejes. Umbral mínimo de superación: 5/10 en la media de los cuatro ejes (coherente con la nota mínima 5 declarada en la Guía Docente 25211NJ).
    *   **Eje 1 — Adecuación al Skopos literario:** La traducción cumple la función estética del texto fuente en la lengua meta. El lector de la traducción experimenta un efecto equivalente al del lector del original. Se evalúa la coherencia entre las decisiones traductoras adoptadas y el Skopos declarado por el alumno en SD_TRA_STYLE.
    *   **Eje 2 — Gestión de culturemas e intertextualidad:** El alumno identifica y resuelve de forma documentada las referencias culturales, intertextos y juegos lingüísticos del original. Las pérdidas inevitables están justificadas y compensadas mediante estrategias traductoras explícitas (domesticación, extranjerización, equivalencia funcional).
    *   **Eje 3 — Calidad literaria de la versión meta:** La traducción funciona como texto literario autónomo en español. Registro literario correcto, puntuación expresiva adecuada al género (poético, teatral, narrativo), sintaxis coherente con las convenciones del género en la lengua meta.
    *   **Eje 4 — Rigor del comentario crítico (SD_TRA_CRIT):** El ensayo justificatorio demuestra dominio de la bibliografía traductológica oficial de la asignatura (Reynolds 2011, Venuti 2017, Skopos). Las citas son correctas y la argumentación es original. Estructura académica rigurosa conforme a los criterios de evaluación de 25211NJ (ensayos de 1500-2000 palabras).
    *   **Activación por fase:**
        *   SD_TRA_STYLE: Ejes 1 y 2 (análisis previo a la transferencia).
        *   SD_TRA_CREATIVE: Ejes 1, 2 y 3 (evaluación de la transferencia estética).
        *   SD_TRA_CRIT: Eje 4 exclusivamente (evaluación del ensayo exegético).
    *   **Nota de distinción:** DRA-HOLO-LIT es una configuración específica de DRA-HOLO para el contexto literario de SUB-LIN-TRA-LIT. No sustituye a DRA-HOLO en ningún otro subarquetipo.

*   BMT-SHIFT (Mediación y Transferencia de Registro):
    *   Mecánica: Adaptación de información técnica a lenguaje divulgativo o viceversa.
    *   Calidad: Evaluación de la fidelidad informativa y adecuación al destinatario.
    *   **Nota de alcance TRA-TECH (SD_TRA_REVIEW) [AUDITADO v5.1 — 2026-04-21]:** SD_TRA_REVIEW NO existe como destreza evaluable autónoma en SUB-LIN-TRA-TECH. La evaluación ordinaria y extraordinaria de la Guía Docente 252113T (FTI-UGR, aprobada 01/07/2025) consiste exclusivamente en traducciones directas cronometradas. En consecuencia, BMT-SHIFT no genera sección de examen autónoma ni actúa como motor principal de ninguna destreza independiente en TRA-TECH. Cualquier referencia a SD_TRA_REVIEW como destreza autónoma de TRA-TECH en versiones anteriores de la constelación queda anulada por esta nota de auditoría.

## 6. MOTORES Y CONFIGURACIONES PARA LA RAMA ARTES Y HUMANIDADES (NUEVO v5.2 — 2026-04-21)

Esta sección define los motores de evaluación y las configuraciones de rúbrica activados bajo los subarquetipos de la Rama Artes y Humanidades.

### EV-ICON-ART (Motor de Identificación y Análisis Iconológico — SUB-HUM-ART-HIST) [NUEVO v5.2 — 2026-04-21]
*   **Ámbito:** SUB-HUM-ART-HIST exclusivamente. Motor asociado a W-ART-IDENT.
*   **Fuente de Certificación:** Metodología de análisis iconográfico e iconológico del Departamento de Historia del Arte UGR, coherente con los criterios de evaluación de las Guías Docentes de Iconografía (26511M2) e Historia de los Estilos e Iconografía (2931114), curso 2025-2026.
*   **Mecánica de Evaluación en Dos Fases:**
    1.  **Fase de Identificación (Campos Fijos — 40% del ítem):** El motor valida los campos del formulario de identificación estructurada contra la base de datos de obras del corpus de la asignatura. Se evalúa la corrección de: Autor/Atribución (exactitud del nombre canónico o justificación de la atribución), Cronología (corrección del período o fecha dentro de la tolerancia definida por el nivel pedagógico), Técnica/Soporte (precisión terminológica según el vocabulario técnico del arte), Estilo/Período/Escuela (adscripción estilística correcta conforme a la historiografía artística). La identificación errónea del autor o la cronología en más de un período estilístico completo activa FAIL_LOGIC: FATAL para la fase de identificación del ítem.
    2.  **Fase de Análisis Iconológico (Editor Libre — 60% del ítem):** El motor evalúa la calidad del comentario en los tres niveles Panofsky mediante rúbrica DRA-HOLO adaptada:
        - **Eje 1 — Descripción Pre-iconográfica:** Precisión y exhaustividad de la descripción formal (composición, figuras, espacios, color, luz). El alumno no puede acceder al nivel iconográfico sin haber completado este eje.
        - **Eje 2 — Análisis Iconográfico:** Correcta identificación de temas, motivos, atributos y fuentes literarias o religiosas. Dominio del repertorio iconográfico del programa (Carmona Muela, Réau, Hall según la bibliografía oficial de la asignatura).
        - **Eje 3 — Interpretación Iconológica:** Capacidad de contextualización histórico-cultural, identificación del programa iconográfico en su conjunto y argumentación sobre el significado intrínseco de la obra. Uso de fuentes secundarias de la historiografía artística.
*   **Rigor Engine:** x1.3 (ITIN_MAI + LVL_B para 3º año) / x1.6 (ITIN_MAI + LVL_C para 4º año).
*   **Criterio de Superación:** Mínimo 5/10 en la media ponderada de las dos fases (40% identificación + 60% análisis). Sin compensación entre fases: la identificación errónea en más de un campo crítico (Autor o Cronología) impide la superación del ítem independientemente de la calidad del análisis.

### EV-MUS-ANAL (Motor de Análisis Musical — SUB-HUM-MUS) [NUEVO v5.2 — 2026-04-21]
*   **Ámbito:** SUB-HUM-MUS exclusivamente. Motor asociado a W-MUS-SCORE y W-AUDIO-INSTR.
*   **Fuente de Certificación:** Criterios de evaluación del Departamento de Historia y Ciencias de la Música UGR, coherentes con las Guías Docentes de Análisis II: Clasicismo y Romanticismo (2991132, aprobada 23/06/2025) y Fundamentos de la Expresión Musical y su Evolución I (2991114, aprobada 25/06/2025). Bibliografía analítica de referencia: LaRue (1989, Análisis del estilo musical), Cook (1991, A guide to musical analysis), Bent (1980, "Analysis" en The New Grove Dictionary).
*   **Mecánica de Evaluación en Dos Destrezas Independientes (50%/50%):**
    1.  **SD_MUS_LIST — Identificación Auditiva (50%):** El motor evalúa la capacidad del alumno para identificar auditivamente período, estilo, forma, género, instrumentación y rasgos estilísticos definitorios de fragmentos musicales. Widget: W-AUDIO-INSTR con configuración MUS (número de reproducciones variable según la estrategia de la asignatura fuente — no fijo en 2). Tipos de ítem: W-OBJ-STRIKE (identificación múltiple), W-TXT-CLOZE (completado de ficha analítica), W-MIX-MATCH (emparejamiento fragmento/período o fragmento/compositor).
    2.  **SD_MUS_SCORE — Análisis en Partitura (50%):** El motor evalúa la calidad del análisis formal, armónico y estilístico realizado sobre la partitura mediante W-MUS-SCORE. Criterios:
        - **Corrección del Análisis Armónico:** Exactitud de los grados romanos, funciones tonales y cadencias identificadas. La confusión de función tonal dominante con subdominante en un contexto cadencial activa penalización severa (-0.5 por error).
        - **Corrección del Análisis Formal:** Exactitud en la identificación y delimitación de secciones formales y su denominación conforme a la terminología canónica (LaRue 1989).
        - **Calidad del Comentario Musicológico:** Rigor en el uso del metalenguaje musicológico (terminología de textura, timbre, ritmo, melodía, armonía, forma), capacidad de relacionar los elementos analizados con el contexto estilístico del período y del compositor.
*   **Rigor Engine:** x1.3 (LVL_B — 3º año) / x1.6 (LVL_C — 4º año).
*   **Criterio de Superación:** Mínimo 5/10 en cada destreza de forma independiente. Sin compensación entre SD_MUS_LIST y SD_MUS_SCORE (FAIL_LOGIC: FATAL por destreza no superada).

### DRA-HOLO configuración ART-CREA (Rúbrica Holística de Proceso Creativo — SUB-HUM-ART-CREA) [NUEVO v5.2 — 2026-04-21]
*   **Ámbito:** SUB-HUM-ART-CREA exclusivamente. Configuración específica de DRA-HOLO para la evaluación del portafolio digital de proceso creativo. Motor asociado a W-PORTFOLIO.
*   **Declaración de Emulación Parcial Certificada [VINCULANTE]:** Esta configuración evalúa exclusivamente las destrezas digitalizables del Grado en Bellas Artes UGR. Las destrezas de taller presencial quedan fuera del alcance de la plataforma.
*   **Fuente de Certificación:** Criterios de evaluación de las Guías Docentes de Arte y Cuerpo (26011D1) y Principios Básicos de la Pintura (2601114) — Facultad de Bellas Artes, UGR, curso 2025-2026.
*   **Mecánica — Rúbrica de Cuatro Ejes:**
    1.  **Eje 1 — Coherencia del Proceso Creativo:** La galería de imágenes evidencia un proceso de investigación y toma de decisiones creativas progresivo y coherente. Los pies de foto documentan adecuadamente cada fase. Se penaliza la ausencia de estados intermedios que evidencien el proceso (obra final sin documentación del proceso: FAIL_LOGIC: FATAL para este eje).
    2.  **Eje 2 — Calidad y Rigor de la Memoria de Proceso:** La memoria demuestra dominio del vocabulario técnico de las artes plásticas (materiales, procedimientos, soportes), coherencia entre la intención artística declarada y el proceso documentado, y fundamentación en referentes artísticos y bibliográficos pertinentes.
    3.  **Eje 3 — Profundidad del Análisis Crítico:** El análisis crítico contextualiza la obra propia dentro de los debates artísticos contemporáneos, demuestra conocimiento de los referentes del programa y argumenta de forma original sobre las decisiones creativas adoptadas.
    4.  **Eje 4 — Corrección Formal de la Documentación Escrita:** La memoria y el análisis crítico están redactados con corrección ortotipográfica y terminológica. La presencia de más de 5 faltas ortográficas en el conjunto de la documentación escrita penaliza el eje en un 50% adicional.
*   **Umbral de Superación:** Mínimo 5/10 en la media de los cuatro ejes. Sin compensación entre ejes: la ausencia de documentación del proceso (Eje 1 nulo) supone el suspenso del subarquetipo independientemente de la calidad de la memoria y el análisis.

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
