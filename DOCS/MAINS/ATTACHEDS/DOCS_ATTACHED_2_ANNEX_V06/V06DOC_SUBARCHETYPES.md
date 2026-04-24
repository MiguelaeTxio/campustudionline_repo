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

*   **SUB-LIN-MINOR: Modelo Minor / Iniciación (UGR - Facultad Filosofía y Letras — Grado en Lenguas Modernas y sus Literaturas) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR - v5.1]**
    *   **Perfil Institucional:** Iniciación a la competencia lingüística, caligráfica y sociocultural en la lengua minor del Grado en Lenguas Modernas y sus Literaturas (Facultad de Filosofía y Letras, UGR). Las lenguas minor ofertadas en el plan de estudios vigente (BOE 02/12/2024) son: **alemán, árabe, checo, francés, griego moderno, inglés, japonés, polaco y portugués**. El plan de estudios contempla además la posibilidad de ampliar la oferta con otras lenguas que la UGR pueda ofertar con posterioridad. La competencia caligráfica es exigencia institucional explícita del título para todas las lenguas minor no latinas (árabe, checo, griego moderno, japonés), conforme a las competencias específicas 31 del Verifica del Grado. El modelo evalúa los tres niveles curriculares del Minor: inicial, intermedio y avanzado (36 ECTS de lengua + 12 ECTS de literatura).
    *   **NOTA CRÍTICA DE DISTINCIÓN INSTITUCIONAL:** El subarquetipo SUB-LIN-MINOR corresponde al itinerario curricular del Grado en Lenguas Modernas (segunda lengua del título), cuyo marco de evaluación es el rendimiento académico en asignaturas regladas. Este marco es distinto al de SUB-LIN-INSTR (acreditación oficial CertAcles del CLM-UGR). El mecanismo de superación de MINOR no es un umbral fijo del 60% ni el sistema de puntos de corte CertAcles: la superación se rige por la normativa académica general de la UGR (calificación mínima de 5 sobre 10 en cada asignatura del bloque Minor).
    *   **Secuencia Genética Obligatoria (5 Fases Subatómicas):**
        1. **SD_PHON_GRAPH (Grafía y Fonética):**
            - Tarea 1: Dictado de signos/caracteres y transcripción a sistema vehicular (Pinyin/Romaji/Transliteración árabe/Romanización del griego moderno según norma ISO 843).
            - Tarea 2: Identificación de fonemas mediante discriminación auditiva.
            - **Widget:** W-TXT-CLOZE (Modo Open con Pad de Trazos/OCR). **Bloqueo de teclado occidental obligatorio para lenguas no latinas (árabe, checo con diacríticos especiales, griego moderno, japonés).**
            - **Widget Especializado:** W-CALLI-PAD (Pad Caligráfico para lenguas no latinas — ver V06DOC_WIDGETS.md sección 7).
        2. **SD_MORPH_BASE (Morfosintaxis y Estructura Elemental):**
            - Tarea: Construcción de enunciados simples y morfología básica (declinación/conjugación inicial, partículas gramaticales, sistema de casos en alemán/checo/japonés).
            - **Motor:** CLO-MULTI y PRM-STRIKE.
        3. **SD_LEX_COMM (Léxico y Función Comunicativa):**
            - Tarea: Emparejamiento de actos de habla (saludos, presentaciones, situaciones cotidianas) con contextos reales de la cultura de la lengua minor.
            - **Widget:** W-MIX-MATCH.
        4. **SD_READ_ADAP (Comprensión Lectora Adaptada):**
            - Tarea: Extracción de información específica en textos auténticos breves (señalética real, menús, anuncios, titulares de prensa adaptados al nivel inicial/intermedio de la lengua minor).
            - **Layout:** SPLIT_TEXT (Panel lateral con estímulo visual real).
        5. **SD_CULT_INTEGRITY (Competencia Intercultural y Contexto):**
            - Tarea: Validación de protocolos de cortesía, geografía política y realidades culturales nucleares de la comunidad lingüística de la lengua minor, conforme a los contenidos de las Guías Docentes de la UGR para esta asignatura.
            - **Rigor:** LVL_A (nivel inicial) / LVL_B (niveles intermedio y avanzado). Inmersión vehicular (Castellano) obligatoria en instrucciones del nivel inicial.
    *   **Protocolo de Superación (Marco Académico UGR — Grado en Lenguas Modernas):**
        - **Mecanismo:** Calificación mínima de 5 sobre 10 en la evaluación de cada fase subatómica, conforme a la normativa académica general de la UGR. No aplica el sistema de puntos de corte CertAcles ni el umbral del 60% por destreza (marcos propios de SUB-LIN-INSTR).
        - **Política de Tolerancia:** Se permite la paráfrasis si el concepto es correcto (ITIN_MIN). Los errores caligráficos en lenguas no latinas penalizan el ítem en un 50% (validación de ductus por motor RBT-SHORT-LANG con módulo de trazos activo).
        - **FAIL_LOGIC:** PARTIAL (penalización proporcional al error, salvo en SD_PHON_GRAPH para lenguas no latinas donde el ductus erróneo es FATAL para el ítem caligráfico).

