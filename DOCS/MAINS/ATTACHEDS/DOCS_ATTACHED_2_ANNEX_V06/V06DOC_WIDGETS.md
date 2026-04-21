# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_WIDGETS.md
# V06DOC_WIDGETS - CATÁLOGO DE COMPONENTES DE INTERFAZ (V1.2 - REFACTORIZACIÓN UGR)

## 1. LIBRERÍA DE COMPONENTES TÉCNICOS

*   **W-DOC-RESOURCES (Panel de Recursos Documentales UGR) [REFACTORIZADO v5.1 — 2026-04-21]**
    *   **Uso:** SUB-LIN-TRA-TECH, fases SD_TERM_RESEARCH y SD_TRA_DRAFT.
    *   **Justificación de Reconversión:** El widget anterior (W-TRA-CAT-EMULATOR) emulaba una herramienta TAO profesional (memoria de traducción, glosario automático), lo cual es incorrecto para el contexto universitario UGR. En el examen oficial de Traducción Especializada B-A Inglés (252113T, FTI-UGR) el alumno no usa herramienta TAO: trabaja con diccionarios bilingües convencionales y elabora su propio glosario durante la fase SD_TERM_RESEARCH.
    *   **Distribución Visual (Tres Paneles):**
        1.  **Panel izquierdo (Estímulo — Sticky):** Texto fuente en inglés. No editable. Permanece visible durante toda la tarea.
        2.  **Panel central (Recursos — Sticky):** Acceso emulado a diccionarios bilingües de referencia certificados por la Guía Docente 252113T: IATE (terminología UE), UNTERM (terminología ONU), Diccionario panhispánico del español jurídico (DPEJ-RAE), Diccionario médico CUN, Glosario científico-técnico. El alumno consulta los recursos y arrastra términos al panel de glosario.
        3.  **Panel derecho (Glosario del alumno):** Zona de construcción del glosario bilingüe durante SD_TERM_RESEARCH. Los términos validados quedan disponibles durante SD_TRA_DRAFT como referencia no editable.
    *   **Motor:** EV-TRA-PRECISION-TECH. La IA audita que los términos del glosario del alumno procedan de fuentes de autoridad y se apliquen coherentemente en la traducción final.

*   W-TECH-CALC (Consola de Cálculo Procedimental):
    *   Uso: Ingenierías y Ciencias.
    *   Funciones: Renderizado MathJax, entrada multietapa, bloqueo de traza lógica.
*   W-CLIN-SCAN (Visor de Evidencia Diagnóstica):
    *   Uso: Medicina, Odontología, Veterinaria.
    *   Funciones: Zoom HD de imágenes médicas, herramientas de medida y marcado de hallazgos.
*   W-OBJ-STRIKE (Selector de Respuesta con Riesgo):
    *   Uso: Lenguas y Materias Troncales.
    *   Funciones: Sistema de descarte visual (tachado) e indicador de riesgo de penalización. Soporte para Media Assets (Audio/Imagen context).

## 2. LIBRERÍA DE COMPONENTES DISCURSIVOS Y DE ACCIÓN

