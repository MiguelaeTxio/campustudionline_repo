# ANEXO HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA (UGR EMULATOR)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

---

## ESTADO DE LA HOJA DE RUTA TÉCNICA (Ref. Plan Maestro)
*Esta sección es el testigo de progreso que debe actualizarse cada sesión.*

1. [X] **Refactor de Orchestrator.** (Completado: Persistencia de arquetipo en `prompt_data`, gestión de strikes de cuota y sincronización de etiquetas UGR).
2. [X] **Estrategia CEFR_LANGUAGES.** (Completado: Prompt multimodal con tags, Frontend corregido con TTS nativo por idioma y grabadora automática).
3. [X] **Estrategia LOGIC_AND_TECH.** (Completado: Implementación de formato UGR Mixto).
4. [X] **Estrategia SOCIO_LEGAL.** (Completado: Implementación de estrategia segregada `legal_strategy.py` con estructura UGR: Test + Teoría + Práctica con fundamentación).
5. [ ] **Estrategia HEALTH_SCIENCES.** (Pendiente).
6. [ ] **Estrategia HUMANITIES_ARTS.** (Pendiente).

---

## LOG DE AVANCES DE ESTA SESIÓN
*   **Implementación SOCIO_LEGAL:** Se ha creado `core/services/assessment_strategies/legal_strategy.py` replicando fielmente el modelo de examen de la Facultad de Derecho UGR.
*   **Segregación de Prompts:** Se ha refactorizado `core/services/prompt_generators.py` para desacoplar la lógica de Humanidades y delegar en la nueva estrategia legal.
*   **Estabilidad del Sistema:** Se ha corregido un error crítico de sintaxis introducido durante el parcheo de los generadores.

---

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
**Objetivo Primario:** Implementación del Arquetipo 4: `HEALTH_SCIENCES`.

1.  **INVESTIGACIÓN OBLIGATORIA (REALIDAD UGR):** Antes de iniciar la implementación técnica, se debe realizar una investigación exhaustiva en internet sobre los formatos de examen actuales de la UGR para grados de Ciencias de la Salud (Enfermería, Medicina, Psicología). El emulador debe reflejar la realidad de la certificación vigente.
2.  **Estrategia Salud:** Crear `health_strategy.py` incorporando los hallazgos (probablemente casos clínicos, protocolos de actuación y triaje).
3.  **Validación:** Asegurar que los prompts generen escenarios clínicos realistas.
