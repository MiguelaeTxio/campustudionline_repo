# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ARCHETYPES/COMPONENTS/WRITING_STANDARD.md
# ESTÁNDAR TÉCNICO: EXPRESIÓN E INTERACCIÓN ESCRITA (WRITING)
# Componente de Evaluación de Competencia Productiva Textual

## 1. OBJETIVO TÉCNICO
Evaluar la capacidad del alumno para producir textos coherentes, cohesionados y adecuados a un contexto específico en el idioma objetivo.

## 2. TAXONOMÍA DE TAREAS (ESTÁNDAR UGR/ACLES)

### 2.1. INTERACCIÓN ESCRITA (TRANSACTIONAL)
- **Lógica:** Respuesta a un estímulo previo (email, anuncio, invitación).
- **Métrica:** 80 - 120 palabras (Latina) / 40 - 60 caracteres (Logográfica).
- **Foco:** Adecuación al registro (formal/informal) y cumplimiento de puntos de información obligatorios.

### 2.2. PRODUCCIÓN ESCRITA (DISCURSIVE)
- **Lógica:** Redacción de un ensayo, artículo de opinión o reseña basada en una tesis o pregunta abierta.
- **Métrica:** 150 - 250 palabras (Latina) / 100 - 180 caracteres (Logográfica).
- **Foco:** Argumentación, uso de conectores lógicos y riqueza de vocabulario.

## 3. REQUERIMIENTOS DE INTERFAZ (UI)
- **Widget Obligatorio:** REQ_DUAL.
- **Entrada de Texto:** Área de texto con contador de palabras/caracteres en tiempo real.
- **Soporte de Evidencia:** El sistema debe permitir la subida de una imagen (JPG/PNG) para validar la caligrafía o esquemas previos, integrándose con el widget dual.

## 4. CRITERIOS DE EVALUACIÓN (LÓGICA IA DE CORRECCIÓN)
La IA de corrección debe aplicar una rúbrica de 0 a 100 basada en:
1. Adecuación: ¿Cumple con el registro y la tarea solicitada?
2. Coherencia y Cohesión: ¿El texto está organizado y usa conectores adecuados?
3. Corrección Gramatical: Precisión en estructuras y ortografía.
4. Rango Léxico: Variedad y precisión del vocabulario empleado.

## 5. PROTOCOLO DE GENERACIÓN IA (PHASE B)
Para generar una tarea de Writing, la IA recibe:
1. El tipo de tarea (Transactional/Discursive).
2. El contexto o input (ej: "Has recibido este email de un amigo...").
3. La métrica de extensión obligatoria.
4. El esquema JSON: {"question_text": "...", "model_answer": "..." (Texto de referencia para corrección)}.