*   W-HUM-TEXT (Editor de Exégesis Crítica):
    *   Uso: Humanidades, Artes y Norma Lingüística (NORM).
    *   Funciones: Pantalla dividida (Fuente vs Ensayo), gestor de citas por arrastre, contador de penalización formal.
    *   **Modo Revisión y Control de Cambios (Específico NORM):** Este modo permite la edición de un texto preexistente (estímulo) registrando cada intervención del alumno. El sistema diferencia visualmente entre inserciones, eliminaciones y sustituciones, permitiendo al motor de evaluación `EV-NORM-ANALYSIS` analizar la precisión de la corrección ortotipográfica y gramatical.
    *   **Directriz de Multimodalidad (Miguel Ángel):** Al interactuar con el editor, el sistema DEBE ofrecer obligatoriamente el selector de entrada:
        1. **Teclado Nativo:** Layout del idioma objetivo (ej. Árabe, Ruso).
        2. **Occidentalización:** Transliteración/Pinyin/Romaji para alfabetos no latinos.
        3. **Pad Virtual/Trazos:** Escritura manual digital (Caligrafía).
        4. **OCR/Captura:** Digitalización de manuscrito físico del alumno.
    *   **Modo TRA-LIT (SUB-LIN-TRA-LIT — SD_TRA_CREATIVE) [NUEVO v5.1 — 2026-04-21]:**
        El widget W-TRA-LIT-CREA referenciado en versiones anteriores de V06DOC_SUBARCHETYPES.md queda eliminado como widget independiente. La destreza SD_TRA_CREATIVE de SUB-LIN-TRA-LIT se mapea a W-HUM-TEXT en modo SPLIT_TEXT con la siguiente configuración específica:
        *   **Panel izquierdo (Estímulo — Sticky):** Texto literario fuente (poema, fragmento teatral o narrativo) en la lengua original (inglés). No editable. Permanece visible durante toda la fase de traducción.
        *   **Panel derecho (Producción — Editor):** W-HUM-TEXT en modo edición libre donde el alumno redacta su traducción literaria al español. Modos de entrada activos: teclado latino estándar + OCR/captura de manuscrito. El modo Occidentalización/Pinyin/Romaji y el Pad de Trazos quedan deshabilitados (no aplican para la combinación inglés→español).
        *   **Motor:** DRA-HOLO-LIT (Ejes 1, 2 y 3).
        *   **Nota de implementación:** Toda referencia a W-TRA-LIT-CREA en la constelación documental debe entenderse como alias de W-HUM-TEXT en Modo TRA-LIT.
    *   **Restricción de Entrada SUB-LIN-NORM [NUEVO v5.1 — 2026-04-21]:**
        La Directriz de Multimodalidad genérica de W-HUM-TEXT contempla los modos Occidentalización/Pinyin/Romaji y Pad de Trazos como opciones del selector. Para el subarquetipo SUB-LIN-NORM estas opciones **no tienen cabida**: la asignatura El Español Actual: Norma y Uso (2831111, Filología Hispánica, UGR) evalúa exclusivamente competencia en español, lengua de alfabeto latino. En el contexto SUB-LIN-NORM los únicos modos de entrada activos son:
        1.  **Teclado Latino Nativo:** Layout estándar del español con soporte de diacríticos propios (tildes, diéresis, eñe).
        2.  **OCR/Captura:** Digitalización de manuscrito físico del alumno.
        Los modos Occidentalización y Pad de Trazos quedan **deshabilitados** para este subarquetipo en todas sus fases (SD_CORPUS_ANALYSIS, SD_MORPH_ANTINORM, SD_ORTHO_PRESCRIPTIVE, SD_CRITICAL_NORM).

*   W-PROC-ACTION (Panel de Acción Crítica):
    *   Uso: Salud y Seguridad Industrial.
    *   Funciones: Checklist dinámico de seguridad, cronómetro ECOE, validación de pasos obligatorios.
*   W-COMM-DIALOG (Interfaz de Mediación Dialéctica):
    *   Uso: Lenguas, Derecho, Educación.
    *   Funciones: Grabadora de audio, chat interactivo con IA UniversIA, análisis de registro formal/informal. Soporte para entrada multimodal en el chat.
*   W-LAW-NAV (Navegador de Marco Normativo y Repositorios de Autoridad):
    *   Uso: Derecho, Ciencias Sociales y Lingüística (NORM).
    *   Funciones: Acceso a repositorio legal o normativo emulado, buscador de jurisprudencia o corpus y cita rápida por arrastre.
    *   **Modo Lingüístico (W-LAW-NAV-LING):** Adaptación específica de la interfaz para la consulta de los recursos de la RAE y la ASALE. El widget proporciona acceso emulado a:
        - **Buscador de Corpus (CORPES XXI / CREA):** Permite realizar consultas de frecuencias léxicas y gramaticales, devolviendo resultados por áreas lingüísticas (España, América, etc.) y por registros (académico, periodístico, coloquial).
        - **Consultas al DPD y DLE:** Interfaz de acceso rápido para la verificación de artículos normativos.
        - **Funcionalidad de Cita por Arrastre:** El alumno puede seleccionar un resultado de frecuencia o un fragmento de una norma y arrastrarlo directamente a la zona de justificación del editor de respuesta, generando una cita bibliográfica automática con el formato oficial de la UGR.

