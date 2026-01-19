# ANEXO HITO 6: SISTEMA DE AUTOEVALUACIONES CON IA (UGR EMULATOR)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

---

## ESTADO DE LA HOJA DE RUTA TÉCNICA (Ref. Plan Maestro)
*Esta sección es el testigo de progreso que debe actualizarse cada sesión.*

1. [X] **Refactor de Orchestrator.** (Completado: Persistencia de arquetipo en `prompt_data`, gestión de strikes de cuota y sincronización de etiquetas UGR).
2. [X] **Estrategia CEFR_LANGUAGES.** (Completado: Prompt multimodal con tags, Frontend corregido con TTS nativo por idioma y grabadora automática).
3. [X] **Estrategia LOGIC_AND_TECH.** (Completado: Implementación de formato UGR Mixto -Teoría y Práctica-, integración en orquestador y generadores centrales).
4. [ ] **Estrategia SOCIO_LEGAL.** (Pendiente: Implementar lógica de casos prácticos y normativa jurídica).
5. [ ] **Estrategia HEALTH_SCIENCES.** (Pendiente).
6. [ ] **Estrategia HUMANITIES_ARTS.** (Pendiente).

---

## LOG DE AVANCES DE ESTA SESIÓN
*   **Implementación LOGIC_AND_TECH:** Se ha creado la estrategia `sciences_strategy.py` siguiendo el modelo "UGR Mixto", diferenciando entre asignaturas de Ingeniería (Código + Teoría Aplicada) y Ciencias Puras (Definiciones Formales + Problemas).
*   **Integración del Orquestador:** Se ha actualizado `orchestrator/tasks.py` para inyectar el nombre de la asignatura (`subject_name`) en la llamada a la estrategia, permitiendo la discriminación de contexto.
*   **Refactor de Prompt Generators:** Se ha eliminado la lógica hardcodeada en `core/services/prompt_generators.py`, delegando correctamente en la nueva función importada.
*   **Corrección de Rutas:** Se han aplicado parches utilizando rutas absolutas para garantizar la integridad del sistema de archivos.

---

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
**Objetivo Primario:** Implementación del Arquetipo 3: `SOCIO_LEGAL`.

1.  **Estrategia Jurídica:** Crear/Actualizar `humanities_strategy.py` (o módulo segregado si se decide separar) para soportar el "Tribunal Legal".
2.  **Estructura de Examen:**
    *   Test de Conceptos (Terminología jurídica).
    *   Caso Práctico (Hechos probados -> Fundamentos de Derecho -> Fallo).
    *   Ensayo/Dictamen.
3.  **Validación:** Asegurar que el prompt exija referencias a normativa vigente (Constitución, Código Civil, etc.) cuando aplique.