*   **SUB-LIN-PHILO: Modelo Filológico / Lingüística Histórica (UGR - Grado en Filología Hispánica — Dpto. de Lengua Española) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR - v5.1]**
    *   **Perfil Institucional:** Análisis científico e histórico de la lengua española desde sus orígenes latinos hasta la actualidad, basado en los criterios de evaluación del Departamento de Lengua Española de la UGR. Las asignaturas fuente son: Fonética y Fonología del Español (2831113, 1º Troncal), Historia de la Lengua Española I (2831141, 4º Obligatoria) e Historia de la Lengua Española II (2831145, 4º Obligatoria), complementadas por Historia del Léxico Español (28311A5, 4º Optativa). La Crítica Textual / Ecdótica se evalúa en el subarquetipo independiente SUB-LIN-ECDO (Dpto. de Literatura Española).
    *   **NOTA CRÍTICA DE FIDELIDAD (v5.1):** Este subarquetipo evalúa exclusivamente las destrezas de lingüística histórica interna (fonética, morfosintaxis y léxico diacrónico) del Dpto. de Lengua Española. La Ecdótica y la Crítica Textual quedan fuera de su ámbito y se evalúan en SUB-LIN-ECDO. La estructura pasa de Cuatri-Destreza a **Tri-Destreza Científica**.
    *   **Secuencia Genética Obligatoria (Tri-Destreza Científica — Dpto. Lengua Española UGR):**
        1. **SD_PHONO (Fonética y Fonología Histórica):**
            - **Objetivo:** Dominio del sistema fonológico del español como disciplina científica (base sincrónica, Fonética y Fonología 2831113) y reconstrucción de la cadena evolutiva desde el étimo latino hasta el romance medieval y moderno (aplicación diacrónica, Historia de la Lengua I 2831141).
            - **Tarea A (Sincrónica):** Identificación y transcripción de fonemas, alófonos, variantes y fenómenos del sistema fonológico actual (vocales, consonantes, sílaba, acento, entonación). Contraste norma/uso. Widget: W-PHILO-IPA (Pad Fonético especializado con bloque de transcripción AFI).
            - **Tarea B (Diacrónica):** Identificación de procesos de cambio fonético (apócope, síncopa, metátesis, lenición, palatalización, sonorización, vocalización) y reconstrucción de estadios evolutivos intermedios. Cada salto fonético debe estar justificado mediante la ley correspondiente. Widget: W-PHILO-IPA. Motor: EV-DIAC-VAL (CHRONO_STRICT activo — YOD_IDENTIFICATION obligatorio).
            - **Fuentes de Autoridad:** Lapesa (1981), Lloyd (1993), Penny (2014), Hualde (2014).
        2. **SD_MORPH_DIAC (Morfología Diacrónica):**
            - **Objetivo:** Análisis de la evolución de los paradigmas flexivos nominales y verbales del español, desde el latín hasta la actualidad (Historia de la Lengua II 2831145, Tema: Morfología histórica nominal y verbal).
            - **Tarea:** Explicación de la reestructuración del sistema de casos latinos al sistema preposicional romance; evolución de los paradigmas pronominales y de los clíticos; creación de los tiempos compuestos; morfología verbal histórica. Se exige identificar la ley de analogía o nivelación morfológica aplicada en cada caso.
            - **Rigor:** Nivel Catedrático (UGR). Motor: EV-DIAC-VAL.
            - **Fuentes de Autoridad:** Alvar/Pottier (1993), Penny (2014), Azofra (2009), Company Company (2014).
        3. **SD_LEX_SEM (Lexicología y Semántica Histórica):**
            - **Objetivo:** Estudio científico del origen y evolución del léxico español desde sus raíces latinas y su contacto con otras lenguas (Historia del Léxico Español 28311A5; Historia de la Lengua II, Tema 7: Lexicología y Semántica históricas).
            - **Tarea:** Análisis de cultismos, semicultismos y palabras patrimoniales (dobletes léxicos). Identificación de los mecanismos de formación de palabras (prefijación, sufijación, composición) en perspectiva histórica. Identificación de cambios semánticos (metáfora, metonimia, elipsis, especialización, generalización). Validación etimológica mediante los recursos de autoridad.
            - **Fuentes de Autoridad:** DCECH (Corominas y Pascual, 1980-1991), CORDE/CDH (RAE), NTLLE (RAE), Dworkin (A History of the Spanish Lexicon, 2012).
            - **Motor:** RBT-CANON (Exigencia de precisión absoluta en la nomenclatura técnica; no se admite paráfrasis en LVL_C).
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        - **Umbral Crítico:** 70% de precisión técnica mínima por destreza. Sin compensación entre destrezas (FAIL_LOGIC: FATAL por destreza si no se alcanza el umbral).
        - **Política de Tolerancia Cero:** La confusión de leyes fonéticas incompatibles, la identificación errónea del tipo de Yod (I/II/III/IV) o el error en la nomenclatura técnica morfológica o lexicológica en Nivel C supone la anulación inmediata del ítem (FAIL_LOGIC: FATAL para ese ítem).
        - **Prohibición de Paráfrasis:** Se exige el uso estricto del metalenguaje filológico oficial de la UGR en las tres destrezas.
    *   **Rigor Engine:** x1.8 (Nivel C1/C2 - Epistemológico).

