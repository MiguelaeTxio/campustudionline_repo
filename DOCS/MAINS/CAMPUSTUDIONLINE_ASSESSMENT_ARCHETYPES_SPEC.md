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
