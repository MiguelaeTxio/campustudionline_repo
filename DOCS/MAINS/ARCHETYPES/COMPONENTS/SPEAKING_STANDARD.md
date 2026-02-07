# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/COMPONENTS/SPEAKING_STANDARD.md
# ESTÁNDAR TÉCNICO: EXPRESIÓN E INTERACCIÓN ORAL (SPEAKING)
# Componente de Evaluación de Competencia Productiva Oral

## 1. OBJETIVO TÉCNICO
Evaluar la capacidad comunicativa oral del alumno, incluyendo la fluidez, la corrección fonética, la entonación y la capacidad de interacción en situaciones simuladas.

## 2. TAXONOMÍA DE TAREAS (ESTÁNDAR UGR/ACLES)

### 2.1. ENTREVISTA PERSONAL (INTERVIEW)
- **Lógica:** Respuesta a preguntas directas sobre el entorno personal, académico o profesional del alumno.
- **Estímulo:** Pregunta textual o audio corto (examinador virtual).
- **Duración:** 30 - 60 segundos por respuesta.

### 2.2. DESCRIPCIÓN Y COMPARACIÓN (LONG TURN)
- **Lógica:** Descripción detallada de una o dos imágenes relacionadas, estableciendo comparaciones y expresando opiniones.
- **Estímulo:** SRC_IMG (Una o varias fotografías).
- **Duración:** 2 - 3 minutos de discurso ininterrumpido.

### 2.3. TAREA COLABORATIVA / NEGOCIACIÓN (SIMULATION)
- **Lógica:** Toma de decisiones basada en un escenario problemático con diferentes opciones.
- **Estímulo:** SRC_HYB (Texto del escenario + opciones visuales).
- **Foco:** Capacidad de argumentar, sugerir y llegar a un acuerdo.

## 3. REQUERIMIENTOS DE INTERFAZ (UI)
- **Widget Obligatorio:** REQ_REC (Recorder V3 - "The Cassette").
- **Flujo Operativo:** El sistema debe habilitar el botón REC solo tras la carga completa del estímulo.
- **Seguridad:** Monitor de nivel de audio (vu-meter) para asegurar que el micrófono está activo antes de la grabación definitiva.

## 4. CRITERIOS DE EVALUACIÓN (LÓGICA IA DE CORRECCIÓN)
La IA debe analizar el archivo de audio basándose en:
1. Fluidez y Coherencia: Capacidad de mantener el discurso sin pausas excesivas.
2. Rango Léxico: Uso de vocabulario variado y preciso.
3. Control Gramatical: Precisión en las estructuras habladas.
4. Pronunciación: Claridad, entonación y respeto a los fonemas críticos de la familia (ej: Tonos en Chino, Vocales largas en Alemán).

## 5. PROTOCOLO DE GENERACIÓN IA (PHASE B)
Para generar una tarea de Speaking, la IA recibe:
1. El tipo de tarea técnica.
2. El estímulo visual o textual asociado.
3. El tiempo de producción objetivo.
4. El esquema JSON: {"question_text": "...", "recording_label": "Instrucción de grabación", "model_answer": "Resumen de puntos clave esperados"}.
