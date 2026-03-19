<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_SUBARCHETYPES.md -->
# V06DOC_SUBARCHETYPES - MATRIZ DE ESPECIALIZACIÓN ACADÉMICA (V2.0 - DETERMINISTA)

Este documento define la **Configuración Estructural Fija** (Receta) que cada Estrategia de Python debe implementar.
**PRINCIPIO:** Python define los Secciones y los Ítems (Widgets). La IA solo rellena el contenido solicitado.

**NOTA DE IMPLEMENTACIÓN:** Cada subarquetipo listado aquí se traduce en una clase `Strategy` que devuelve un esqueleto inmutable.


## 1. RAMA: ARTES Y HUMANIDADES (12 Modelos)
### LENGUAS (CLM / LENGUAS MODERNAS)
*   **SUB-LIN-INSTR: Modelo Instrumental (Acreditación CertAcles / CLM UGR) [REFACTORIZADO SUBATÓMICO]**
    *   **Perfil:** Evaluación de competencia operativa integral para fines generales y académicos.
    *   **Secuencia Genética Obligatoria (5 Fases / 5 Destrezas):**
        1. **SD_READ (Reading):** 3 Ítems (PRM-STRIKE para detalle, MAT-LINK para global, CLO-MULTI para gramática en contexto).
        2. **SD_LIST (Listening):** 2 Ítems (PRM-STRIKE + RBT-CANON). Máximo 2 reproducciones.
        3. **SD_WRIT (Writing):** 2 Tareas (Producción breve funcional + Ensayo académico DRA-HOLO).
        4. **SD_SPEAK (Speaking):** 2 Bloques (Monólogo W-COMM-DIALOG + Interacción DIA-INTERACT).
        5. **SD_MEDI (Mediation):** 1 Tarea (Transferencia de registro técnico a divulgativo BMT-SHIFT).
    *   **Directriz de Multimodalidad (Miguel Ángel):** Los widgets de texto (W-HUM-TEXT, W-TXT-CLOZE) deben activar el selector de entrada: Teclado Nativo, Transliteración, Pad de Trazos u OCR según el idioma objetivo.
    *   **Criterio de Éxito:** 60% mínimo en CADA fase. Sin posibilidad de compensación entre destrezas. Navegación secuencial bloqueada.
*   **SUB-LIN-MINOR: Modelo Minor / Iniciación (UGR - Facultad Filosofía y Letras) [REFACTORIZADO V3.1]**
    *   **Perfil:** Iniciación a la competencia lingüística y caligráfica (Alemán, Árabe, Checo, Chino, Griego, Hebreo, Italiano, Japonés, Polaco, Portugués, Ruso).
    *   **Excepción B2:** Los itinerarios de Inglés y Francés Minor inician directamente en nivel B2 (MCERL).
    *   **Secuencia Genética Obligatoria (4 Fases):**
        1. **SD_GRAPH (Grafía y Fonética):** Dictado de signos/caracteres y transcripción. Uso OBLIGATORIO de Pad de Trazos/OCR para alfabetos no latinos (Chino, Árabe, Japonés, Ruso, Hebreo).
        2. **SD_GRAM (Estructura Base):** Construcción morfosintáctica elemental (Módulo Inicial I y II).
        3. **SD_READ_MIN (Lectura Adaptada):** Comprensión de textos breves y señalética real.
        4. **SD_CULT (Contexto Sociocultural):** Validación de normas de cortesía, geografía y cultura base.
    *   **Parámetros de Inmersión:** Inmersión VEHICULAR (Castellano) obligatoria en instrucciones para niveles LVL_A y LVL_B.
    *   **Regla de Oro UGR (CertAcles):** Umbral del 60% por destreza obligatoria. Sin compensación.
*   **SUB-LIN-PHILO: Modelo Filológico (UGR / Filología Hispánica y Clásica) [REFACTORIZADO V3.2]**
    *   **Perfil:** Análisis científico, histórico y ecdótico de la lengua y sus textos.
    *   **Secuencia Genética Obligatoria (4 Fases):**
        1. **SD_PHONO (Fonética y Fonología Histórica):** Análisis de leyes de evolución sonora (ej. Yod, lenición) y transcripción paleográfica/IPA.
        2. **SD_MORPH_DIAC (Morfología Diacrónica):** Evolución de paradigmas nominales y verbales desde la lengua origen (Latín/Indoeuropeo/Germánico).
        3. **SD_LEX_SEM (Lexicología y Semántica):** Etimología, cambios semánticos y análisis de préstamos (Germanismos, Arabismos).
        4. **SD_TEXT_CRIT (Crítica Textual / Ecdótica):** Colación de variantes, estema codicum y establecimiento de edición crítica.
    *   **Rigor:** Epistemológico (LVL_C). Prohibición absoluta de paráfrasis.
    *   **Motor Principal:** EV-DIAC-VAL (Validación Diacrónica).

*   **SUB-LIN-NORM: Modelo Norma y Uso (UGR / Grado Filología) [VERIFICADO UGR 2025/26]**
    *   **Perfil:** Análisis avanzado de la norma panhispánica y fenómenos antinormativos.
    *   **Secuencia Genética Obligatoria (4 Fases):**
        1. **SD_CORPUS_ANALYSIS:** Búsqueda y análisis de frecuencias en CORPES XXI/CREA (Widget W-LAW-NAV).
        2. **SD_MORPH_ANTINORM:** Identificación de queísmo, dequeísmo, leísmo y concordancias complejas.
        3. **SD_ORTHO_PRESCRIPTIVE:** Ortografía técnica y puntuación según la Ortografía de la Lengua Española (2010).
        4. **SD_CRITICAL_NORM:** Comentario crítico sobre la adecuación de un texto al registro académico vs. norma.
    *   **Rigor:** C1/C2 (Avanzado).
*   **SUB-LIN-TRA-TECH:** (Traducción Profesional). Glosarios, memorias de traducción y terminología.
*   **SUB-LIN-TRA-LIT: Modelo de Traducción Literaria y Editorial (FTI UGR) [REFACTORIZADO V3.2]**
    *   **Perfil:** Traducción de textos creativos, poéticos, narrativos y humanísticos.
    *   **Secuencia Genética Obligatoria (3 Fases):**
        1. **SD_TRA_STYLE (Análisis Estilístico Comparado):** Identificación de la voz del autor y transposición de figuras retóricas y matices.
        2. **SD_TRA_CREATIVE (Transferencia Creativa):** Recreación del efecto estético y literario en la lengua de llegada.
        3. **SD_TRA_CRIT (Crítica de Traducción):** Análisis exegético de versiones previas y justificación de la propuesta personal.
    *   **Rigor:** Hermenéutico (LVL_C).
    *   **Motor Principal:** DRA-HOLO (Rúbrica de Calidad Literaria).
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
