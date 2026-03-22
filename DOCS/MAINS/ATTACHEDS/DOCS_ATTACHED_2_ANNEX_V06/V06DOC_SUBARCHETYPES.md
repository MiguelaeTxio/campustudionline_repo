# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_SUBARCHETYPES.md
# V06DOC_SUBARCHETYPES - MATRIZ DE ESPECIALIZACIÓN ACADÉMICA (V2.1 - DETERMINISTA)

Este documento define la **Configuración Estructural Fija** (Receta) que cada Estrategia de Python debe implementar.
**PRINCIPIO:** Python define los Secciones y los Ítems (Widgets). La IA solo rellena el contenido solicitado.

**NOTA DE IMPLEMENTACIÓN:** Cada subarquetipo listado aquí se traduce en una clase `Strategy` que devuelve un esqueleto inmutable.


## 1. RAMA: ARTES Y HUMANIDADES (12 Modelos)
### LENGUAS (CLM / LENGUAS MODERNAS)
*   **SUB-LIN-INSTR: Modelo Instrumental (Acreditación CertAcles / CLM UGR) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR]**
    *   **Perfil Institucional:** Evaluación de la competencia comunicativa operativa (B1/B2) bajo el Marco Común Europeo de Referencia (MCERL) y la normativa del CLM-UGR y CertAcles.
    *   **Secuencia Genética Obligatoria (Penta-Destreza):**
        1. **SD_READ (Comprensión de Lectura):**
            - Tarea 1: Comprensión Global/Ideación. Emparejar 6-8 encabezados con párrafos de un texto de 400-500 palabras. (Widget: W-MIX-MATCH / Motor: MAT-LINK).
            - Tarea 2: Localización de Información Específica. Selección de datos concretos en 4-5 micro-textos temáticos. (Widget: W-OBJ-STRIKE / Motor: PRM-STRIKE).
            - Tarea 3: Reconstrucción Coherente (Gapped Text). Reintegrar 5-6 fragmentos extraídos en su posición original. (Widget: W-TXT-CLOZE / Modo: Select / Motor: CLO-MULTI).
        2. **SD_LIST (Comprensión Auditiva):**
            - Tarea 1: Discriminación en Micro-Interacciones. Preguntas de opción múltiple sobre 6-8 diálogos situacionales. (Widget: W-OBJ-STRIKE / Motor: PRM-STRIKE).
            - Tarea 2: Extracción de Datos / Toma de Notas. Completado de esquema basado en monólogo/entrevista. (Widget: W-TXT-CLOZE / Modo: Open). **Motor: RBT-SHORT-LANG (Restricción estricta: 1-4 palabras).**
            - **Restricción de Acceso:** Máximo 2 reproducciones de audio por ítem.
        3. **SD_WRIT (Expresión e Interacción Escrita):**
            - Tarea 1: Interacción Funcional Dirigida. Email/Carta formal cubriendo 3-4 puntos obligatorios. Extensión: 120-150 palabras. (Widget: W-HUM-TEXT / Rúbrica: DRA-HOLO).
            - Tarea 2: Discurso Académico / Ensayo. Producción argumentativa sobre tema propuesto. Extensión: 150-180 palabras. (Widget: W-HUM-TEXT / Rúbrica: DRA-HOLO).
        4. **SD_SPEAK (Expresión e Interacción Oral):**
            - Fase 1: Entrevista de Identidad y Entorno. (Widget: W-COMM-DIALOG).
            - Fase 2: Monólogo Sostenido de Análisis. Descripción de situación basada en estímulo visual complejo. (Widget: W-COMM-DIALOG).
            - Fase 3: Mediación Dialéctica / Negociación. Toma de decisiones compartida con UniversIA en tiempo real. (Widget: W-COMM-DIALOG / Motor: DIA-INTERACT).
        5. **SD_MEDI (Mediación Lingüística):**
            - Tarea 1: Transferencia Intralingüística/Interlingüística. Adaptación de información técnica de un gráfico o texto complejo a un destinatario no experto. (Widget: BMT-SHIFT).
    *   **Protocolo de Superación UGR:**
        - Umbral Crítico: Mínimo 60% de la puntuación en CADA destreza.
        - Compensación: Prohibida (FAIL_LOGIC: FATAL).
        - Navegación: Unidireccional Sellada (No-Backtracking entre destrezas).

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

*   **SUB-LIN-TRA-TECH:** (Traducción Profesional). Glosarios, memorias de traducción y terminología.
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
