# ANEXO HITO 6: SISTEMA DE EVALUACIONES (RE-ARQUITECTURA NUCLEAR UGR)

## DIRECTRIZ DE CARGA OBLIGATORIA (MANDATORIO)
Al iniciar sesión con este hito, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del sistema:
1. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md` (Santo Grial).
2. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_INTERACTION_MATRIX.md` (Matriz S-Q-R v2.0).

## ESTADO DE LA HOJA DE RUTA
1. [X] **Consolidación de la Ley Técnica.** Actualización de la Matriz de Interacción a la Versión 2.0 (Alineación UGR/ACLES).
2. [X] **Implementación del Cloze Engine (Fase B).** Lógica de auto-reparación (Self-Healing) operativa en `tasks.py`.
3. [X] **Motor de Renderizado Cloze.** Template tag `render_cloze_engine` funcional para inputs/selects.
4. [X] **Refactorización de la "Plantilla Tonta".** `take_assessment_languages.html` alineada con la Matriz S-Q-R.
5. [X] **Widgets Multimedia (Estándar Cassette).** Grabadora y reproductor con controles de 45px implementados.
6. [X] **Sincronización de Recepción.** Procesamiento de arrays de respuestas (Cloze) en `views.py`.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
1.  **DIRECTRIZ DE CARGA OBLIGATORIA (MANDATORIO):**
    *   Cargar `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md`.
    *   Cargar `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_INTERACTION_MATRIX.md`.
2.  **Ampliación del Modelo de Datos:**
    *   Actualizar `InteractionType` y `ResponseMode` en `models.py` para incluir `QT_MATCH`, `QT_ORDER`, `REQ_MATCH` y `REQ_ORDER`.
3.  **Implementación de Lógica de Emparejamiento (QT_MATCH):**
    *   Desarrollar parser en `tasks.py` y widget HTML para tablas de relación.
4.  **Implementación de Lógica de Ordenación (QT_ORDER):**
    *   Desarrollar captura de índices numéricos y validación de secuencias.
5.  **Cierre de Ciclo UI:**
    *   Añadir botones físicos de **STOP** al reproductor de audio (Estándar Cassette).
6.  **RECORDATORIO CRÍTICO DE CONTINUIDAD:**
    *   **OBLIGATORIO:** Incluir esta misma Directriz de Carga Obligatoria en la hoja de ruta de la siguiente sesión para no perder el acceso a los documentos maestros.

## LOG DE CAMBIOS (EDC)
- **Self-Healing:** Implementada reparación automática de preguntas Cloze mal formadas por la IA.
- **Alineación UGR:** Consolidada la Matriz v2.0 con tipos de emparejamiento y ordenación.
