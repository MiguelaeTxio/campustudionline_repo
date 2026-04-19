# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_SUBARCHETYPES.md
# V06DOC_SUBARCHETYPES - MATRIZ DE ESPECIALIZACIÓN ACADÉMICA (V2.1 - DETERMINISTA)

Este documento define la **Configuración Estructural Fija** (Receta) que cada Estrategia de Python debe implementar.
**PRINCIPIO:** Python define los Secciones y los Ítems (Widgets). La IA solo rellena el contenido solicitado.

**NOTA DE IMPLEMENTACIÓN:** Cada subarquetipo listado aquí se traduce en una clase `Strategy` que devuelve un esqueleto inmutable.


## 1. RAMA: ARTES Y HUMANIDADES (12 Modelos)
### LENGUAS (CLM / LENGUAS MODERNAS)
*   **SUB-LIN-INSTR: Modelo Instrumental (Acreditación CertAcles / CLM UGR 2026) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR - v5.0]**
    *   **Perfil Institucional y Pedagógico:** Evaluación oficial, legal y vinculante de la competencia comunicativa operativa en los niveles B1 y B2 del Marco Común Europeo de Referencia para las Lenguas (MCERL), bajo el sello CertAcles y la normativa estricta del Centro de Lenguas Modernas (CLM-UGR). El examen es binivel: un mismo instrumento de evaluación permite acreditar el nivel B1 o el B2 en función de la puntuación alcanzada en cada destreza respecto a los puntos de corte establecidos por el Consejo de Europa para cada convocatoria. Tiene reconocimiento en todas las universidades españolas adscritas a la CRUE, en los programas de movilidad Erasmus+ y en más de 250 universidades europeas a través de CERCLES y NULTE.
    *   **Secuencia Genética Obligatoria (Estructura de Cuatro Destrezas - CLM-UGR):**
        *   **NOTA CRÍTICA DE FIDELIDAD:** El examen CertAcles consta de CUATRO destrezas evaluadas de forma independiente: Comprensión de Lectura, Comprensión Auditiva, Expresión e Interacción Escritas y Expresión e Interacción Orales. La Mediación Lingüística NO constituye una destreza independiente en el examen oficial del CLM-UGR; queda reservada como dimensión pedagógica de la plataforma para subarquetipos avanzados de traducción. Su inclusión previa como SD_MEDI queda ANULADA y ELIMINADA de este subarquetipo.
        1. **SD_READ (Comprensión de Lectura — 75 minutos):**
            *   **Estructura Oficial Binivel (CLM-UGR):** 5 textos de diferente tipología (narrativos, descriptivos, de opinión, informativos), distribuidos en 2 textos de nivel B1, 1 texto bisagra con ítems de nivel B1 y B2, y 2 textos de nivel B2. Total aproximado: 40 ítems. Las calificaciones B2, B1 o No Apto se asignan en función de la puntuación total de todos los ítems según el punto de corte de cada convocatoria.
            *   **Tarea A (Ítem de Respuesta Alternativa / Respuesta Múltiple):** El alumno elige una respuesta correcta entre cuatro opciones. Solo una es correcta; las demás son distractores. Evalúa la comprensión global y la inferencia. (Widget: W-OBJ-STRIKE / Motor: MAT-LINK — SIN penalización por respuesta incorrecta).
            *   **Tarea B (Ítem de Reintegración de Fragmento):** El alumno inserta en su ubicación original una palabra o fragmento extraído del texto. Puede haber distractores que no corresponden al texto. Evalúa el dominio de la estructura textual, la coherencia discursiva, el uso de marcadores del discurso y la resolución de anáforas y catáforas. (Widget: W-TXT-CLOZE / Modo: Select / Motor: CLO-MULTI — SIN penalización por respuesta incorrecta).
            *   **Tarea C (Ítem de Relacionar o Emparejar):** El alumno vincula uno a uno los elementos de dos listas formadas por textos cortos o fragmentos con enunciados. Evalúa skimming (captar la idea nuclear de cada párrafo) evitando distractores de repetición superficial de palabras. (Widget: W-MIX-MATCH / Motor: MAT-LINK — SIN penalización por respuesta incorrecta).
            *   **Tarea D (Ítem de Respuesta Corta):** El alumno responde con un máximo de CUATRO palabras. La respuesta se considera errónea si excede de cuatro palabras. No es necesario escribir frases completas. (Widget: W-TXT-CLOZE / Modo: Open / Motor: RBT-SHORT-LANG — SIN penalización por respuesta incorrecta).
            *   **Directriz de Corrección (CLM-UGR):** Las respuestas se registran en hoja de respuestas. No restan las respuestas incorrectas. La superación del nivel B1 o B2 depende de los puntos de corte fijados para la convocatoria, no de un umbral fijo del 60%.
        2. **SD_LIST (Comprensión Auditiva — aproximadamente 45 minutos):**
            *   **Estructura Oficial Binivel (CLM-UGR):** 5 textos grabados de diferente tipología (narrativos, descriptivos, de opinión, biográficos, de conversación; en registro formal, informal o académico), distribuidos en 2 grabaciones de nivel B1, 1 grabación bisagra con ítems de nivel B1 y B2, y 2 grabaciones de nivel B2. Total aproximado: 40 ítems. Cada grabación se escucha exactamente DOS veces.
            *   **Tarea A (Ítem de Respuesta Alternativa / Respuesta Múltiple):** El alumno elige una respuesta correcta entre cuatro opciones. Evalúa la captación de la intención comunicativa, el tono y el registro sociolingüístico de diálogos situacionales y monólogos. (Widget: W-OBJ-STRIKE / Motor: MAT-LINK — SIN penalización por respuesta incorrecta).
            *   **Tarea B (Ítem de Relacionar o Emparejar):** El alumno relaciona enunciados con las distintas partes de la audición. Evalúa la discriminación fonética y la extracción de datos específicos en tiempo real. (Widget: W-MIX-MATCH / Motor: MAT-LINK — SIN penalización por respuesta incorrecta).
            *   **Tarea C (Ítem de Respuesta Corta):** El alumno responde con un máximo de CUATRO palabras. Evalúa la toma de notas académicas y la extracción de información fáctica unívoca de monólogos, entrevistas extensas o fragmentos de conferencia. (Widget: W-TXT-CLOZE / Modo: Open / Motor: RBT-SHORT-LANG — Validación de precisión léxica con Fuzzy Matching de tolerancia mínima — SIN penalización por respuesta incorrecta).
            *   **Restricción de Audio (CLM-UGR — Bloqueo Hermético):** El widget W-AUDIO-INSTR implementa bloqueo hermético del botón "Play" tras la segunda reproducción completa de cada pista. La barra de progreso es meramente informativa: se deshabilita el adelantado y retroceso del audio (Non-Scrubbing) para garantizar la audición lineal obligatoria. El sistema registra el timestamp de cada reproducción y persiste el contador en base de datos para sobrevivir a refresco de página.
        3. **SD_WRIT (Expresión e Interacción Escritas — 60 minutos):**
            *   **Estructura Oficial Binivel (CLM-UGR):** 2 tareas de escritura de distinta tipología. El alumno debe intentar ambas independientemente del nivel que quiera acreditar.
            *   **Tarea 1 — Nivel B1 (Interacción Funcional Transaccional):** Producción de una respuesta escrita (carta, email informal/neutro, narración, artículo, blog o informe) a partir de un estímulo previo. Extensión obligatoria: **200-250 palabras**. El alumno debe cubrir obligatoriamente todos los puntos de control informativos especificados en el encargo. (Widget: W-HUM-TEXT / Rúbrica: DRA-HOLO — Criterios: Cumplimiento de la tarea, Coherencia y Cohesión, Competencia lingüística general, Corrección gramatical, Dominio y riqueza de vocabulario).
            *   **Tarea 2 — Nivel B2 (Producción Académica / Ensayo Argumentativo):** Producción de un texto de mayor complejidad (carta, email formal/neutro, artículo, informe, ensayo, narración o reseña). Extensión obligatoria: **250-300 palabras**. Se exige registro formal cuando el nivel objetivo es B2. (Widget: W-HUM-TEXT / Rúbrica: DRA-HOLO — Mismos cinco criterios con mayor exigencia en corrección gramatical y riqueza léxica).
            *   **Directriz de Multimodalidad (Miguel Ángel):** El selector de entrada DEBE habilitar obligatoriamente el modo **OCR/Captura** (widget W-OCR-PRO). Esta funcionalidad permite al alumno realizar la producción escrita en papel físico —emulando el protocolo de examen presencial tradicional del CLM-UGR, donde se usa bolígrafo obligatoriamente— y digitalizar el manuscrito mediante la cámara del dispositivo. El sistema procesa la imagen para auditar la corrección gramatical, la adecuación al registro y el cumplimiento de la extensión léxica.
            *   **Baremo de Penalización Formal (FORM_PEN — CLM-UGR):** Se aplican descuentos automáticos sobre la nota bruta: -0.1 puntos por cada falta de ortografía y -0.05 puntos por cada error ortotipográfico (tildes, puntuación). El umbral de exclusión se fija en más de 5 faltas de ortografía en una sola tarea, lo que conlleva anulación inmediata de la tarea (Nota: 0.0 — FAIL_LOGIC: FATAL en esa tarea).
        4. **SD_SPEAK (Expresión e Interacción Orales — 10 minutos):**
            *   **Estructura Oficial (CLM-UGR):** Entrevista individual de aproximadamente 10 minutos con un examinador del CLM, licenciado y nativo. Consta de tres partes secuenciales:
            *   **Fase 1 — Preguntas sobre Vida Cotidiana (Nivel B1):** Interacción oral sobre la familia, la casa, el tiempo libre, los estudios y el trabajo. Evalúa la fluidez básica, el alcance léxico para temas cotidianos y la capacidad de desenvolverse en situaciones familiares. (Widget: W-COMM-DIALOG / Motor: DIA-INTERACT).
            *   **Fase 2 — Descripción y Análisis de Fotografía (Niveles B1/B2):** El alumno describe, compara y analiza críticamente una fotografía o imagen aportada por el examinador (educación, trabajo, lugares, vacaciones, deporte, ocio, comida). Evalúa el alcance descriptivo, la capacidad de argumentación y la adecuación del registro al nivel. (Widget: W-COMM-DIALOG / Motor: DIA-INTERACT).
            *   **Fase 3 — Opinión sobre Tema Propuesto (Niveles B1/B2):** El alumno expone y defiende su opinión sobre un tema concreto facilitado por el examinador (educación, trabajo, vacaciones, deporte, ocio, salud, tecnología). El examinador puede plantear preguntas de apoyo. Evalúa la fluidez sostenida, la capacidad de argumentación, la corrección gramatical y la adecuación pragmática al registro. (Widget: W-COMM-DIALOG / Motor: DIA-INTERACT).
            *   **Criterios de Evaluación (CLM-UGR):** Alcance de la gramática y el vocabulario, Corrección de la gramática y el vocabulario, Fluidez, Coherencia y cohesión.
            *   **Nota sobre UniversIA:** En la plataforma, el rol del examinador humano es emulado por el asistente UniversIA a través del widget W-COMM-DIALOG. La Fase 3 evalúa la opinión del alumno sobre un tema, no una negociación dialéctica. La interacción debe ser natural y abierta, sin forzar dinámicas de conflicto o toma de decisiones compartida que no corresponden al formato oficial.
    *   **Protocolo de Superación y Calificación (Sistema Oficial CLM-UGR 2026):**
        *   **Mecanismo de Puntos de Corte (Binivel):** La acreditación del nivel B1 o B2 en cada destreza depende de los puntos de corte fijados para cada convocatoria siguiendo las pautas del Consejo de Europa, con el fin de ajustar los exámenes al MCERL. No existe un umbral fijo del 60% universal: los puntos de corte son variables y se establecen mediante análisis estadístico de la distribución de respuestas de cada convocatoria.
        *   **Obligatoriedad de Superación por Destreza:** Para obtener el nivel global de dominio B1 o B2, el alumno debe alcanzar ese nivel en las CUATRO destrezas evaluadas de forma independiente. La compensación entre destrezas no está permitida.
        *   **Gestión del Fallo Parcial (Convocatorias Sucesivas):** Si el alumno supera el examen completo pero no alcanza el nivel en una única destreza, podrá examinarse de esa única destreza en una de las próximas convocatorias en un plazo máximo de un año. Esta posibilidad está limitada a una sola destreza pendiente; si son dos o más, debe repetir el examen completo.
        *   **Navegación de Seguridad (Non-Backtracking):** El flujo de examen es Unidireccional Sellado. Una vez completada y enviada una destreza, el acceso a la misma queda bloqueado permanentemente para garantizar la validez del dominio lingüístico demostrado en tiempo real.

