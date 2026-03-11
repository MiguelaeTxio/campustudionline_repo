<!-- /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md -->
# ANEXO: HITO 06 - BLINDAJE Y REFACTORIZACIÓN DEL ARQUETIPO DE LENGUAS
# ESTADO: EN PROGRESO (HOJA DE RUTA DEFINITIVA)

## HOJA DE RUTA PARA LA PRÓXIMA SESIÓN (ACTUALIZADA)
1. **Propagación de Directriz Vinculante (PMA Estricto):** Modificación de todos los archivos `TOTAL_COMMANDER_*.md` para actualizar la directriz del modelo de IA a `gemini-3.1-flash` e insertar la validación de sintaxis JS mediante `esprima`.
2. **Actualización de Documentación Satélite (Hito 6):** Reflejar en la documentación técnica del Hito 6 el cambio de metodología: transición de "relleno de marcadores" a "JSON estructurado nativo" (Structured Outputs).
3. **Refactorización de Código Fuente:** Aplicar las modificaciones correspondientes en `gemini_service.py` y el resto de servicios de IA para implementar los esquemas nativos y simplificar la lógica de validación, tras haber completado las actualizaciones documentales.

**DIRECTRIZ DE FUENTE DE LA VERDAD:** Los cambios son atómicos y deben seguir el `PMA` estricto (Backup, Propuesta, Auditoría de Diff, Autorización, `mv`). No se debe aplicar ningún cambio sin la validación previa de sintaxis y la auditoría de diff individualizada.