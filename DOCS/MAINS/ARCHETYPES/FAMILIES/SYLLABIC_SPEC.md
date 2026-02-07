# ESPECIFICACIÓN TÉCNICA: FAMILIA SILÁBICA (KO, JA-KANA)
# Documento Operativo de Ingeniería de Evaluación

## 1. PARÁMETROS DE CARGA Y LÓGICA DE DATOS
- **Métrica de Unidad:** Bloque Silábico (Hangeul) / Carácter fonético (Kana).
- **Definición de Unidad:** Combinación de grafemas (Jamo) que forman una unidad de sonido independiente.
- **Factor de Dificultad:** Complejidad de la estructura del bloque (C+V vs C+V+C) y uso de partículas gramaticales.
- **Codificación:** UTF-8 (Support for Hangeul Syllables / Hiragana / Katakana).

## 2. REQUERIMIENTOS DE INTERFAZ (UI)
- **Dirección del Texto:** LTR (Horizontal).
- **Tipografía:** Fuentes con soporte Unicode específico para silabarios orientales que garanticen la separación visual de bloques.
- **Input de Datos:** 
  - Digital: Teclado silábico virtual o conversión fonética (Romanización).
  - Analógico: Widget REQ_DUAL para captura de caligrafía silábica.

## 3. ESPECIFICACIÓN DE BLOQUES DE COMPETENCIA
### 3.1. Comprensión Lectora (Reading)
- **Extensión:** 
  - A1/A2: 100 - 200 bloques/caracteres.
  - B1/B2: 400 - 600 bloques/caracteres.
- **Tipología de Tarea:** Asociación fonema-bloque (REQ_MATCH) e identificación de estructuras aglutinantes.

### 3.2. Comprensión Auditiva (Listening)
- **Foco Crítico:** Distinción de consonantes similares (tensas, aspiradas, simples en Coreano).
- **Tarea:** Transcripción de dictados cortos o selección del bloque silábico escuchado.
- **Widget:** Player V3.

### 3.3. Expresión Escrita (Writing)
- **Widget:** REQ_DUAL.
- **Protocolo de Validación:** El sistema debe permitir la subida de foto para validar la correcta formación del bloque (proporción entre consonante y vocal).
- **Lógica de Corrección IA:** Evaluación del uso de partículas de caso y cohesión entre bloques.

### 3.4. Expresión Oral (Speaking)
- **Widget:** REQ_REC (The Cassette).
- **Lógica de Corrección IA:** Análisis de la articulación silábica y la entonación rítmica de las oraciones.

## 4. FOCO PEDAGÓGICO DE LA IA (PROMPT DATA)
La IA debe priorizar en esta familia:
1. Fonética Aplicada: Correspondencia exacta entre el símbolo y el sonido silábico.
2. Aglutinación: Correcto uso de sufijos y partículas pegadas a la raíz silábica.
3. Estructura de Bloque: Validación de la correcta posición de los elementos dentro del cuadrado imaginario del carácter.
