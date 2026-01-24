# PLAN MAESTRO DE EVALUACIONES: LEY ESTRUCTURAL E INMUTABLE (UGR EMULATOR)

## 1. MÁXIMAS DE DESARROLLO (VINCULANTES)
1.  **AUDITORÍA GIT & PAIR:** Antes de modificar el sistema de rotación de ApiKeys o el orquestador, es OBLIGATORIO ejecutar un PAIR comparando con el motor de generación de contenidos mediante auditoría de historial Git. La gestión de claves debe ser idéntica.
2.  **INVESTIGACIÓN ACADÉMICA:** Todo cambio en prompts o estructuras de examen requiere un PVD previo en internet para contrastar la normativa vigente de certificación de la UGR (CertAcles, CLM, Guías Docentes).
3.  **SEGREGACIÓN DE ESQUELETOS:** Queda TERMINANTEMENTE PROHIBIDO ensuciar `tasks.py` con lógica de creación de preguntas. Cada arquetipo debe definir su esqueleto (Python) en su respectivo archivo de estrategia.
4.  **FLUJO ATÓMICO:** El proceso de generación se divide en dos fases:
    -   Fase A: Creación del Esqueleto vacío (Lógica Python en Estrategia).
    -   Fase B: Relleno de Contenido (Llamadas a API).

## 2. ARQUITECTURA DE ARQUETIPOS
1.  **LOGIC_AND_TECH:** (Ingeniería/Ciencias). Foco en LaTeX y bloques de código.
2.  **CEFR_LANGUAGES:** (Idiomas). Foco en las 4 destrezas y TTS nativo.
3.  **SOCIO_LEGAL:** (Derecho/Sociales). Foco en fundamentación jurídica y casos.
4.  **HEALTH_SCIENCES:** (Salud). Foco en razonamiento clínico (ECOE).
5.  **HUMANITIES_ARTS:** (Artes/Letras). Foco en ensayo académico y dialéctica.

## 3. ESTÁNDARES TÉCNICOS
-   **TTS:** Acento nativo dinámico por asignatura.
-   **Frontend:** Soporte universal para Markdown, LaTeX (MathJax) y Audio v3.
-   **Persistencia:** Clasificación inamovible en `prompt_data` tras primera ejecución.


## 4. ESPECIFICACIÓN TÉCNICA DE ARQUETIPOS
La definición detallada de esqueletos, niveles y widgets se rige por:
- `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md`