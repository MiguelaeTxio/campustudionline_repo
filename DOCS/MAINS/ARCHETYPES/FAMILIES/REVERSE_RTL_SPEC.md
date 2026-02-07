# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/FAMILIES/REVERSE_RTL_SPEC.md
# ESPECIFICACIÓN TÉCNICA: FAMILIA SEMÍTICA / RTL (AR, HE)
# Documento Operativo de Ingeniería de Evaluación

## 1. PARÁMETROS DE CARGA Y LÓGICA DE DATOS
- **Métrica de Unidad:** Palabra (Token RTL).
- **Definición de Unidad:** Cadena de caracteres ligada (Árabe) o aislada (Hebreo) delimitada por espacios, procesada de derecha a izquierda.
- **Factor de Dificultad:** Presencia/Ausencia de vocalización (Harakat/Niqqud) y complejidad de la derivación de la raíz trilítera.
- **Codificación:** UTF-8 (Strict Unicode con soporte Bidi).

## 2. REQUERIMIENTOS DE INTERFAZ (UI)
- **Dirección del Texto:** RTL (Right-to-Left).
- **Ajustes Críticos:** Inyección obligatoria de CSS_RTL_OVERRIDE para invertir alineación, cursores, barras de scroll y posición de iconos de validación.
- **Input de Datos:** 
  - Digital: Teclado virtual específico integrado para evitar el mapeo incorrecto de caracteres en sistemas operativos occidentales.
  - Analógico: Widget REQ_DUAL con soporte de previsualización RTL.

## 3. ESPECIFICACIÓN DE BLOQUES DE COMPETENCIA
### 3.1. Comprensión Lectora (Reading)
- **Extensión:** 
  - A1/A2: 100 - 150 palabras (Vocalización completa).
  - B1/B2: 300 - 450 palabras (Vocalización parcial/nula).
  - C1/C2: 600 - 800 palabras (Textos clásicos o periodísticos complejos).
- **Tipología de Tarea:** Análisis morfosintáctico de raíces y completado de textos sin vocales escritas.

### 3.2. Comprensión Auditiva (Listening)
- **Foco Crítico:** Identificación de la vocalización fonética y discriminación de sonidos enfáticos y guturales (Ej: Qaf vs Kaf).
- **Tarea:** Marcar la estructura vocálica correcta sobre un texto consonántico (Harakat placement).
- **Widget:** Player V3.

### 3.3. Expresión Escrita (Writing)
- **Widget:** REQ_DUAL. 
- **Protocolo de Validación:** Soporte para caligrafía ligada (Árabe) asegurando que el sistema no rompa las ligaduras al renderizar.
- **Lógica de Corrección IA:** Evaluación de la ortografía radical y la correcta aplicación de la declinación nominal (I’rab).

### 3.4. Expresión Oral (Speaking)
- **Widget:** REQ_REC (The Cassette).
- **Lógica de Corrección IA:** Análisis de la pronunciación de fonemas específicos y el respeto a la cantidad vocálica (vocales largas vs cortas).

## 4. FOCO PEDAGÓGICO DE LA IA (PROMPT DATA)
La IA debe priorizar en esta familia:
1. Morfología de Raíces: Capacidad de derivar formas verbales a partir del esquema trilítero.
2. Sintaxis de Inversión: Correcto orden de palabras en la estructura VSO (Verbo-Sujeto-Objeto) o Nominal.
3. Vocalización Implícita: Capacidad del alumno para leer e interpretar el sentido sin apoyo de marcas vocálicas gráficas.
