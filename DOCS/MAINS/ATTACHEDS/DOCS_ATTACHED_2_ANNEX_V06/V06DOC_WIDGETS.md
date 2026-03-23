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