*   **SUB-LIN-ECDO: Modelo de Edición y Crítica Textual (UGR - Grado en Filología Hispánica — Dpto. de Lengua Española) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR - v5.1]**
    *   **Perfil Institucional:** Evaluación de las competencias de edición, corrección y crítica textual aplicadas al español, bajo los criterios de la asignatura **La Industria Editorial: Edición, Corrección, Anotación y Evaluación de Textos Españoles (28311A9)** — 4º curso, 1er semestre, Optativa — del Departamento de Lengua Española de la UGR (Guía Docente aprobada 18/06/2025). Este subarquetipo se desmembró de SUB-LIN-PHILO en v5.1 para garantizar la adscripción disciplinar correcta de cada dominio. La competencia CE10 ("Conocer las técnicas y métodos de la crítica textual y de la edición de textos, aplicados a la literatura escrita en español") actúa como competencia transversal de contexto. La metodología de referencia para la dimensión crítico-textual es Blecua (2004, Manual de crítica textual, Castalia), citado en la bibliografía complementaria oficial de 28311A9.
    *   **NOTA DE DISTINCIÓN DISCIPLINAR:** Este subarquetipo no evalúa la Ecdótica neolachmanniana como eje metodológico central (dominio de investigación de Máster/Doctorado), sino la competencia práctica del filólogo como editor, corrector y evaluador de textos en el sentido de la asignatura 28311A9. La Ecdótica de Blecua se incorpora como componente de la destreza SD_ANNOT (anotación crítica), donde el alumno debe identificar y resolver problemas de transmisión textual en un contexto de edición profesional.
    *   **Secuencia Genética Obligatoria (Cuatri-Destreza Editorial — Dpto. Lengua Española UGR 2025-2026):**
        1. **SD_ORTOTYPO (Corrección Ortotipográfica):**
            - **Objetivo:** Aplicación rigurosa de las normas ortotipográficas del español (OLE 2010 / RAE-ASALE) a un texto que va a ser editado (Temas 3-4 de 28311A9: corrección de primeras pruebas y ortotipografía).
            - **Tarea:** El alumno recibe un texto con errores ortotipográficos (uso de mayúsculas, puntuación compleja, comillas, rayas, paréntesis, guiones, numerales, siglas, abreviaturas, extranjerismos) y debe marcarlos, clasificarlos y corregirlos siguiendo la OLE 2010 y las convenciones editoriales del español.
            - **Widget:** W-HUM-TEXT (Modo Revisión y Control de Cambios — marca visualmente inserciones, supresiones y sustituciones).
            - **Motor:** EV-NORM-ANALYSIS (Validación de la corrección ortotipográfica contra la OLE 2010 y el DPD).
            - **Fuentes de Autoridad:** RAE/ASALE (2010, OLE), Martínez de Sousa (2004, Ortografía y ortotipografía del español actual).
        2. **SD_STYLE (Corrección de Estilo):**
            - **Objetivo:** Detección y corrección de problemas de estilo, coherencia, cohesión y adecuación de registro en un texto original o editado (Tema 4 de 28311A9: corrección de estilo).
            - **Tarea:** El alumno recibe un texto con desviaciones de estilo (redundancias, anacolutos, discordancias de registro, ambigüedades sintácticas, vicios de dicción, cacofonías) y debe elaborar un informe de corrección de estilo razonado, proponiendo las intervenciones necesarias y justificándolas con criterios normativos o de uso.
            - **Widget:** W-HUM-TEXT (Editor con SPLIT_TEXT — Panel estímulo con texto original / Panel de acción con propuesta de corrección).
            - **Motor:** EV-NORM-ANALYSIS + DRA-HOLO (Rúbrica de calidad argumentativa del informe).
            - **Fuentes de Autoridad:** Martínez de Sousa (2012, Manual de estilo de la lengua española), RAE/ASALE (2009, NGLE).
        3. **SD_ANNOT (Anotación Crítica y Edición Científica):**
            - **Objetivo:** Elaboración de una anotación crítica de un fragmento literario en español (competencia CE10 transversal del Grado), que implica el manejo de fuentes, la identificación de variantes textuales relevantes y la redacción de notas filológicas al pie (componente ecdótico — Blecua, 2004).
            - **Tarea:** El alumno recibe un fragmento de texto literario español (Medieval, Siglo de Oro o Contemporáneo) y debe: (a) identificar los problemas de transmisión textual presentes (variantes, lectiones, errores evidentes); (b) proponer y justificar la lectura adoptada apoyándose en criterios ecdóticos básicos (lectio difficilior, lectio brevior, eliminatio codicum descriptorum); (c) redactar las notas al pie con el formato de edición científica estándar de la UGR.
            - **Widget:** W-PHILO-ECDO (Modo SPLIT_TEXT para visualización simultánea de variantes) + W-HUM-TEXT (Editor de notas al pie).
            - **Motor:** EV-PALE (Validación de la corrección de la transcripción y del aparato de variantes) + DRA-HOLO (Rúbrica de calidad argumentativa de las notas).
            - **Fuentes de Autoridad:** Blecua, A. (2004, Manual de crítica textual, Castalia), Biblioteca Virtual Miguel de Cervantes, BVFE.
        4. **SD_EVAL (Evaluación Editorial e Informe de Lector):**
            - **Objetivo:** Elaboración de un informe de evaluación editorial de un original inédito o de una propuesta de edición, según los criterios de la industria editorial española (Prácticas de 28311A9: elaboración de informes de corrección y evaluación de originales).
            - **Tarea:** El alumno recibe un original (fragmento de obra inédita o propuesta de edición científica) y debe elaborar un informe de lector profesional que incluya: valoración de la originalidad y calidad literaria o científica, viabilidad editorial y comercial, correcciones necesarias antes de la publicación, y recomendación final motivada (aceptar, rechazar o aceptar con cambios).
            - **Widget:** W-HUM-TEXT (Editor de informe con rúbrica estructurada).
            - **Motor:** DRA-HOLO (Rúbrica analítica holística: adecuación al género del informe, rigor argumentativo, corrección formal, viabilidad de la propuesta).
    *   **Protocolo de Superación y Rigor:**
        - **Umbral Crítico:** Mínimo 60% en cada destreza de forma independiente. Sin compensación entre destrezas (FAIL_LOGIC: FATAL por destreza si no se alcanza el umbral).
        - **Política de Tolerancia Cero:** El error en la nomenclatura ortotipográfica técnica (ej. confundir raya con guion largo) o la cita falsa de una norma de autoridad (OLE, DPD, NGLE) anula el ítem (FAIL_LOGIC: FATAL para ese ítem).
        - **Corrección Formal Obligatoria:** El informe propio del alumno (SD_STYLE, SD_ANNOT, SD_EVAL) debe estar libre de errores ortotipográficos. La presencia de más de 3 faltas ortotipográficas en el informe del alumno penaliza la destreza en un 20% adicional sobre la nota bruta.
    *   **Rigor Engine:** x1.5 (Nivel C1 - Profesional/Editorial). Inferior al x1.8 de PHILO dado el perfil aplicado y no epistemológico de la asignatura fuente.

*   **SUB-LIN-NORM: Modelo Norma y Uso (UGR / Grado en Filología Hispánica — Asignatura: El Español Actual: Norma y Uso, cód. 2831111, 1º Grado, Troncal, Dpto. Lengua Española) [CERTIFICADO v5.1 — 2026-04-20]**
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

*   **SUB-LIN-TRA-TECH: Modelo de Traducción Profesional y Técnica (FTI UGR — Asignatura: Traducción Especializada B-A Inglés, cód. 252113T, 3º Grado, Obligatoria) [CERTIFICADO v5.1 — 2026-04-20]**
    *   **Perfil Institucional:** Evaluación de la competencia traductora especializada (Científico-Técnica, Jurídico-Económica) bajo el enfoque del Skopos y la ISO 17100.
    *   **Secuencia Genética Obligatoria (Fidelidad 100%):**
        1.  **SD_TRA_ANALYSIS (Análisis del Encargo):** Identificación de la función textual, el destinatario y los problemas potenciales del texto (neologismos, ambigüedades sintácticas) antes de la traducción.
        2.  **SD_TERM_RESEARCH (Fase Documental):** Creación de un glosario técnico bilingüe basado en fuentes de autoridad (IATE, UNTERM). Validación de equivalencias terminológicas unívocas.
        3.  **SD_TRA_DRAFT (Traducción Directa):** Traducción de textos especializados de entre 200-250 palabras cada uno. Se evalúa la precisión léxica, el cumplimiento del registro y la adecuación al género textual.
        4.  **SD_TRA_REVIEW (Control de Calidad y Post-edición):** Revisión de estilo y coherencia. Incluye la post-edición de un output de Traducción Automática (TA) para detectar alucinaciones y errores de cohesión.
    *   **Protocolo de Superación:** Umbral mínimo del 50% en cada sección de traducción de forma independiente. Sin compensación (FAIL_LOGIC: FATAL).