## 3. LIBRERÍA DE COMPONENTES LINGÜÍSTICOS ESTRUCTURALES (NUEVO V1.1)

*   W-TXT-CLOZE (Integrador de Huecos en Texto):
    *   Uso: Lenguas (Use of English) y Derecho (Completar escritos).
    *   Funciones: Renderizado de texto fluido con inputs incrustados. Soporta modo "Open" (Caja de texto) y "Select" (Dropdown en el hueco).
    *   **Directriz de Multimodalidad (Miguel Ángel):** Los inputs en modo "Open" deben heredar el selector de entrada multimodal (Teclado/Trazos/OCR) para garantizar la precisión caligráfica en lenguas Minor/Maior.
    *   **Mandato Minor (Bloqueo Caligráfico):** En el subarquetipo SUB-LIN-MINOR, cuando el `target_language_code` sea no-latino (Chino, Japonés, Árabe, Hebreo, Ruso), los inputs en modo "Open" quedan bloqueados EXCLUSIVAMENTE a **Pad de Trazos** u **OCR**. Se deshabilita el teclado occidental para forzar la evaluación de la grafía real.
*   W-MIX-MATCH (Matriz de Vinculación):
    *   Uso: Lenguas (Reading Headlines) y Ciencias (Concepto-Definición).
    *   Funciones: Arrastrar y soltar (Drag & Drop) o conectores visuales entre dos columnas.

## 4. ESTRATEGIA DE LAYOUT Y PANELES (UX OPTIMIZATION)

*   **W-LAYOUT-SIDE (Panel Lateral Persistente):**
    *   **Función:** Muestra el "Estímulo de Sección" (Texto de lectura, Supuesto de hecho, Texto para corrección normativa) de forma estática (Sticky) mientras el alumno hace scroll en las preguntas.
    *   **Justificación UX:** Evita el scroll vertical repetitivo ("Yo-Yo effect").
    *   **Contenido:** Estrictamente el material generado para el examen (Reading/Caso/Texto NORM). NUNCA los apuntes del alumno.

## 5. COMPONENTES ESPECIALIZADOS PHILO (UGR) [REFACTORIZADO SUBATÓMICO - FIDELIDAD 100% UGR]

*   **W-PHILO-IPA (Pad de Transcripción Fonética y Diacrónica):**
    *   **Función:** Interfaz de entrada de caracteres especializados para el análisis de la evolución fonética y la fonología histórica.
    *   **Especificaciones de Teclado Virtual:**
        - **Bloque Consonántico Medieval:** Símbolos para sibilantes medievales (s sorda/sonora, ts, dz), palatales (ɲ, ʎ, ʝ) y fricativas (β, ð, ɣ, ʃ, ʒ, θ).
        - **Bloque de Modificadores Diacrónicos:** Marcadores de cantidad vocálica latina (macrón, breve), acento prosódico y signos de evolución ( > , < , * ).
        - **Selector de Yods (I-IV):** Botonera rápida para clasificar el tipo de Yod detectada en el estadio evolutivo.
    *   **Multimodalidad:** Permite la entrada mediante teclado físico (mapeo de teclas rápidas) o Pad táctil para dispositivos móviles.

*   **W-PHILO-ECDO (Editor de Crítica Textual y Colación):**
    *   **Función:** Herramienta de trabajo para la fijación de textos (Ecdótica) basada en la Metodología de Alberto Blecua (UGR).
    *   **Configuración de Pantalla (Layout):**
        - **Modo Collatio (Split-View):** Visualización sincronizada de hasta tres fuentes simultáneas (ej. Códice A, Códice B y Manuscrito de Trabajo).
        - **Panel de Aparato Crítico:** Zona inferior para la redacción de variantes, adiciones, omisiones y correcciones (emendatio).
        - **Línea de Tiempo de Transmisión:** Visualización gráfica del Stemma Codicum (árbol genealógico de los textos) vinculado a las variantes seleccionadas.
    *   **Interactividad:** Permite el arrastre de fragmentos de texto entre testimonios para realizar el cotejo visual.

