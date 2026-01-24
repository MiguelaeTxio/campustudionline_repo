# ANEXO HITO 6: SISTEMA DE EVALUACIONES (ESTABILIZACIÓN ARQUITECTÓNICA)

DIRECTRIZ OBLIGATORIA: Al iniciar sesión con este hito, es **MANDATORIO** cargar los archivos:
1. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md` (Lógica de Motor)
2. `DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_ARCHETYPES_SPEC.md` (Esqueleto y Granularidad)

## ESTADO DE LA HOJA DE RUTA
1. [X] **Restauración de Sistema.** (Sintaxis corregida y servidor WSGI operativo).
2. [X] **Implementación de Atomic Flow (Fase A).** (Esqueletos deterministas delegados a estrategias).
3. [X] **Sincronización PAIR de Rotación.** (Blindaje ante errores 429 y rotación proactiva).
4. [X] **Purga de Código Muerto.** (Eliminada lógica obsoleta de clasificación por keywords).
5. [X] **Sincronización de la Triada de la Verdad.** (Creación del Santo Grial de Arquetipos v2.0).
6. [X] **Reparación de Regresiones de UI.** (Corrección de límites y estados en utils.py).

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN
1. **Implementación de INPUT_DUALITY:** Refactorizar `take_assessment_*.html` para que toda pregunta `open_ended` muestre simultáneamente `textarea` y `input[type=file]`.
2. **Inyección de STIMULUS_STICKY:** Implementar mediante JS y CSS el botón flotante persistente para consulta de `Reading` y `Listening` mediante modal.
3. **Refactorización de Fase B (Audio):** Ajustar el motor de tareas para forzar la generación de audios en formato **MP3**.
4. **Validación de Esqueleto Minor:** Ejecutar prueba real de Chino B1 para verificar la inyección de la tarea de caligrafía (Foto prioritaria).

## LOG DE CAMBIOS (NRA)
- Consolidado el Santo Grial de Arquetipos (v2.0) con granularidad por curso y nivel.
- Corregida la segregación de `SOCIO_LEGAL` eliminando lógica residual en Humanidades.
- Restaurado el motor de estados de UI en `assessment/utils.py`.