*   **SUB-LIN-TRA-LIT: Modelo de Traducción Literaria y Editorial (FTI UGR — Asignatura: Literatura y Traducción Lengua B Inglés, cód. 25211NJ, 3º Grado, Optativa) [CERTIFICADO v5.1 — 2026-04-20]**
    *   **Perfil:** Traducción de textos creativos, poéticos y humanísticos basada en los criterios de la FTI (UGR).
    *   **Secuencia Genética Obligatoria (3 Fases):**
        1. **SD_TRA_STYLE (Análisis Estilístico Comparado):** Identificación de la voz del autor, rasgos dialectales/cronoflectales y desafíos retóricos. (Widget: W-HUM-TEXT).
        2. **SD_TRA_CREATIVE (Transferencia Estética):** Recreación del efecto estético y literario en la lengua meta (Skopos). Gestión de culturemas e intertextualidad. (Widget: W-HUM-TEXT — Modo TRA-LIT).
        3. **SD_TRA_CRIT (Crítica y Justificación):** Comentario exegético defendiendo las opciones de traducción y compensaciones literarias. (Widget: W-HUM-TEXT).
    *   **Rigor:** Hermenéutico / Nivel C2 (LVL_C).
    *   **Motor Principal:** DRA-HOLO (Rúbrica de Calidad Literaria UGR).

### HUMANIDADES
*   **SUB-HUM-HIST: Modelo Historiográfico (Grado en Historia UGR — Asignaturas: Historia Universal Contemporánea I, cód. 2921128; Historia Moderna Universal I, cód. 2921126; Dpto. Historia Contemporánea aprobado 16/06/2025, Dpto. Historia Moderna aprobado 23/06/2025) [CERTIFICADO v5.3 — 2026-04-22]**
    *   **Perfil Institucional y Pedagógico:** Evaluación de la competencia historiográfica en el Grado en Historia de la UGR. El modelo emula la estructura evaluativa del Dpto. de Historia Contemporánea y del Dpto. de Historia Moderna: prueba escrita de desarrollo y análisis de fuentes primarias como eje central de la calificación, complementada por evaluación continua de trabajos prácticos (comentarios de texto, mapas, imágenes, tablas estadísticas, grabados). La evaluación es íntegramente discursiva: no existe componente de respuesta objetiva estandarizado en el examen de la asignatura núcleo.
    *   **Fuente de Certificación:** Guías Docentes de Historia Universal Contemporánea I (2921128, 2º Grado en Historia, Obligatoria, Dpto. Historia Contemporánea — aprobada 16/06/2025) e Historia Moderna Universal I (2921126, 2º Grado en Historia, Obligatoria, Dpto. Historia Moderna — aprobada 23/06/2025). Patrón evaluativo verificado como transversal al conjunto de asignaturas del Grado.
    *   **Secuencia Genética Obligatoria (Estructura de Dos Destrezas — UGR Grado Historia):**
        1.  **SD_HIST_DEV (Desarrollo Historiográfico — 60-70% de la calificación):**
            *   **Mecánica:** Prueba escrita de desarrollo de contenidos teóricos. El alumno expone y argumenta sobre un tema del programa con estructura lógica y rigor historiográfico. Se valora la capacidad de síntesis y análisis, la organización del discurso y la corrección formal. La exposición debe evitar la mera reproducción memorística: se exige elaboración personal con esquema de análisis original.
            *   **Widget:** W-HUM-TEXT.
            *   **Layout:** Sin partición lateral (el estímulo forma parte del enunciado, no es un documento adjunto permanente).
            *   **Motor:** DRA-HOLO (Rúbrica holística adaptada al discurso historiográfico — ver nota de configuración HIST en V06DOC_BLOCKS.md).
            *   **Criterio mínimo de superación:** El alumno debe obtener 5/10 en esta destreza para que pueda realizarse la media con SD_HIST_PRAC. Sin esta condición, la asignatura queda suspensa con independencia de la nota práctica (FAIL_LOGIC: FATAL).
        2.  **SD_HIST_PRAC (Análisis de Fuentes y Comentario de Documentos Históricos — 30-40% de la calificación):**
            *   **Mecánica:** Análisis de una fuente histórica primaria o secundaria (documento escrito, mapa histórico, grabado, imagen, tabla estadística o gráfico de datos). El alumno debe identificar el tipo documental, contextualizarlo en su marco temporal e ideológico, y elaborar un comentario crítico argumentado. No se admite la mera descripción sin contextualización historiográfica. Se valora especialmente la elaboración personal y la capacidad para establecer relaciones causales y consecuenciales entre el documento y su época.
            *   **Widget:** W-HUM-TEXT con layout W-LAYOUT-SIDE (documento/fuente en panel izquierdo sticky; editor de comentario en panel derecho).
            *   **Motor:** DRA-HOLO (configuración HIST).
            *   **Tipología documental emulable:** Texto histórico primario (discurso, tratado, manifiesto, diario, carta), mapa histórico, grabado o ilustración con carga histórica, tabla estadística de datos demográficos o económicos, gráfico de evolución histórica.
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        *   **Umbral de SD_HIST_DEV:** Mínimo 5/10 (condición necesaria no compensable — FAIL_LOGIC: FATAL si no se alcanza).
        *   **Calificación final:** Media ponderada de SD_HIST_DEV (60-70%) + SD_HIST_PRAC (30-40%). Los porcentajes exactos los fija el profesorado al inicio de curso; la plataforma opera con la banda certificada.
        *   **Penalización por plagio o reproducción sin cita:** Calificación 0 automática en el ítem afectado (coherente con la normativa de evaluación UGR, artículo 15.2).
        *   **Rigor Engine:** x1.2 (LVL_A — 1º y 2º año del Grado) / x1.4 (LVL_B — 3º y 4º año del Grado).
        *   **Widgets activos:** W-HUM-TEXT, W-LAYOUT-SIDE. W-OBJ-STRIKE queda EXCLUIDO de este subarquetipo — no existe componente de respuesta objetiva en el patrón evaluativo certificado del Grado en Historia UGR.