*   **W-PHILO-OCR-PALE (Digitalización y Resolución Paleográfica):**
    *   **Función:** Visor de alta precisión para el análisis de fuentes primarias (manuscritos e incunables).
    *   **Herramientas de Visión:**
        - **Lupa Magnética HD:** Zoom dinámico con capacidad de realce de tintas (Filtros de contraste y umbralización para lectura de pergaminos).
        - **Capa de Transcripción Flotante:** Permite escribir la transcripción literal directamente sobre la imagen del manuscrito, asegurando la correspondencia línea por línea.
    *   **Gestor de Braquigrafía (Resolución de Abreviaturas):**
        - Diccionario visual de abreviaturas medievales integrado. Al seleccionar un signo abreviativo (braquigrafía), el widget sugiere resoluciones basadas en la normativa de la Real Chancillería de Granada.
    *   **Multimodalidad (Miguel Ángel):** Soporta **OCR Predictivo** entrenado en letras góticas, cortesanas y humanísticas para asistir en la primera fase de la lectura.

## 6. LIBRERÍA TÉCNICA PARA EL MODELO INSTRUMENTAL (UGR 2026) [ADICIÓN QUIRÚRGICA - FIDELIDAD 100%]

Esta sección define el comportamiento técnico y visual de los componentes de interacción activados bajo el subarquetipo SUB-LIN-INSTR (CertAcles / CLM-UGR).

### W-AUDIO-INSTR (Reproductor de Audio de Rigor Institucional)
*   **Uso:** Destreza SD_LIST (Comprensión Auditiva).
*   **Comportamiento Técnico:**
    1. **Contador de Reproducciones:** Implementa un bloqueo hermético del botón "Play" tras la segunda reproducción completa. Envía un flag de estado al orquestador para invalidar intentos posteriores.
    2. **Inhibición de Navegación (Non-Scrubbing):** La barra de progreso es meramente informativa. Se deshabilita la interacción del alumno para adelantar o retrasar el audio, garantizando la audición lineal obligatoria en las pruebas de acreditación.
    3. **Persistencia de Estado:** En caso de refresco de página (F5), el widget recupera el número de reproducciones consumidas desde la base de datos de sesión.

### W-OCR-PRO (Módulo de Auditoría de Producción Manuscrita) [ACTUALIZADO v5.0]
*   **Uso:** Destreza SD_WRIT (Producción Escrita). En SUB-LIN-INSTR, la Mediación no constituye destreza independiente; este widget opera exclusivamente en el contexto de SD_WRIT cuando el encargo requiere producción manuscrita digitalizada.
*   **Funciones de Multimodalidad (Miguel Ángel):**
    1. **Captura y Pre-procesamiento:** Interfaz de cámara con guías de encuadre. Aplica algoritmos de normalización de imagen (contraste, brillo y eliminación de ruido) para optimizar la legibilidad del manuscrito. Emula el protocolo de examen presencial del CLM-UGR, donde la producción escrita se realiza obligatoriamente con bolígrafo.
    2. **Garantía de Autoría:** Registra metadatos de la captura (timestamp, geolocalización básica del dispositivo) para certificar que la producción es original y realizada dentro del tiempo estipulado para la sección.
    3. **Envío Estructurado:** El widget envía la imagen optimizada al motor de evaluación para su análisis por el motor OCR de alta fidelidad integrado con la IA (gemini-2.5-flash).

