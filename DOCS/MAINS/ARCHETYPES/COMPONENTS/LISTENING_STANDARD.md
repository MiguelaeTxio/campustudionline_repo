# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/COMPONENTS/LISTENING_STANDARD.md
# ESTÁNDAR TÉCNICO: COMPRENSIÓN AUDITIVA (LISTENING)
# Componente de Evaluación de Competencia Oral Receptiva

## 1. OBJETIVO TÉCNICO
Evaluar la capacidad del alumno para procesar, discriminar e interpretar información a partir de estímulos sonoros (SRC_AUD).

## 2. TAXONOMÍA DE TAREAS (TIPO UGR/ACLES)

### 2.1. COMPRENSIÓN GENERAL (IDENTIFICACIÓN)
- **Lógica:** Determinar el contexto, la relación entre hablantes o el propósito del mensaje.
- **Estímulo:** Monólogos o diálogos cortos (30-60 segundos).
- **Widget de Respuesta:** REQ_RADIO.

### 2.2. COMPRENSIÓN ESPECÍFICA (DETAIL)
- **Lógica:** Capturar datos concretos, opiniones o inferencias en un discurso extenso.
- **Estímulo:** Entrevistas o reportajes (2-4 minutos).
- **Widget de Respuesta:** REQ_RADIO.

### 2.3. TOMA DE NOTAS / COMPLETADO (GAP-FILL)
- **Lógica:** Extraer palabras exactas, cifras o nombres para completar un resumen o esquema.
- **Estímulo:** Noticia, fragmento de conferencia o discurso informativo.
- **Widget de Respuesta:** REQ_INPUT.
- **Parámetro IA:** El modelo de respuesta (model_answer) debe incluir variantes aceptables (ej: números en cifra o letra).

## 3. ESPECIFICACIÓN DEL REPRODUCTOR (PLAYER V3)
- **Control de Intentos:** Limitador físico configurado a 2 escuchas para exámenes de acreditación.
- **Inhibición de Avance:** Prohibición técnica de "seek" (adelantar) durante la primera reproducción para garantizar la escucha lineal.
- **Persistencia de Estado:** El sistema debe registrar si el audio ha sido reproducido y cuántos intentos restan.

## 4. LÓGICA DE DATOS Y PERSISTENCIA
- **Campo Transcript:** Todo objeto de escucha debe incluir el texto íntegro del audio. Este campo es invisible para el alumno pero obligatorio para la IA de corrección.
- **Fidelidad:** Audio en formato MP3/AAC con bitrate suficiente para distinguir fonemas críticos (especialmente en familias Logográficas y Semíticas).

## 5. PROTOCOLO DE GENERACIÓN IA (PHASE B)
Para generar un ítem de Listening, la IA recibe:
1. El transcript del audio.
2. La tarea técnica (Gist/Detail/Gap-fill).
3. La restricción de nivel (velocidad, ruido de fondo, complejidad léxica).
4. El esquema JSON de salida: {"question_text": "...", "options": [...], "model_answer": "..."}.
