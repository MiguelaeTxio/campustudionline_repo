# ANEXO HITO 6: SISTEMA DE EVALUACIONES (ESTABILIZACIÓN ARQUITECTÓNICA)

**DIRECTRIZ OBLIGATORIA:** Al iniciar sesión con este hito, es **MANDATORIO** cargar el archivo:
`DOCS/MAINS/CAMPUSTUDIONLINE_ASSESSMENT_MASTER_PLAN.md`

## ESTADO DE LA HOJA DE RUTA (POST-RESTRUCTURACIÓN)
1. [X] **Restauración de Sistema.** (Reparado el crash de `tasks.py` y restaurado sistema de claves).
2. [ ] **Migración de Esqueletos (FASE 1).** Mover `create_assessment_skeleton` de `tasks.py` a las estrategias individuales.
3. [ ] **Auditoría Git de Rotación.** Sincronizar al 100% el sistema de ApiKeys con el de contenidos.
4. [ ] **Test de Estrategia LOGIC_AND_TECH.** Verificar renderizado de LaTeX.

## LOG DE CAMBIOS (SESIÓN ACTUAL)
-   **Fijación de Ley:** Eliminado el rastreo de progreso del Master Plan para convertirlo en documento de ley técnica.
-   **Blindaje de Cuotas:** Reforzada la detección de errores 429 en el orquestador para forzar rotación de claves.
-   **Limpieza de Tasks:** Preparado el orquestador para recibir los esqueletos desde las estrategias.