*   **SUB-HUM-PHIL: Modelo Dialéctico (Grado en Filosofía UGR — Asignaturas: Historia de la Filosofía Antigua II, cód. 26311M3, aprobada 23/06/2025; Filosofía y Argumentación, cód. 2631111, aprobada 24/06/2025; Historia de la Filosofía Española, cód. 26311M5, aprobada 23/06/2025) [CERTIFICADO v5.3 — 2026-04-22]**
    *   **Perfil Institucional y Pedagógico:** Evaluación de la competencia filosófica en el Grado en Filosofía de la UGR. El modelo emula la estructura evaluativa cuatripartita transversal al Dpto. de Filosofía I y Dpto. de Filosofía II: test de precisión conceptual + preguntas de desarrollo de extensión media + comentario de texto filosófico del programa + ensayo filosófico argumentado con fundamentación bibliográfica. El patrón es constante en las asignaturas del Grado con independencia de la especialidad (antigua, española, contemporánea, argumentación). La competencia nuclear es la construcción, articulación y defensa de argumentos filosóficos propios, rigurosos y razonados mediante terminología filosófica precisa.
    *   **Fuente de Certificación:** Guías Docentes de Historia de la Filosofía Antigua II (26311M3, 2º Grado en Filosofía, Optativa, Dpto. Filosofía II — aprobada 23/06/2025), Filosofía y Argumentación (2631111, 1º Grado en Filosofía, Troncal, Dpto. Filosofía I/II — aprobada 24/06/2025) e Historia de la Filosofía Española (26311M5, Optativa, Dpto. Filosofía I/II — aprobada 23/06/2025). El patrón cuatripartita está verificado como transversal al conjunto de asignaturas del Grado.
    *   **Secuencia Genética Obligatoria (Estructura de Cuatro Partes — UGR Grado Filosofía):**
        1.  **SD_PHIL_TEST (Precisión Conceptual — test):**
            *   **Mecánica:** Test de respuesta alternativa sobre conceptos, categorías, autores y tesis nucleares del programa. Evalúa la exactitud terminológica y la identificación correcta de posiciones filosóficas. La confusión de tesis entre autores o la atribución incorrecta de conceptos activa penalización (PRM-STRIKE con fórmula UGR de corrección por azar).
            *   **Widget:** W-OBJ-STRIKE / Motor: PRM-STRIKE (penalización activa).
            *   **Peso orientativo:** ~15-20% de la calificación del examen.
        2.  **SD_PHIL_DEV (Preguntas de Desarrollo de Extensión Media):**
            *   **Mecánica:** El alumno desarrolla por escrito entre dos y cinco cuestiones de extensión media sobre epígrafes del programa. Se valora la precisión terminológica, la organización lógica del discurso y la capacidad de síntesis argumentada. No se admite la mera enumeración sin argumentación.
            *   **Widget:** W-HUM-TEXT.
            *   **Motor:** DRA-HOLO (configuración PHIL).
            *   **Peso orientativo:** ~30-35% de la calificación del examen.
        3.  **SD_PHIL_TEXT (Comentario de Texto Filosófico):**
            *   **Mecánica:** El alumno comenta un fragmento de texto filosófico del corpus del programa (Platón, Aristóteles, Gracián, autores del programa según asignatura). El comentario debe situar el texto en su contexto histórico-filosófico, identificar las tesis y argumentos del autor, y relacionarlos con el conjunto de su pensamiento y con el debate filosófico del período. Se valora especialmente la capacidad de interpretación interna del texto frente a la mera paráfrasis.
            *   **Widget:** W-HUM-TEXT con layout W-LAYOUT-SIDE (texto filosófico en panel izquierdo sticky; editor de comentario en panel derecho).
            *   **Motor:** DRA-HOLO (configuración PHIL).
            *   **Peso orientativo:** ~25-30% de la calificación del examen.
        4.  **SD_PHIL_ESSAY (Ensayo Filosófico Argumentado):**
            *   **Mecánica:** El alumno redacta un ensayo filosófico de 1200-2000 palabras con argumentación original, posicionamiento crítico ante un problema filosófico del programa y uso riguroso de al menos dos fuentes bibliográficas oficiales de la asignatura. Se penaliza la ausencia de toma de postura propia, la cita incorrecta o la reproducción sin argumentación personal. Se aplica FAIL_LOGIC: FATAL si el ensayo carece de toda fundamentación bibliográfica.
            *   **Widget:** W-HUM-TEXT.
            *   **Motor:** DRA-HOLO (configuración PHIL — exigencia máxima en Eje 4: rigor del argumento propio y uso de fuentes).
            *   **Peso orientativo:** ~25-30% de la calificación del examen.
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        *   **Umbral global:** Mínimo 5/10 en la media ponderada de las cuatro partes. Las cuatro partes NO son compensables entre sí por debajo del umbral de suficiencia parcial de cada una (FAIL_LOGIC: FATAL si SD_PHIL_ESSAY carece de bibliografía o si SD_PHIL_TEXT se limita a paráfrasis sin interpretación).
        *   **Rigor Engine:** x1.3 (LVL_A — 1º y 2º año) / x1.6 (LVL_B — 3º y 4º año — MAIOR).
        *   **Penalización formal:** La corrección ortotipográfica es condición de evaluabilidad en SD_PHIL_ESSAY — más de 5 faltas graves en el ensayo penaliza el eje de corrección formal en DRA-HOLO en un 50% adicional (coherente con la regla eliminatoria del arquetipo HERMENÉUTICO en V06DOC_ARCHETYPES.md).
