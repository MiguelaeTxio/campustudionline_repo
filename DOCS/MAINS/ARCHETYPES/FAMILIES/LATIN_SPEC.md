# ESPECIFICACIÓN TÉCNICA: FAMILIA LATINA (EN, FR, IT, PT, DE, ES)
# Documento Operativo de Ingeniería de Evaluación

## 1. PARÁMETROS DE CARGA Y LÓGICA DE DATOS
- **Métrica de Unidad:** Palabra (Token).
- **Definición de Token:** Cadena de caracteres delimitada por espacios en blanco o signos de puntuación.
- **Factor de Dificultad:** Longitud media de palabra (WL) y densidad de conectores lógicos por párrafo.
- **Codificación:** UTF-8 (Strict).

## 2. REQUERIMIENTOS DE INTERFAZ (UI)
- **Dirección del Texto:** LTR (Left-to-Right).
- **Mapa de Caracteres Especiales:** Obligatorio para REQ_INPUT en lenguas con diacríticos extendidos (ej: ç, ß, œ, à, é).
- **Tipografía:** Sans-serif de alta legibilidad (mínimo 16px para textos de lectura).

## 3. ESPECIFICACIÓN DE BLOQUES DE COMPETENCIA
### 3.1. Comprensión Lectora (Reading)
- **Extensión:** 
  - A1/A2: 150 - 250 palabras.
  - B1/B2: 450 - 600 palabras.
  - C1/C2: 800 - 1200 palabras.
- **Tipología de Tarea:** Opción múltiple (3-4 opciones), Reintegro de frases (Gapped Text), Emparejamiento de títulos.

### 3.2. Comprensión Auditiva (Listening)
- **Audio:** MP3/AAC 128kbps mínimo.
- **Intentos:** Configuración estándar de 2 escuchas.
- **Tarea:** Identificación de información específica y toma de notas (Gap-fill).

### 3.3. Expresión Escrita (Writing)
- **Widget:** REQ_DUAL.
- **Lógica de Corrección IA:** Evaluación de adecuación (registro), coherencia, cohesión y corrección gramatical/ortográfica.
- **Extensión Target:** Definida por el Nivel CEFR (desde 30 hasta 350 palabras).

### 3.4. Expresión Oral (Speaking)
- **Widget:** REQ_REC (The Cassette).
- **Lógica de Corrección IA:** Análisis de fluidez, rango léxico y entonación fonética.

## 4. FOCO PEDAGÓGICO DE LA IA (PROMPT DATA)
La IA debe priorizar en esta familia:
1. Morfosintaxis: Uso correcto de tiempos verbales, concordancia y declinaciones (en Alemán).
2. Léxico: Uso de "Phrasal Verbs" (EN), "Faux Amis" (FR) y colocaciones idiomáticas según nivel.
3. Cohesión: Uso de marcadores del discurso y conectores subordinantes.
