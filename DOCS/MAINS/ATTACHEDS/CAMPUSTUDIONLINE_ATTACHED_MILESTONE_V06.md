# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md

# ANEXO HITO 6: SISTEMA DE EVALUACIONES (RE-ARQUITECTURA NUCLEAR UGR)

## DIRECTRIZ DE CARGA OBLIGATORIA (MANDATORIO)
Al iniciar sesión con este hito, es **IMPERATIVO** cargar los siguientes documentos que constituyen la Ley Técnica del sistema:
1. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_SYSTEM_MASTER_PLAN.md` (Santo Grial).
2. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_INTERACTION_MATRIX.md` (Matriz S-Q-R).

## ESTADO DE LA HOJA DE RUTA
1. [X] **Consolidación del Santo Grial.** Definición de la Matriz de Interacción Universal (Source-Interaction-Response).
2. [X] **Migración de Modelos.** Implementación de campos `source_type`, `interaction_type` y `response_mode` en el modelo `Question` (Migración 0028).
3. [X] **Sincronización Administrativa.** Actualización de `admin.py` para visualizar y filtrar por la nueva matriz.
4. [X] **Refactorización de Estrategias.** Actualización de las 5 estrategias académicas para emitir esqueletos compatibles con el Emulador UGR.
5. [X] **Reparación del Orquestador.** Actualización de `orchestrator/tasks.py` para persistir la triada S-Q-R durante la generación.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)
1.  **Refactorización de la "Plantilla Tonta":**
    *   Modificar `take_assessment_languages.html` para eliminar los `{% if %}` basados en nombres de variables antiguos.
    *   Implementar un sistema de `render_mode` basado exclusivamente en los campos `source_type`, `interaction_type` y `response_mode`.
2.  **Implementación de Widgets Multimedia (Estándar Cassette):**
    *   Asegurar el renderizado de botones redondos de 45px en todos los estímulos de audio (`SRC_AUD`).
    *   Añadir botones físicos de **STOP** al reproductor y botones de **STOP/SAVE** a la grabadora.
3.  **Lógica de Escritura Dual (REQ_DUAL):**
    *   Garantizar que en preguntas de producción escrita siempre coexistan el `textarea` y la zona `upload-dashed`.
4.  **Implementación del Cloze Engine (Fase B):**
    *   Actualizar el parser en `tasks.py` para detectar patrones `[opcion1/opcion2]` en el texto generado por la IA y transformarlos en inputs o dropdowns según indique el `interaction_type`.

## LOG DE CAMBIOS (EDC)
- **Migración Nuclear:** Se eliminaron los campos `widget_type` y `question_type` en favor de la matriz de interacción UGR.
- **Idiomas (Acreditación):** Implementado el esqueleto de 9 preguntas que cubre Reading, Use of English, Listening, Writing y Speaking.
- **Backend Sync:** Sincronizados `tasks.py` y todas las estrategias para evitar errores de integridad tras el cambio de modelo.