*   **SUB-LIN-MINOR: Modelo Minor / Iniciación (UGR - Facultad Filosofía y Letras) [REFACTORIZADO V4.2 - FIDELIDAD 100% UGR]**
    *   **Perfil Institucional:** Iniciación a la competencia lingüística, caligráfica y sociocultural (Alemán, Árabe, Chino, Japonés, Ruso, etc.) según las Guías Docentes de la UGR.
    *   **Secuencia Genética Obligatoria (5 Fases Subatómicas):**
        1. **SD_PHON_GRAPH (Grafía y Fonética):**
            - Tarea 1: Dictado de signos/caracteres y transcripción a sistema vehicular (Pinyin/Romaji/Transliteración).
            - Tarea 2: Identificación de fonemas mediante discriminación auditiva.
            - **Widget:** W-TXT-CLOZE (Modo Open con Pad de Trazos/OCR). **Bloqueo de teclado occidental obligatorio para lenguas no latinas.**
        2. **SD_MORPH_BASE (Morfosintaxis y Estructura Elemental):**
            - Tarea: Construcción de enunciados simples y morfología básica (declinación/conjugación inicial).
            - **Motor:** CLO-MULTI y PRM-STRIKE.
        3. **SD_LEX_COMM (Léxico y Función Comunicativa):**
            - Tarea: Emparejamiento de actos de habla (saludos, presentaciones) con contextos reales.
            - **Widget:** W-MIX-MATCH.
        4. **SD_READ_ADAP (Comprensión Lectora Adaptada):**
            - Tarea: Extracción de información específica en señalética real, menús y anuncios breves.
            - **Layout:** SPLIT_TEXT (Panel lateral con estímulo visual real).
        5. **SD_CULT_INTEGRITY (Competencia Intercultural y Contexto):**
            - Tarea: Validación de protocolos de cortesía, geografía política y realidades culturales nucleares de la UGR.
            - **Rigor:** LVL_A. Inmersión vehicular (Castellano) obligatoria en instrucciones.
    *   **Regla de Oro UGR (CertAcles):** Umbral del 60% por destreza. Sin compensación (FAIL_LOGIC: FATAL).