*   **SUB-HUM-ART-HIST: Modelo Iconográfico (Grado en Historia del Arte UGR — Asignaturas: Iconografía, cód. 26511M2, aprobada 24/06/2025; Historia de los Estilos e Iconografía, cód. 2931114, aprobada 24/06/2025) [CERTIFICADO v5.3 — 2026-04-22]**
    *   **Perfil Institucional y Pedagógico:** Evaluación de la competencia iconográfica e iconológica en el Grado en Historia del Arte de la UGR. El modelo emula la estructura evaluativa del Dpto. de Historia del Arte: prueba de reconocimiento iconográfico de imágenes como eje sumativo (50-60%) complementada por análisis formal e iconológico escrito (40-50%). Las dos destrezas son independientes y no compensables: la identificación errónea en campos críticos (autor, cronología) impide la superación del ítem con independencia de la calidad del análisis. La metodología de análisis aplicada es la tripartita de Panofsky (descripción pre-iconográfica → análisis iconográfico → interpretación iconológica), verificada como estándar del Dpto. de Historia del Arte UGR.
    *   **Fuente de Certificación:** Guías Docentes de Iconografía (26511M2, Grado en Conservación y Restauración de Bienes Culturales, Obligatoria, Dpto. Historia del Arte — aprobada 24/06/2025) e Historia de los Estilos e Iconografía (2931114, 1º Grado en Historia del Arte, Troncal, Dpto. Historia del Arte — aprobada 24/06/2025). Bibliografía de referencia metodológica certificada: Carmona Muela, Réau y Hall (iconografía cristiana y clásica); Panofsky (Estudios sobre iconología, 1972; El significado en las artes visuales, 1979).
    *   **Secuencia Genética Obligatoria (Estructura de Dos Destrezas — UGR Grado Historia del Arte):**
        1.  **SD_ART_IDENT (Reconocimiento Iconográfico de Imágenes — 50-60% de la calificación):**
            *   **Mecánica:** El alumno recibe una imagen de obra de arte del corpus del programa y debe cumplimentar el formulario de identificación estructurada mediante W-ART-IDENT. Los campos obligatorios son: Autor/Atribución, Cronología/Período, Técnica/Soporte, Estilo/Escuela, Título/Tema iconográfico. La identificación errónea del Autor o la Cronología en más de un período estilístico completo activa FAIL_LOGIC: FATAL para la fase de identificación del ítem, con independencia de la calidad del análisis posterior.
            *   **Widget:** W-ART-IDENT.
            *   **Motor:** EV-ICON-ART (Fase de Identificación — 40% del ítem dentro de la destreza).
            *   **Corpus emulable:** Obras del repertorio iconográfico oficial del Dpto. de Historia del Arte UGR — iconografía cristiana (Carmona Muela, Réau), iconografía clásica (Hall), repertorios de otras culturas según el programa.
        2.  **SD_ART_ANAL (Análisis Formal e Iconológico — 40-50% de la calificación):**
            *   **Mecánica:** El alumno redacta el comentario analítico de la misma imagen siguiendo los tres niveles de Panofsky: descripción pre-iconográfica (composición, figuras, espacios, color, luz), análisis iconográfico (identificación de temas, motivos, atributos y fuentes del programa), e interpretación iconológica (contextualización histórico-cultural, programa iconográfico, significado intrínseco). No se puede acceder al nivel iconológico sin haber completado el pre-iconográfico.
            *   **Widget:** W-HUM-TEXT con layout W-LAYOUT-SIDE (imagen en panel izquierdo sticky; editor de análisis en panel derecho).
            *   **Motor:** EV-ICON-ART (Fase de Análisis — 60% del ítem dentro de la destreza).
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        *   **Umbral de cada destreza:** Mínimo 5/10 en SD_ART_IDENT y mínimo 5/10 en SD_ART_ANAL de forma independiente. Sin compensación entre destrezas (FAIL_LOGIC: FATAL por destreza no superada).
        *   **Calificación final:** Media ponderada de SD_ART_IDENT (50-60%) + SD_ART_ANAL (40-50%). Los porcentajes exactos los fija el profesorado; la plataforma opera con la banda certificada.
        *   **Rigor Engine:** x1.3 (LVL_A — 1º y 2º año — ITIN_MAI) / x1.6 (LVL_B — 3º y 4º año — ITIN_MAI).
        *   **Widgets activos:** W-ART-IDENT, W-HUM-TEXT, W-LAYOUT-SIDE. Motor: EV-ICON-ART.
