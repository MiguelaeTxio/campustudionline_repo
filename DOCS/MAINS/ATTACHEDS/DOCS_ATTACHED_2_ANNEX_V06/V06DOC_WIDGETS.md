# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/DOCS_ATTACHED_2_ANNEX_V06/V06DOC_WIDGETS.md
# V06DOC_WIDGETS - CATÁLOGO DE COMPONENTES DE INTERFAZ (V1.2 - REFACTORIZACIÓN UGR)

## 1. LIBRERÍA DE COMPONENTES TÉCNICOS\n\n*   **W-TRA-CAT-EMULATOR (Simulador de Herramienta TAO) [NUEVO 2026]**\n    *   **Uso:** Traducción Profesional (SUB-LIN-TRA-TECH).\n    *   **Funciones:** Panel de traducción segmentada con ventana de sugerencias de memoria y glosario obligatorio. Audita el uso de la terminología sugerida.

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

### W-OCR-PRO (Módulo de Auditoría de Producción Manuscrita)
*   **Uso:** Destreza SD_WRIT (Producción Escrita) y SD_MEDI (Mediación).
*   **Funciones de Multimodalidad (Miguel Ángel):**
    1. **Captura y Pre-procesamiento:** Interfaz de cámara con guías de encuadre. Aplica algoritmos de normalización de imagen (contraste, brillo y eliminación de ruido) para optimizar la legibilidad del manuscrito.
    2. **Garantía de Autoría:** Registra metadatos de la captura (timestamp, geolocalización básica del dispositivo) para certificar que la producción es original y realizada en el tiempo estipulado para la sección.
    3. **Envío Estructurado:** El widget envía la imagen optimizada al motor de evaluación para su análisis por el motor OCR de alta fidelidad integrado con la IA.

### W-MEDI-LAYOUT (Interfaz de Doble Panel para Transferencia)
*   **Uso:** Destreza SD_MEDI (Mediación Lingüística).
*   **Distribución Visual (UX Design):**
    1. **Panel Estímulo (Sticky Left/Top):** Visualización persistente del material de origen (gráfico, tabla de datos o texto especializado). No permite edición.
    2. **Panel de Acción (Right/Bottom):** Editor de texto multimodal (W-HUM-TEXT) donde el alumno realiza la síntesis o adaptación.
    3. **Interactividad de Cita:** Permite seleccionar fragmentos de datos en el Panel Estímulo y arrastrarlos al Panel de Acción para generar una cita fáctica precisa, evaluando la capacidad del alumno para manejar fuentes de información técnica.

### W-INSTR-SELECTOR (Selector Multimodal CertAcles)
*   **Comportamiento:** Componente global inyectado en todo widget de entrada de texto.
*   **Configuración Instrumental:** Ofrece obligatoriamente los cuatro modos de entrada (Teclado Nativo, Occidentalización, Pad de Trazos, OCR). En el subarquetipo instrumental, el modo "Teclado Nativo" fuerza el layout del idioma objetivo, deshabilitando correctores ortográficos del sistema operativo para auditar la competencia real del alumno.