*   **SUB-LIN-PHILO: Modelo Filológico / Crítica Textual (UGR - Facultad de Filosofía y Letras) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR]**
    *   **Perfil Institucional:** Análisis científico, histórico y ecdótico de la lengua española y sus monumentos literarios. Basado en los criterios de evaluación del Departamento de Lengua Española y el Departamento de Filologías Clásicas de la UGR.
    *   **Secuencia Genética Obligatoria (Cuatri-Destreza Científica):**
        1. **SD_PHONO (Fonética y Fonología Histórica):**
            - **Objetivo:** Reconstrucción de la cadena evolutiva desde el étimo latino (u origen) hasta el romance medieval o moderno.
            - **Tarea:** Identificación de procesos de cambio (apócope, síncopa, metátesis, lenición, palatalización) y transcripción mediante el Alfabeto Fonético Internacional.
            - **Widget:** W-PHILO-IPA (Pad Fonético especializado).
            - **Motor:** EV-DIAC-VAL (Validación de pasos intermedios. Cada salto fonético debe estar justificado).
        2. **SD_MORPH_DIAC (Morfología Diacrónica):**
            - **Objetivo:** Análisis de la evolución de los paradigmas flexivos nominales y verbales.
            - **Tarea:** Explicación de la reestructuración del sistema de casos latinos al sistema preposicional romance, creación de tiempos compuestos y evolución de los clíticos.
            - **Rigor:** Nivel Catedrático (UGR). Se exige identificar la ley de analogía o nivelación morfológica aplicada.
        3. **SD_LEX_SEM (Lexicología y Semántica Histórica):**
            - **Objetivo:** Estudio del origen y evolución del léxico (Etimología).
            - **Tarea:** Análisis de cultismos, semicultismos y palabras patrimoniales. Identificación de cambios semánticos (metáfora, metonimia, elipsis).
            - **Fuente de Autoridad:** Uso emulado de los criterios del DCECH (Corominas y Pascual) y el CORDE/CDH.
        4. **SD_TEXT_CRIT (Crítica Textual / Ecdótica):**
            - **Objetivo:** Establecimiento de la edición crítica de un texto medieval o clásico.
            - **Tarea:** Ejecución de las fases neolachmannianas (Metodología Alberto Blecua): Recensio (inventario), Collatio (cotejo de variantes), Examinatio (juicio crítico) y Selectio/Emendatio (propuesta de fijación).
            - **Widget:** W-PHILO-ECDO (Interfaz SPLIT_TEXT para colación de manuscritos).
            - **Motor:** EV-PALE (Validación de normas de transcripción paleográfica vs. crítica).
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        - **Umbral Crítico:** 70% de precisión técnica mínima.
        - **Política de Tolerancia Cero:** La presencia de una sola falta de ortografía técnica (tildes, grafemas medievales) en el Nivel C o la confusión de leyes fonéticas incompatibles supone la anulación inmediata del ítem (FAIL_LOGIC: FATAL).
        - **Prohibición de Paráfrasis:** Se exige el uso estricto del metalenguaje filológico oficial de la UGR.
    *   **Rigor Engine:** x1.8 (Nivel C1/C2 - Epistemológico).