*   **SUB-HUM-ART-CREA: Modelo Bellas Artes — Emulación Parcial Certificada (Grado en Bellas Artes UGR — Asignaturas: Arte y Cuerpo, cód. 26011D1, Dpto. Pintura aprobada 09/06/2025 / Dpto. Escultura aprobada 24/06/2025; Principios Básicos de la Pintura, cód. 2601114, Dpto. Pintura aprobada junio 2025) [CERTIFICADO v5.3 — 2026-04-22]**
    *   **DECLARACIÓN DE EMULACIÓN PARCIAL CERTIFICADA [VINCULANTE — 2026-04-21]:** Este subarquetipo emula exclusivamente las destrezas digitalizables del Grado en Bellas Artes UGR. La destreza nuclear del Grado — la realización de obra de taller presencial (pintura, escultura, instalación, performance corporal) — es **no digitalizable** y queda fuera del alcance de la plataforma. Esta exclusión es permanente, está documentada explícitamente y no puede ser revisada sin indicación explícita del usuario. Las destrezas emuladas son: portafolio digital de proceso creativo, memoria de proceso escrita y análisis crítico argumentado.
    *   **Perfil Institucional y Pedagógico:** Evaluación de las competencias teórico-reflexivas y de documentación del proceso creativo en el Grado en Bellas Artes de la UGR. El patrón evaluativo transversal de la Facultad de Bellas Artes UGR incluye: entrega obligatoria de portafolio/dossier/memoria que recoja toda la producción de trabajos (obligatorio por normativa UGR Art. 16) + prueba teórica escrita sobre contenidos del programa. La plataforma emula la parte digitalizable: portafolio digital de proceso creativo (60-70% del componente práctico emulable) + memoria de proceso y análisis crítico escrito (30-40% del componente teórico emulable).
    *   **Fuente de Certificación:** Guías Docentes de Arte y Cuerpo (26011D1, 4º Grado en Bellas Artes, Optativa, Dpto. Pintura/Escultura — aprobadas 09/06/2025 y 24/06/2025) y Principios Básicos de la Pintura (2601114, 1º Grado en Bellas Artes, Obligatoria, Dpto. Pintura — aprobada junio 2025). Patrón evaluativo verificado como transversal a toda la Facultad de Bellas Artes UGR.
    *   **Secuencia Genética Obligatoria — Alcance Emulable (Estructura de Dos Destrezas):**
        1.  **SD_CREA_PORT (Portafolio Digital de Proceso Creativo — 60-70% del alcance emulable):**
            *   **Mecánica:** El alumno entrega una galería de imágenes que documenta los estados intermedios del proceso creativo de un proyecto artístico: bocetos, estudios previos, pruebas materiales, versiones intermedias y obra final fotografiada. Cada imagen debe ir acompañada de un pie de foto que documente el estado del proceso, las decisiones adoptadas y los referentes artísticos aplicados. La ausencia de documentación de estados intermedios (presentación de la obra final sin documentación del proceso) activa FAIL_LOGIC: FATAL para este eje.
            *   **Widget:** W-PORTFOLIO (Portafolio Digital de Proceso Creativo).
            *   **Motor:** DRA-HOLO configuración ART-CREA (Eje 1 — Coherencia del Proceso Creativo).
            *   **Destrezas de taller excluidas:** Realización física de la obra (pintura, escultura, instalación, performance presencial). Estas destrezas son no emulables y quedan fuera del alcance de la plataforma.
        2.  **SD_CREA_MEM (Memoria de Proceso y Análisis Crítico — 30-40% del alcance emulable):**
            *   **Mecánica:** El alumno redacta en dos bloques diferenciados: (a) Memoria de proceso — descripción y justificación de las decisiones creativas adoptadas durante el proyecto, con referencia explícita a los materiales, procedimientos y soportes utilizados y a los referentes artísticos del programa; (b) Análisis crítico — contextualización de la obra propia en los debates artísticos contemporáneos del programa y argumentación original sobre las decisiones creativas adoptadas. Ambos bloques son evaluados como una unidad por DRA-HOLO ART-CREA.
            *   **Widget:** W-HUM-TEXT.
            *   **Motor:** DRA-HOLO configuración ART-CREA (Ejes 2, 3 y 4 — Calidad de la Memoria, Profundidad del Análisis Crítico, Corrección Formal).
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        *   **Umbral global:** Mínimo 5/10 en la media de los cuatro ejes de DRA-HOLO ART-CREA.
        *   **FAIL_LOGIC:** FATAL para Eje 1 si el portafolio presenta obra final sin documentación del proceso — el subarquetipo queda suspenso independientemente de la calidad de la memoria y el análisis.
        *   **Penalización formal:** Más de 5 faltas ortotipográficas graves en el conjunto de la documentación escrita penaliza el Eje 4 en un 50% adicional.
        *   **Rigor Engine:** x1.2 (LVL_A — 1º y 2º año) / x1.4 (LVL_B — 3º y 4º año).
        *   **Widgets activos:** W-PORTFOLIO, W-HUM-TEXT. Motor: DRA-HOLO configuración ART-CREA.
*   **SUB-HUM-MUS: Modelo Musicología (Grado en Historia y Ciencias de la Música UGR — Asignaturas: Análisis II: Clasicismo y Romanticismo, cód. 2991132, aprobada 23/06/2025; Fundamentos de la Expresión Musical y su Evolución I, cód. 2991114, Dpto. Historia y Ciencias de la Música aprobada 23/06/2025 / Dpto. Didáctica aprobada 25/06/2025) [CERTIFICADO v5.3 — 2026-04-22]**
    *   **Perfil Institucional y Pedagógico:** Evaluación de la competencia musicológica y analítica en el Grado en Historia y Ciencias de la Música de la UGR. El modelo emula la estructura evaluativa del Dpto. de Historia y Ciencias de la Música: dos destrezas independientes no compensables de peso igual (50%/50%), con umbral mínimo del 50% en cada una. La primera destreza evalúa la capacidad de identificación auditiva (período, estilo, forma, género, instrumentación, rasgos estilísticos) a partir de fragmentos musicales. La segunda evalúa la capacidad de análisis formal, armónico y estilístico a partir de partitura. Bibliografía de referencia analítica certificada: LaRue (1989), Cook (1991), Bent (1980), Blanquer Ponsoda (1989), Cadwallader.
    *   **Fuente de Certificación:** Guías Docentes de Análisis II: Clasicismo y Romanticismo (2991132, 3º Grado en Historia y Ciencias de la Música, Obligatoria, Dpto. Historia y Ciencias de la Música — aprobada 23/06/2025) y Fundamentos de la Expresión Musical y su Evolución I (2991114, 1º Grado en Historia y Ciencias de la Música, Obligatoria, Dpto. Historia y Ciencias de la Música/Dpto. Didáctica — aprobadas 23/06/2025 y 25/06/2025).
    *   **Secuencia Genética Obligatoria (Estructura de Dos Destrezas — UGR Grado Historia y Ciencias de la Música):**
        1.  **SD_MUS_LIST (Identificación Auditiva — 50% de la calificación):**
            *   **Mecánica:** El alumno escucha fragmentos musicales del corpus del programa (Clasicismo, Romanticismo y períodos adyacentes según el nivel) y debe identificar: período estilístico, estilo compositivo específico, forma musical, género, instrumentación/agrupación y rasgos estilísticos definitorios. Los ítems se presentan combinando W-OBJ-STRIKE (identificación múltiple de período/estilo/género/instrumentación), W-TXT-CLOZE (completado de ficha analítica con términos del metalenguaje musicológico) y W-MIX-MATCH (emparejamiento fragmento/compositor o fragmento/período). El número de reproducciones por fragmento es variable según la estrategia configurada para cada nivel — NO está fijado en 2 reproducciones como en SUB-LIN-INSTR.
            *   **Widget:** W-AUDIO-INSTR (configuración MUS — reproducciones variables).
            *   **Motor:** EV-MUS-ANAL (SD_MUS_LIST).
            *   **Umbral mínimo:** 5/10 en esta destreza de forma independiente. FAIL_LOGIC: FATAL si no se alcanza, sin compensación con SD_MUS_SCORE.
        2.  **SD_MUS_SCORE (Análisis en Partitura — 50% de la calificación):**
            *   **Mecánica:** El alumno recibe una partitura de una obra del corpus del programa en el visor W-MUS-SCORE y debe realizar: análisis armónico (grados romanos, funciones tonales, cadencias), análisis formal (identificación y delimitación de secciones con denominación canónica conforme a LaRue 1989) y comentario musicológico (metalenguaje de textura, timbre, ritmo, melodía, armonía, forma; contextualización estilística). La confusión de función tonal dominante con subdominante en contexto cadencial activa penalización severa. El análisis debe redactarse en el editor adjunto al visor.
            *   **Widget:** W-MUS-SCORE (con editor de análisis integrado) + W-HUM-TEXT para el comentario musicológico.
            *   **Motor:** EV-MUS-ANAL (SD_MUS_SCORE).
            *   **Umbral mínimo:** 5/10 en esta destreza de forma independiente. FAIL_LOGIC: FATAL si no se alcanza, sin compensación con SD_MUS_LIST.
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        *   **Umbral de cada destreza:** Mínimo 5/10 en SD_MUS_LIST y mínimo 5/10 en SD_MUS_SCORE de forma independiente (FAIL_LOGIC: FATAL por destreza no superada — coherente con la normativa explícita de la Guía Docente 2991132).
        *   **Calificación final:** Media aritmética de SD_MUS_LIST (50%) + SD_MUS_SCORE (50%).
        *   **Rigor Engine:** x1.3 (LVL_B — 3º año del Grado) / x1.6 (LVL_C — 4º año del Grado).
        *   **Bibliografía analítica de referencia:** LaRue (1989, *Análisis del estilo musical*), Cook (1991, *A guide to musical analysis*), Bent (1980, "Analysis" en *The New Grove Dictionary*), Blanquer Ponsoda (1989), Cadwallader (*Analysis of tonal music: a Schenkerian approach*).
        *   **Widgets activos:** W-AUDIO-INSTR, W-OBJ-STRIKE, W-TXT-CLOZE, W-MIX-MATCH, W-MUS-SCORE, W-HUM-TEXT. Motor: EV-MUS-ANAL.