### W-MEDI-LAYOUT (Interfaz de Doble Panel para Transferencia) [ACTUALIZADO v5.0]
*   **Uso:** Componente auxiliar de SD_WRIT (Producción Escrita) en SUB-LIN-INSTR cuando el encargo de escritura incluye un estímulo fuente (gráfico, tabla de datos o texto especializado) que el alumno debe procesar e integrar en su producción. No constituye sección de examen autónoma en INSTR. Para los subarquetipos de Traducción (SUB-LIN-TRA-TECH / SUB-LIN-TRA-LIT), mantiene su función como interfaz principal de la fase documental y de transferencia.
*   **Distribución Visual (UX Design):**
    1. **Panel Estímulo (Sticky Left/Top):** Visualización persistente del material de origen (gráfico, tabla de datos o texto especializado). No permite edición por parte del alumno. Se mantiene visible durante toda la duración de la tarea de producción escrita.
    2. **Panel de Acción (Right/Bottom):** Editor de texto multimodal (W-HUM-TEXT) donde el alumno redacta su producción escrita. Soporta los cuatro modos de entrada del W-INSTR-SELECTOR (Teclado Nativo, Occidentalización, Pad de Trazos, OCR/Captura).
    3. **Interactividad de Cita:** Permite seleccionar fragmentos de datos del Panel Estímulo y arrastrarlos al Panel de Acción para generar una referencia fáctica precisa. Esta funcionalidad evalúa la capacidad del alumno para manejar e integrar fuentes de información técnica en su producción escrita.

### W-INSTR-SELECTOR (Selector Multimodal CertAcles)
*   **Comportamiento:** Componente global inyectado en todo widget de entrada de texto.
*   **Configuración Instrumental:** Ofrece obligatoriamente los cuatro modos de entrada (Teclado Nativo, Occidentalización, Pad de Trazos, OCR). En el subarquetipo instrumental, el modo "Teclado Nativo" fuerza el layout del idioma objetivo, deshabilitando correctores ortográficos del sistema operativo para auditar la competencia real del alumno.

## 7. LIBRERÍA TÉCNICA PARA EL MODELO MINOR — PAD CALIGRÁFICO (UGR 2026) [NUEVO v5.1 - FIDELIDAD 100% UGR]

Esta sección define el comportamiento técnico y visual del componente de entrada caligráfica activado bajo el subarquetipo SUB-LIN-MINOR para las lenguas no latinas (árabe, checo con diacríticos especiales, griego moderno, japonés), en cumplimiento de la competencia específica 31 del Verifica del Grado en Lenguas Modernas y sus Literaturas (Facultad de Filosofía y Letras, UGR — BOE 02/12/2024): "Conocer y dominar la caligrafía de la lengua minor".

### W-CALLI-PAD (Pad Caligráfico para Lenguas No Latinas — SUB-LIN-MINOR)
*   **Uso:** Destreza SD_PHON_GRAPH (Grafía y Fonética) en SUB-LIN-MINOR. Activado exclusivamente cuando el `target_language_code` corresponde a una lengua no latina: árabe (`ar`), japonés (`ja`), griego moderno (`el`), checo (`cs`). El widget queda deshabilitado para lenguas latinas (alemán, francés, inglés, polaco, portugués) donde el teclado nativo con diacríticos es suficiente.
*   **Modos de Entrada (Selector Obligatorio):**
    1.  **Pad de Trazos Digital:** Lienzo táctil calibrado para la escritura manual de caracteres. El alumno traza el carácter con el dedo o lápiz óptico. El sistema captura la secuencia completa de trazos (ductus) y la presión relativa de cada uno.
    2.  **OCR/Captura de Manuscrito Físico:** El alumno escribe el carácter en papel físico y lo digitaliza mediante la cámara del dispositivo. El sistema aplica preprocesamiento de imagen (normalización de contraste y brillo, umbralización) antes de pasarlo al motor de validación.
    *   **MANDATO DE BLOQUEO:** En SD_PHON_GRAPH para lenguas no latinas, se deshabilitan obligatoriamente el teclado occidental y la entrada por transliteración (Pinyin, Romaji, etc.) para forzar la evaluación de la grafía real. La occidentalización queda reservada únicamente para las tareas de transcripción a sistema vehicular (Tarea 1 de SD_PHON_GRAPH) cuando el enunciado lo especifique explícitamente.