*   **SUB-LIN-NORM: Modelo Norma y Uso (UGR / Grado en Filología Hispánica) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR]**
    *   **Perfil Institucional:** Evaluación avanzada de la competencia normativa, prescriptiva y descriptiva del español contemporáneo bajo los estándares del Departamento de Lengua Española de la Universidad de Granada (UGR). El modelo evalúa la capacidad científica del alumno para discernir entre la norma panhispánica culta y los fenómenos de variación lingüística, utilizando como herramientas la gramática académica y el análisis de corpus.
    *   **Secuencia Genética Obligatoria (Cuatri-Destreza Normativa):**
        1. **SD_CORPUS_ANALYSIS (Investigación y Validación Empírica):**
            - **Objetivo:** Capacitar al alumno en la validación de usos lingüísticos basándose en datos reales de frecuencia y prestigio.
            - **Tarea:** Investigación emulada en CORPES XXI para determinar la aceptabilidad de construcciones en conflicto (ej. pluralización de "haber" impersonal, uso de "detrás mío" vs. "detrás de mí", o el uso del infinitivo fático). El alumno debe interpretar mapas geográficos y frecuencias por registro.
            - **Widget:** W-LAW-NAV (Configurado como Navegador de Corpus Lingüístico).
            - **Motor:** EV-NORM-ANALYSIS (Valida la interpretación científica del uso frente a la prescripción).
        2. **SD_MORPH_ANTINORM (Diagnóstico de Desviaciones Morfosintácticas):**
            - **Objetivo:** Detección y corrección razonada de infracciones gramaticales en el registro culto.
            - **Tarea:** Identificación técnica de fenómenos como queísmo, dequeísmo, leísmo (de persona y de cosa), laísmo, loísmo y discordancias en el orden de los clíticos o en oraciones de pasiva refleja e impersonal.
            - **Widget:** W-OBJ-STRIKE y W-TXT-CLOZE (Modo Input).
            - **Motor:** RBT-CANON (Exigencia de precisión absoluta en la nomenclatura del fenómeno).
        3. **SD_ORTHO_PRESCRIPTIVE (Ortografía y Ortotipografía Académica):**
            - **Objetivo:** Aplicación rigurosa de la normativa de la RAE/ASALE (2010) y normas de edición técnica.
            - **Tarea:** Edición de textos que presentan dificultades en el uso de mayúsculas diacríticas, puntuación compleja (posicionamiento de signos respecto a comillas y notas al pie), acentuación de compuestos y gestión de extranjerismos y neologismos.
            - **Widget:** W-HUM-TEXT (Entorno de edición crítica).
            - **Rigor:** x1.7 (Penalización severa por desviaciones de la OLE 2010).
        4. **SD_CRITICAL_NORM (Comentario Crítico y Justificación Bibliográfica):**
            - **Objetivo:** Defensa argumentada de la corrección lingüística basándose en obras de referencia oficiales.
            - **Tarea:** Redacción de una justificación académica para la propuesta de mejora de un texto inadecuado, citando explícitamente la Nueva Gramática (NGLE) o el Diccionario Panhispánico de Dudas (DPD). Evaluación de la adecuación del registro al contexto (jurídico, administrativo, académico).
            - **Layout:** SPLIT_TEXT (Panel lateral persistente con el texto fuente).
            - **Motor:** DRA-HOLO (Rúbrica analítica holística de la UGR para Norma y Uso).
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        - **Umbral Crítico:** Mínimo 75% de precisión técnica.
        - **Política de Tolerancia Cero:** El error en la identificación técnica de un fenómeno (ej. confundir un queísmo con una falta de régimen) o la cita falsa de una obra de referencia supone el suspenso automático del ítem (FAIL_LOGIC: FATAL).
        - **Rigor Engine:** x1.7 (Nivel C1/C2 - Normativo).

