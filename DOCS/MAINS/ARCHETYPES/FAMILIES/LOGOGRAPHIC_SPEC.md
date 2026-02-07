# ESPECIFICACIÓN TÉCNICA: FAMILIA LOGOGRÁFICA (ZH, JA)
# Documento Operativo de Ingeniería de Evaluación

## 1. PARÁMETROS DE CARGA Y LÓGICA DE DATOS
- **Métrica de Unidad:** Carácter (Logograma).
- **Definición de Unidad:** Glifo individual con carga semántica independiente.
- **Factor de Dificultad:** Densidad de trazos y nivel de abstracción del radical.
- **Codificación:** UTF-8 (Strict Unicode).

## 2. REQUERIMIENTOS DE INTERFAZ (UI)
- **Dirección del Texto:** LTR (Horizontal estándar UGR).
- **Tamaño de Fuente:** Mínimo 18px (Cuerpo de texto) y 22px (Ítems de examen) para legibilidad de trazos.
- **Input de Datos:** 
  - Digital: Soporte para IME (Pinyin/Romaji).
  - Analógico: Widget REQ_DUAL forzado para captura de caligrafía.

## 3. ESPECIFICACIÓN DE BLOQUES DE COMPETENCIA
### 3.1. Comprensión Lectora (Reading)
- **Extensión:** 
  - A1/A2: 80 - 150 caracteres.
  - B1/B2: 350 - 500 caracteres (Sin ayuda fonética).
  - C1/C2: 600 - 900 caracteres (Uso de jianzi/kanji complejo).
- **Tipología de Tarea:** Asociación concepto-carácter (REQ_MATCH) e identificación de sinónimos/antónimos logográficos.

### 3.2. Comprensión Auditiva (Listening)
- **Foco Crítico:** Discriminación Tonal (Chino) y Acento de Tono (Japonés).
- **Tarea:** Identificación del carácter correcto entre distractores homófonos.
- **Widget:** Player V3 (Fidelidad de audio obligatoria).

### 3.3. Expresión Escrita (Writing)
- **Widget:** REQ_DUAL (MODO FORZADO). 
- **Protocolo de Validación:** El sistema exige la subida de una imagen del manuscrito.
- **Lógica de Corrección IA:** Evaluación del orden de trazos, proporciones del carácter y precisión de los radicales.

### 3.4. Expresión Oral (Speaking)
- **Widget:** REQ_REC (The Cassette).
- **Lógica de Corrección IA:** Prioridad absoluta a la curva tonal y la correcta pronunciación de las sílabas cerradas.

## 4. FOCO PEDAGÓGICO DE LA IA (PROMPT DATA)
La IA debe priorizar en esta familia:
1. Semántica Visual: Relación directa entre el radical y el significado.
2. Precisión Tonal: Detección de errores en los 4 tonos (ZH) o entonación melódica (JA).
3. Caligrafía: Validación del equilibrio estético y estructural del logograma.
