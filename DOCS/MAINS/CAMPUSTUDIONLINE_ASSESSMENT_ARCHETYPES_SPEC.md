# ESPECIFICACIÓN TÉCNICA DE AUTOEVALUACIONES (ESTÁNDAR UNIFICADO UGR)

## 1. CAPA NUCLEAR: GESTIÓN DE RANGO Y CONTEXTO ACADÉMICO
Esta capa es MANDATORIA y común para TODOS los arquetipos. El orquestador debe garantizar:
- **Inyección de Syllabus:** Todo examen debe basarse en el `course_content_outline` y `learning_objectives` del `Subject`.
- **Filtro de Rango (Anti-Ceguera):** Es OBLIGATORIO que el contenido entregado a la IA esté filtrado por el `selection_range` del usuario. Se prohíbe entregar el `full_content` si existe una selección parcial.
- **Trazabilidad Pedagógica:** El prompt debe incluir qué objetivos de aprendizaje se están evaluando específicamente en ese rango.

## 2. CAPA ESTRUCTURAL: BLOQUES Y GRAFÍAS
Funcionalidades transversales según tipo de materia:
- **Script Family:** 
    - `LOGOGRAPHIC` (Chino/Japonés): Fuerza `QT_PROD` para caligrafía.
    - `RTL` (Árabe): Fuerza alineación derecha.
- **Inmersión Lingüística:** 
    - `MINOR`: Instrucciones en Castellano / Contenido en Idioma Objetivo.
    - `MAIOR`: Inmersión Total (100% Idioma Objetivo).

## 3. DEFINICIÓN DE ARQUETIPOS (ESPECIFICACIONES SECTORIALES)

### I. CEFR_LANGUAGES (Idiomas)
- **Foco:** Gramática, Vocabulario y Sintaxis Aplicada.
- **Estructura:** Itinerarios Grado (UGR) vs Acreditación (CLM).

### II. LOGIC_AND_TECH / HEALTH / LEGAL / HUMANITIES
- **Foco:** Aplicación del conocimiento según el syllabus inyectado en el Paso 1.
- **Estructura:** Desarrollo, Test y Casos Prácticos definidos en el Master Plan.

## 4. ESPECIFICACIÓN DE INTERFAZ (UI LABELS CONTRACT)
Para garantizar la correcta renderización en el Frontend, cada estrategia debe retornar un diccionario `ui_labels` estrictamente tipado según su familia.

### A. FAMILIA LINGÜÍSTICA (CEFR_LANGUAGES)
Usa claves técnicas para mapear bloques de competencia.
\`\`\`json
{
    "LBL_READING": "Target / Lectura",
    "LBL_LISTENING": "Target / Escucha",
    "LBL_WRITING": "Target / Escritura",
    "LBL_SPEAKING": "Target / Grabación",
    "submit_button": "Entregar Evaluación",
    "write_placeholder": "Escribe aquí..."
}
\`\`\`

### B. FAMILIA ACADÉMICA (RESTO DE ARQUETIPOS)
Usa claves semánticas descriptivas para cabeceras de sección.

#### HUMANITIES & ARTS
\`\`\`json
{
    "reading_header": "FUENTE / TEXTO DE ANÁLISIS",
    "audio_header": "RECURSO AUDIOVISUAL",
    "recording_label": "RESPUESTA ORAL",
    "upload_label": "Subir Manuscrito/Imagen",
    "upload_help": "Clic o arrastrar archivo",
    "write_answer_placeholder": "Desarrolla tu análisis académico aquí...",
    "submit_button": "Entregar Evaluación"
}
\`\`\`

#### LOGIC_AND_TECH
\`\`\`json
{
    "reading_header": "MATERIAL DE REFERENCIA",
    "audio_header": "RECURSO DE APOYO",
    "recording_label": "EXPLICACIÓN VERBAL",
    "upload_label": "Subir Resolución (Foto/PDF)",
    "upload_help": "Adjuntar cálculos manuscritos",
    "write_answer_placeholder": "Desarrolla tu respuesta técnica aquí...",
    "submit_button": "Entregar Evaluación"
}
\`\`\`

#### SOCIO_LEGAL
\`\`\`json
{
    "reading_header": "EXPEDIENTE / CASO DE ESTUDIO",
    "audio_header": "TESTIMONIO / GRABACIÓN",
    "recording_label": "DICTAMEN ORAL",
    "upload_label": "Subir Escrito Jurídico",
    "upload_help": "Adjuntar documento",
    "write_answer_placeholder": "Fundamentación jurídica...",
    "submit_button": "Entregar Dictamen"
}
\`\`\`

#### HEALTH_SCIENCES
\`\`\`json
{
    "reading_header": "HISTORIA CLÍNICA / CASO",
    "audio_header": "AUSCULTACIÓN / ENTREVISTA",
    "recording_label": "JUICIO CLÍNICO ORAL",
    "upload_label": "Subir Informe/Pauta",
    "upload_help": "Adjuntar notas clínicas",
    "write_answer_placeholder": "Juicio diagnóstico y plan...",
    "submit_button": "Finalizar ECOE"
}
\`\`\`