*   **SUB-LIN-TRA-TECH: Modelo de Traducción Profesional y Técnica (FTI UGR) [REFACTORIZADO 2026]**
    *   **Perfil Institucional:** Evaluación de la competencia traductora especializada (Científico-Técnica, Jurídico-Económica) bajo el enfoque del Skopos y la ISO 17100.
    *   **Secuencia Genética Obligatoria (Fidelidad 100%):**
        1.  **SD_TRA_ANALYSIS (Análisis del Encargo):** Identificación de la función textual, el destinatario y los problemas potenciales del texto (neologismos, ambigüedades sintácticas) antes de la traducción.
        2.  **SD_TERM_RESEARCH (Fase Documental):** Creación de un glosario técnico bilingüe basado en fuentes de autoridad (IATE, UNTERM). Validación de equivalencias terminológicas unívocas.
        3.  **SD_TRA_DRAFT (Traducción Directa):** Traducción de dos textos fuente de 350 palabras cada uno. Se evalúa la precisión léxica, el cumplimiento del registro y la adecuación al género textual.
        4.  **SD_TRA_REVIEW (Control de Calidad y Post-edición):** Revisión de estilo y coherencia. Incluye la post-edición de un output de Traducción Automática (TA) para detectar alucinaciones y errores de cohesión.
    *   **Protocolo de Superación:** Umbral mínimo del 50% en cada sección de traducción de forma independiente. Sin compensación (FAIL_LOGIC: FATAL).