*   **Motor de Validación de Ductus (Integrado con RBT-SHORT-LANG):**
    *   **Validación de Secuencia de Trazos:** El motor verifica que el orden y la dirección de los trazos del alumno se corresponden con el ductus normativo del carácter en la lengua objetivo. La referencia normativa por lengua es:
        - **Japonés (`ja`):** Norma del Ministerio de Educación japonés (MEXT) para el orden de trazos de kana y kanji de uso común (jōyō kanji).
        - **Árabe (`ar`):** Norma de escritura cursiva del árabe estándar moderno (MSA). Validación de la unión correcta de grafemas en posición inicial, medial y final de palabra.
        - **Griego moderno (`el`):** Norma de escritura minúscula del griego moderno estándar. Validación de la ligadura y el orden de trazos según la caligrafía escolar griega oficial.
        - **Checo (`cs`):** Validación de los diacríticos especiales (háček, čárka) como parte integral del trazo — la omisión o el posicionamiento erróneo de un diacrítico se considera falta caligráfica.
    *   **Validación de Integridad Grafémica:** El motor compara el carácter resultante con la base de patrones OCR de alta fidelidad (integrado con `gemini-2.5-flash`) para verificar la legibilidad y la corrección formal del grafema producido, independientemente del ductus.
    *   **Baremo de Penalización Caligráfica:**
        - **Ductus erróneo (orden/dirección de trazos incorrecto):** Penalización del 50% sobre la puntuación del ítem caligráfico. El carácter puede ser legible pero el ductus es evaluado de forma autónoma como competencia específica del título.
        - **Integridad grafémica comprometida (carácter ilegible o irreconocible):** FAIL_LOGIC: FATAL para ese ítem (nota 0.0). No aplica penalización parcial.
        - **Diacrítico omitido o mal posicionado (checo):** Computa como falta caligráfica con penalización del 50% sobre el ítem.
*   **UX y Accesibilidad:**
    *   **Referencia Visual Animada:** El widget muestra, antes del inicio de la tarea, una animación del ductus normativo del tipo de carácter a producir (stroke order animation), conforme al estándar de los materiales pedagógicos de la UGR para lenguas no latinas. Esta referencia es visible durante la fase de instrucciones pero se oculta durante la evaluación.
    *   **Área de Trazado Escalable:** El lienzo del pad se ajusta dinámicamente al tamaño de pantalla del dispositivo, garantizando un área mínima de 200×200 píxeles por carácter para asegurar la precisión del trazo en dispositivos móviles.
    *   **Borrador por Carácter:** El alumno dispone de un botón de borrado por carácter (no por trazo individual) para reintentar la producción caligráfica dentro del tiempo asignado a la tarea.

## 8. LIBRERÍA DE COMPONENTES PARA LA RAMA ARTES Y HUMANIDADES (NUEVO v5.2 — 2026-04-21)

Esta sección define los componentes de interacción activados bajo los subarquetipos de la Rama Artes y Humanidades que no tienen equivalente en las secciones anteriores.

### W-ART-IDENT (Visor de Identificación y Comentario Iconográfico — SUB-HUM-ART-HIST) [NUEVO v5.2 — 2026-04-21]
*   **Uso:** SUB-HUM-ART-HIST (Historia del Arte UGR). Instrumento nuclear de la prueba de reconocimiento iconográfico de imágenes, certificado como componente evaluativo del 50-60% de la calificación en el Grado en Historia del Arte UGR (Guías Docentes del Departamento de Historia del Arte, aprobadas 24/06/2025).
*   **Fuente de Certificación:** Guías Docentes de Iconografía (26511M2), Historia de los Estilos e Iconografía (2931114), Historia del Arte del Renacimiento (2931127) e Historia del Arte Antiguo y Medieval (2921124) — Departamento de Historia del Arte, UGR, curso 2025-2026.
*   **Distribución Visual (Tres Zonas):**
    1.  **Zona Superior (Imagen — Sticky):** Visor HD de la obra de arte con zoom dinámico (mínimo 400% sin pérdida de calidad). Herramienta de marcado iconográfico: el alumno puede seleccionar y etiquetar zonas de la imagen (personajes, atributos, escenas, elementos arquitectónicos) para referirse a ellas en su análisis. Los marcadores quedan numerados y vinculados al editor de análisis. La imagen permanece visible durante toda la tarea.
    2.  **Zona Media (Identificación Estructurada — Campos Fijos):** Formulario de identificación con los campos canónicos del análisis histórico-artístico UGR:
        - **Autor / Atribución:** Campo de texto libre con validación terminológica (nombre canónico del artista o "Anónimo / Escuela de...").
        - **Título / Denominación:** Campo de texto libre.
        - **Cronología:** Campo de texto libre (admite dataciones aproximadas: "ca.", "primer tercio del siglo XVI", etc.).
        - **Técnica y Soporte:** Campo de texto libre (ej. "Óleo sobre tabla", "Mármol de Carrara", "Fresco").
        - **Localización / Institución:** Campo de texto libre (museo, colección, in situ).
        - **Estilo / Período / Escuela:** Campo de texto libre con validación terminológica básica.
        - Motor de validación de identificación: **EV-ICON-ART** (ver V06DOC_BLOCKS.md).
    3.  **Zona Inferior (Análisis Libre — Editor):** W-HUM-TEXT en modo libre para el comentario formal e iconológico en tres niveles Panofsky:
        - **Nivel Pre-iconográfico:** Descripción formal de lo que se ve (líneas, colores, composición, figuras).
        - **Nivel Iconográfico:** Identificación de temas, motivos y fuentes literarias o religiosas.
        - **Nivel Iconológico:** Interpretación del significado intrínseco, el contexto histórico-cultural y el programa iconográfico en su conjunto.
        - El alumno puede referenciar los marcadores de zona colocados en el visor mediante sintaxis `[M1]`, `[M2]`, etc. para vincular la descripción con la imagen.
