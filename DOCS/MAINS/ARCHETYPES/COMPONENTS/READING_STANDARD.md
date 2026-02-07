# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/COMPONENTS/READING_STANDARD.md
# ESTÁNDAR TÉCNICO: COMPRENSIÓN LECTORA (READING)
# Componente de Evaluación de Competencia Textual

## 1. OBJETIVO TÉCNICO
Evaluar la capacidad del alumno para decodificar, procesar e inferir información a partir de estímulos visuales/textuales (SRC_TXT).

## 2. TAXONOMÍA DE TAREAS (TIPO UGR)

### 2.1. TAREA DE COMPRENSIÓN GLOBAL (GIST)
- **Lógica:** Selección de la idea principal o propósito del autor entre distractores semánticos.
- **Widget:** REQ_RADIO.
- **Parámetro IA:** Generar 3-4 opciones (A, B, C) donde solo una sea verdadera según el texto y las otras sean interpretaciones parciales o falsas.

### 2.2. TAREA DE COMPRENSIÓN ESPECÍFICA (SCANNING)
- **Lógica:** Localización de datos concretos (fechas, nombres, hechos).
- **Widget:** REQ_RADIO o REQ_MATCH.
- **Parámetro IA:** Inyectar una pregunta que obligue a la lectura detallada de un párrafo específico.

### 2.3. TAREA DE EMPAREJAMIENTO (MATCHING)
- **Lógica:** Relacionar enunciados (opiniones/perfiles) con fragmentos de texto o diferentes textos cortos.
- **Widget:** REQ_MATCH.
- **Parámetro IA:** Generar una matriz de 5-8 enunciados y 4-5 fuentes de información.

### 2.4. TAREA DE REINTEGRACIÓN (GAPPED TEXT)
- **Lógica:** Reinsertar frases extraídas en sus huecos correspondientes para evaluar la cohesión y coherencia.
- **Widget:** REQ_ORDER o REQ_DROP.
- **Parámetro IA:** El texto debe tener 5 huecos. Se deben proporcionar 7 fragmentos (5 correctos + 2 distractores).

## 3. REQUERIMIENTOS DE INTERFAZ (UI)
- **Sincronización:** El texto de estímulo (reading_stimulus) debe permanecer visible en un panel lateral (Sticky) mientras el alumno navega por las preguntas.
- **Resaltado:** Capacidad técnica para resaltar fragmentos del texto si la tarea lo requiere (ej: "Analiza la palabra en negrita").
- **Tipografía:** Renderizado adaptativo según la Familia Lingüística (ver SPEC de Familia).

## 4. PROTOCOLO DE GENERACIÓN IA (PHASE B)
Para cada ítem de Reading, la IA debe recibir:
1. El fragmento de texto exacto (filtrado por rango).
2. El tipo de tarea técnica.
3. El nivel de dificultad (Métrica de longitud y complejidad léxica).
4. El esquema JSON de salida obligatorio: {"question_text": "...", "options": [...], "model_answer": "..."}.

## 5. VALIDACIÓN PEDAGÓGICA
- Prohibido generar preguntas cuyas respuestas no se encuentren explícita o implícitamente en el texto proporcionado (Evitar conocimiento general externo).