*   **SUB-LIN-TRA-LIT: Modelo de Traducción Literaria y Editorial (FTI UGR) [REFACTORIZADO QUIRÚRGICO]**
    *   **Perfil:** Traducción de textos creativos, poéticos y humanísticos basada en los criterios de la FTI (UGR).
    *   **Secuencia Genética Obligatoria (3 Fases):**
        1. **SD_TRA_STYLE (Análisis Estilístico Comparado):** Identificación de la voz del autor, rasgos dialectales/cronoflectales y desafíos retóricos. (Widget: W-HUM-TEXT).
        2. **SD_TRA_CREATIVE (Transferencia Estética):** Recreación del efecto estético y literario en la lengua meta (Skopos). Gestión de culturemas e intertextualidad. (Widget: W-TRA-LIT-CREA).
        3. **SD_TRA_CRIT (Crítica y Justificación):** Comentario exegético defendiendo las opciones de traducción y compensaciones literarias. (Widget: W-HUM-TEXT).
    *   **Rigor:** Hermenéutico / Nivel C2 (LVL_C).
    *   **Motor Principal:** DRA-HOLO (Rúbrica de Calidad Literaria UGR).

### HUMANIDADES
*   **SUB-HUM-HIST:** (Modelo Historiográfico). Análisis de fuentes primarias y cronología.
*   **SUB-HUM-PHIL:** (Modelo Dialéctico). Lógica formal, ética y ensayo crítico.
*   **SUB-HUM-ART-HIST:** (Modelo Iconográfico). Análisis formal y contextual de la obra.
*   **SUB-HUM-ART-CREA:** (Modelo Bellas Artes). Portafolio, técnica matérica y discurso visual.
*   **SUB-HUM-MUS:** (Modelo Musicología). Análisis armónico, formas y transcripción.
*   **SUB-HUM-ANTH:** (Modelo Antropológico). Etnografía y estructuras culturales.