*   **SUB-HUM-ANTH: Modelo Antropológico — Subarquetipo Transversal (Sin asignatura monográfica UGR) [CERTIFICADO v5.3 — 2026-04-22]**
    *   **DECLARACIÓN INSTITUCIONAL DE TRANSVERSALIDAD [VINCULANTE — 2026-04-22]:** La Antropología Social y Cultural no cuenta con asignatura monográfica propia en los Grados de la UGR analizados en el marco del Hito 6. Sus contenidos y competencias se distribuyen transversalmente a través de asignaturas de Sociología, Filosofía, Historia y Ciencias Sociales. Esta circunstancia es estructural en el diseño de los planes de estudio de las universidades andaluzas y no constituye una laguna de la plataforma. La declaración es permanente y análoga a la declaración de transversalidad de SUB-LIN-TRA-LIT en la Rama Lenguas. El subarquetipo se documenta explícitamente sin anclaje en una guía docente específica de referencia.
    *   **Perfil Pedagógico (Sin Fuente Monográfica Certificada):** El modelo SUB-HUM-ANTH emula las competencias evaluativas transversales de la Antropología Social y Cultural tal como aparecen distribuidas en los planes de estudio UGR: análisis de estructuras culturales y sociales, interpretación de datos etnográficos y comparación intercultural. Al carecer de guía docente monográfica de referencia, el patrón evaluativo se construye a partir del perfil competencial del arquetipo HERMENÉUTICO (V06DOC_ARCHETYPES.md, sección 5) y de los criterios de evaluación genéricos de las asignaturas de Ciencias Sociales y Humanidades de la UGR donde la Antropología aparece como componente transversal.
    *   **Secuencia Genética Obligatoria (Patrón Transversal Certificado):**
        1.  **SD_ANTH_TEXT (Comentario de Fuente Etnográfica o Texto Antropológico):**
            *   **Mecánica:** El alumno comenta una fuente etnográfica, un fragmento de trabajo de campo, un texto antropológico clásico o un caso de estudio intercultural. Debe identificar el marco teórico del texto (funcionalismo, estructuralismo, interpretativismo, etc.), analizar las categorías culturales empleadas y contextualizar el caso en la tradición antropológica correspondiente.
            *   **Widget:** W-HUM-TEXT con layout W-LAYOUT-SIDE (fuente/texto en panel izquierdo sticky; editor de comentario en panel derecho).
            *   **Motor:** DRA-HOLO (configuración HERMENÉUTICO).
            *   **Peso orientativo:** ~50% de la calificación.
        2.  **SD_ANTH_ESSAY (Disertación Comparativa Intercultural):**
            *   **Mecánica:** El alumno redacta una disertación comparativa de 800-1500 palabras sobre un problema antropológico propuesto (estructura de parentesco, ritual, identidad cultural, diversidad, cambio social). Debe aplicar conceptos del metalenguaje antropológico, comparar al menos dos contextos culturales distintos y argumentar desde una perspectiva teórica explícitamente declarada.
            *   **Widget:** W-HUM-TEXT.
            *   **Motor:** DRA-HOLO (configuración HERMENÉUTICO).
            *   **Peso orientativo:** ~50% de la calificación.
    *   **Protocolo de Superación y Rigor (V06DOC_LEVELS):**
        *   **Umbral global:** Mínimo 5/10 en la media ponderada de las dos destrezas.
        *   **FAIL_LOGIC:** FATAL para SD_ANTH_ESSAY si la disertación carece de marco teórico explícito o no aplica metalenguaje antropológico reconocible.
        *   **Rigor Engine:** x1.2 (LVL_A) / x1.4 (LVL_B).
        *   **Widgets activos:** W-HUM-TEXT, W-LAYOUT-SIDE. Motor: DRA-HOLO (configuración HERMENÉUTICO).
        *   **PROHIBICIÓN:** No se pueden crear widgets ni motores adicionales para este subarquetipo sin investigación online previa que identifique una asignatura monográfica UGR de referencia que justifique la extensión del modelo.

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
