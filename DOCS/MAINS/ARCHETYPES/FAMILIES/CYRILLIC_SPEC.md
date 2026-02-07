# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/FAMILIES/CYRILLIC_SPEC.md
# ESPECIFICACIÓN TÉCNICA: FAMILIA CIRÍLICA (RU, UK, BG)
# Documento Operativo de Ingeniería de Evaluación

## 1. PARÁMETROS DE CARGA Y LÓGICA DE DATOS
- **Métrica de Unidad:** Palabra (Token Cirílico).
- **Definición de Unidad:** Cadena de caracteres del alfabeto cirílico delimitada por espacios.
- **Factor de Dificultad:** Complejidad de la declinación (6 casos estándar) y uso de verbos de movimiento con prefijos.
- **Codificación:** UTF-8 (Strict Unicode Cyrillic).

## 2. REQUERIMIENTOS DE INTERFAZ (UI)
- **Dirección del Texto:** LTR (Left-to-Right).
- **Tipografía:** Obligatorio el uso de fuentes con glifos cirílicos completos (ej: Roboto, Open Sans Cyrillic) para evitar el renderizado defectuoso de caracteres.
- **Input de Datos:** 
  - Digital: Mapa de caracteres virtual integrado en REQ_INPUT para facilitar la escritura sin teclado físico cirílico.
  - Analógico: Widget REQ_DUAL para validación de escritura cursiva (el cursivo cirílico difiere significativamente del de imprenta).

## 3. ESPECIFICACIÓN DE BLOQUES DE COMPETENCIA
### 3.1. Comprensión Lectora (Reading)
- **Extensión:** 
  - A1/A2: 150 - 300 palabras.
  - B1/B2: 500 - 700 palabras.
  - C1/C2: 900 - 1200 palabras (Textos literarios clásicos o prensa técnica).
- **Tipología de Tarea:** Identificación de funciones sintácticas basadas en casos y comprensión de la reducción vocálica.

### 3.2. Comprensión Auditiva (Listening)
- **Foco Crítico:** Identificación del **Acento Tónico Móvil** (el cambio de sílaba tónica altera el significado de la palabra).
- **Tarea:** Marcar la posición del acento escuchado sobre una lista de palabras escritas o identificar palabras homógrafas por su sonido.
- **Widget:** Player V3.

### 3.3. Expresión Escrita (Writing)
- **Widget:** REQ_DUAL. 
- **Lógica de Corrección IA:** Validación estricta de las terminaciones de caso (declension endings) y la concordancia de género/número.
- **Nota Técnica:** La IA debe ser capaz de corregir tanto el texto digital como el manuscrito subido.

### 3.4. Expresión Oral (Speaking)
- **Widget:** REQ_REC (The Cassette).
- **Lógica de Corrección IA:** Evaluación de la palatalización de consonantes y la correcta reducción de las vocales átonas (ej: "o" pronunciada como "a" en ruso).

## 4. FOCO PEDAGÓGICO DE LA IA (PROMPT DATA)
La IA debe priorizar en esta familia:
1. Sistema de Casos: Correcta aplicación de las desinencias según la función gramatical.
2. Aspecto Verbal: Distinción entre verbos perfectivos e imperfectivos en contextos narrativos.
3. Fonética y Acentuación: Detección de errores rítmicos que dificulten la comprensión por parte de un nativo.