## 2. RAMA: CIENCIAS DE LA SALUD (10 Modelos)
*   **SUB-SAN-MED-CLIN:** (Medicina). Diagnóstico diferencial y razonamiento clínico.
*   **SUB-SAN-MED-BASIC:** (Básicas Médicas). Anatomía, Histología y Fisiología (Identificación).
*   **SUB-SAN-ODON:** (Odontología). Materiales, radiología y técnica dental.
*   **SUB-SAN-FISIO:** (Fisioterapia). Valoración funcional y anatomía palpatoria.
*   **SUB-SAN-CUID:** (Enfermería). Planes NANDA/NIC/NOC y seguridad del paciente.
*   **SUB-SAN-LAB:** (Bioquímica/Farmacia). Balances químicos, laboratorio y farmacología.
*   **SUB-SAN-PSY-CLIN:** (Psicología). Diagnóstico DSM/CIE y evaluación conductual.
*   **SUB-SAN-PSY-EXP:** (Psicología Exp). Metodología, estadística y diseños de investigación.
*   **SUB-SAN-VET:** (Veterinaria). Clínica animal y cirugía veterinaria.
*   **SUB-SAN-NUT:** (Nutrición). Dietética, bromatología y salud pública.

## 3. RAMA: CIENCIAS SOCIALES Y JURÍDICAS (10 Modelos)
*   **SUB-SOC-LAW-PROC:** (Derecho Procesal). Plazos, trámites y técnica procesal.
*   **SUB-SOC-LAW-DICT:** (Derecho Civil/Penal). Dictamen basado en hechos y jurisprudencia.
*   **SUB-SOC-ECON-QUAN:** (Economía). Contabilidad, econometría y micro/macro avanzada.
*   **SUB-SOC-ECON-MGMT:** (Empresa). Estrategia, marketing y organización.
*   **SUB-SOC-EDU-KIDS:** (Magisterio). Diseño de situaciones de aprendizaje y DUA.
*   **SUB-SOC-EDU-SEC:** (Profesorado). Didáctica específica y normativa educativa.
*   **SUB-SOC-COMM-JOUR:** (Periodismo). Redacción, ética y análisis de medios.
*   **SUB-SOC-COMM-AV:** (Audiovisual). Guion, técnica de cámara y postproducción.
*   **SUB-SOC-GEOG:** (Geografía). Análisis territorial, SIG y climatología.
*   **SUB-SOC-WORK:** (Trabajo Social). Intervención social, políticas y mediación comunitaria.

## 4. RAMA: INGENIERÍA Y ARQUITECTURA (7 Modelos)
*   **SUB-TEC-SOFT:** (Informática). Algoritmia, estructuras y arquitectura software.
*   **SUB-TEC-CIVIL:** (Caminos). Cálculo de estructuras y normativa (CTE).
*   **SUB-TEC-INDUS:** (Industrial). Termodinámica, máquinas e industrias.
*   **SUB-TEC-CHEM:** (Ing. Química). Reactores y balances de materia.
*   **SUB-TEC-PROJ:** (Arquitectura). Proyecto arquitectónico y análisis urbano.
*   **SUB-TEC-CONS:** (Edificación). Técnica constructiva y gestión de obra.
*   **SUB-TEC-PURE:** (Física/Mates). Rigor deductivo formal y demostración.

## 5. RAMA: CIENCIAS (6 Modelos)
*   **SUB-SCI-BIO:** (Biología). Taxonomía, ecología y genética.
*   **SUB-SCI-CHEM:** (Química). Síntesis, inorgánica y orgánica pura.
*   **SUB-SCI-PHYS:** (Física). Mecánica cuántica y electromagnetismo.
*   **SUB-SCI-GEOL:** (Geología). Mineralogía, estratigrafía y cartografía.
*   **SUB-SCI-ENV:** (Ambientales). Gestión de residuos y contaminación.
*   **SUB-SCI-DATA:** (Ciencia de Datos). IA, Big Data y estadística computacional.
