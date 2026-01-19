# ANEXO HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA (UGR EMULATOR)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

---

## ESTADO DE LA HOJA DE RUTA TÉCNICA (Ref. Plan Maestro)
*Esta sección es el testigo de progreso que debe actualizarse cada sesión.*

1. [X] **Refactor de Orchestrator.** (Completado: Persistencia de arquetipo en `prompt_data`, gestión de strikes de cuota y sincronización de etiquetas UGR).
2. [X] **Estrategia CEFR_LANGUAGES.** (Completado: Prompt multimodal con tags, Frontend corregido con TTS nativo por idioma y grabadora automática).
3. [ ] **Estrategia LOGIC_AND_TECH.** (Pendiente: Implementar lógica de problemas complejos, LaTeX y bloques de código).
4. [ ] **Estrategia SOCIO_LEGAL.** (Pendiente).
5. [ ] **Estrategia HEALTH_SCIENCES.** (Pendiente).
6. [ ] **Estrategia HUMANITIES_ARTS.** (Pendiente).

---

## LOG DE AVANCES DE ESTA SESIÓN
*   **Reparación Crítica:** Resolución de `ImportError` en `tasks.py` mediante la creación/unificación de funciones de estrategia segregadas.
*   **Persistencia del Arquetipo:** Se ha blindado el motor para que el "Rector" (IA) solo clasifique una vez; el resultado se guarda en DB, evitando cambios de formato en reintentos.
*   **UX Idiomas:** Se ha eliminado el ruido en el audio (Speaker A/B) y se ha configurado el `SpeechSynthesis` del navegador para usar acentos nativos (fr-FR, en-US) según la asignatura.
*   **Taxonomía UGR:** El clasificador ha sido re-entrenado para reconocer las 5 áreas de conocimiento de la Universidad de Granada, ignorando la rama genérica y analizando el contenido semántico de cada asignatura.

---

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
**Objetivo Primario:** Implementación del Arquetipo 1: `LOGIC_AND_TECH`.

1.  **Estrategia Técnica:** Actualizar `sciences_strategy.py` para que la IA genere problemas de ingeniería que requieran:
    *   Resolución mediante fórmulas en formato **LaTeX**.
    *   Desarrollo de algoritmos en bloques de **Pseudocódigo** o código real.
2.  **Validación de Salida:** Asegurar que el prompt prohíba preguntas teóricas de "desarrollo de texto" en este arquetipo, forzando el enfoque práctico/técnico.
3.  **Refactor de Prompt:** Adaptar la lógica para asignaturas detectadas como Criptografía, Algorítmica y Programación.