*   **Motor principal:** EV-ICON-ART.
*   **Layout:** FULL_STACK (las tres zonas se apilan verticalmente; la imagen es sticky al hacer scroll en el formulario y el editor).
*   **Nota de corrección formal:** La corrección ortotipográfica del análisis se evalúa mediante el baremo estándar DRA-HOLO de la Rama Humanidades. El rigor terminológico en los campos de identificación es condición necesaria para la superación del ítem.

### W-MUS-SCORE (Visor de Partitura y Análisis Musical — SUB-HUM-MUS) [NUEVO v5.2 — 2026-04-21]
*   **Uso:** SUB-HUM-MUS (Historia y Ciencias de la Música UGR). Instrumento nuclear del análisis en partitura, certificado como componente evaluativo del 50% de la calificación en el Grado en Historia y Ciencias de la Música UGR (Guía Docente de Análisis II: Clasicismo y Romanticismo, cód. 2991132, aprobada 23/06/2025, y Fundamentos de la Expresión Musical y su Evolución I, cód. 2991114, aprobada 25/06/2025).
*   **Fuente de Certificación:** Guías Docentes de Análisis II: Clasicismo y Romanticismo (2991132), Fundamentos de la Expresión Musical y su Evolución I (2991114) y Teoría y Práctica de la Interpretación Musical I (299112A) — Departamento de Historia y Ciencias de la Música, UGR, curso 2025-2026.
*   **Distribución Visual (Dos Paneles):**
    1.  **Panel izquierdo (Partitura — Sticky):** Visor HD de la partitura en imagen de alta resolución. Herramientas de anotación superpuestas directamente sobre la partitura:
        - **Marcado de Compases:** El alumno puede seleccionar rangos de compases y etiquetarlos (ej. "Exposición", "Desarrollo", "Cadencia auténtica perfecta").
        - **Etiquetado Armónico:** Inserción de símbolos de análisis armónico sobre los acordes (grados romanos: I, IV, V, ii, vii°; indicación de función tonal: T, S, D; identificación de cadencias).
        - **Marcado de Motivos:** El alumno puede trazar arcos o corchetes sobre fragmentos melódicos para identificar motivos, temas y su transformación.
        - **Indicación de Forma:** Botonera rápida para etiquetar secciones formales (A, B, A', Coda, Puente, etc.) conforme a la terminología estándar de LaRue (1989) y Cook (1991), referencias bibliográficas del Grado en Historia y Ciencias de la Música UGR.
        - La partitura permanece visible y anotable durante toda la tarea.
    2.  **Panel derecho (Análisis Musicológico — Editor):** W-HUM-TEXT en modo libre para el comentario analítico formal. El alumno redacta el análisis estructurado referenciando los marcadores de la partitura. Soporta notación musical básica mediante símbolos Unicode estándar (bemoles ♭, sostenidos ♯, becuadros ♮, corcheas ♩).
*   **Motor de Identificación Auditiva (Complementario):** Cuando el subarquetipo activa la destreza SD_MUS_LIST (identificación auditiva), se integra el widget **W-AUDIO-INSTR** con configuración MUS: el número de reproducciones por fragmento se define por la estrategia de la asignatura (no fijo en 2 como en INSTR — variable según la guía docente de la asignatura fuente). Motor: **EV-MUS-ANAL**.
*   **Motor principal:** EV-MUS-ANAL.
*   **Layout:** SPLIT_TEXT (partitura en panel izquierdo sticky; editor de análisis en panel derecho).

### W-PORTFOLIO (Portafolio Digital de Proceso Creativo — SUB-HUM-ART-CREA) [NUEVO v5.2 — 2026-04-21]
*   **Uso:** SUB-HUM-ART-CREA (Bellas Artes UGR). Instrumento de emulación parcial certificada del portafolio/dossier de proceso creativo, que constituye el 60-70% de la calificación en el Grado en Bellas Artes UGR (Guías Docentes de Arte y Cuerpo, cód. 26011D1, y Principios Básicos de la Pintura, cód. 2601114, aprobadas en junio de 2025).
*   **Declaración de Emulación Parcial Certificada [VINCULANTE]:** CampuStudiOnline emula exclusivamente las destrezas evaluables en entorno digital del Grado en Bellas Artes UGR. Las destrezas de taller presencial (técnica matérica directa, modelado físico, fundición escultórica, grabado tradicional) quedan fuera del alcance de la plataforma y se documentan explícitamente como no emulables. El widget evalúa: (a) el proceso creativo documentado mediante imágenes digitalizadas; (b) la memoria escrita de proceso; (c) el análisis crítico de la obra propia.
*   **Fuente de Certificación:** Guías Docentes de Arte y Cuerpo (26011D1) y Principios Básicos de la Pintura (2601114) — Facultad de Bellas Artes, UGR, curso 2025-2026.
*   **Distribución Visual (Tres Zonas):**
    1.  **Zona Superior (Galería de Proceso — Carga de Imágenes):** Interfaz de carga de imágenes (capturas del proceso creativo en sus distintas fases: bocetos, estudios preparatorios, estados intermedios de la obra, obra final). El alumno carga entre 5 y 15 imágenes ordenadas cronológicamente. Cada imagen admite un pie de foto descriptivo (máx. 150 palabras) que documenta la fase del proceso y las decisiones técnicas adoptadas.
        - Formatos admitidos: JPG, PNG, PDF (para obras en papel).
        - La plataforma aplica validación básica de carga (tamaño máximo por imagen: 10 MB; mínimo de 5 imágenes para habilitar el envío).
    2.  **Zona Media (Memoria de Proceso — Editor):** W-HUM-TEXT en modo libre para la redacción de la memoria de proceso creativo. La memoria debe incluir: descripción del proyecto y su intención artística, materiales y técnicas empleados, referentes artísticos y bibliográficos, decisiones creativas adoptadas y justificación de las mismas. Extensión mínima: 500 palabras. Motor: DRA-HOLO (rúbrica analítica holística adaptada al contexto de Bellas Artes).
    3.  **Zona Inferior (Análisis Crítico — Editor):** W-HUM-TEXT en modo libre para el análisis crítico de la obra propia en relación con el contexto artístico contemporáneo y los contenidos de la asignatura. El alumno contextualiza su producción dentro de los debates artísticos actuales y la bibliografía del programa. Extensión mínima: 300 palabras.
*   **Motor principal:** DRA-HOLO (configuración ART-CREA — ver V06DOC_BLOCKS.md).
*   **Layout:** FULL_STACK (las tres zonas se apilan verticalmente con navegación por pestañas entre Galería, Memoria y Análisis Crítico).
*   **Nota de restricción de entrada:** Los modos Occidentalización y Pad de Trazos de W-HUM-TEXT quedan deshabilitados en este widget (el castellano es el idioma vehicular obligatorio en Bellas Artes UGR). Modos activos: Teclado Latino Nativo y OCR/Captura.
