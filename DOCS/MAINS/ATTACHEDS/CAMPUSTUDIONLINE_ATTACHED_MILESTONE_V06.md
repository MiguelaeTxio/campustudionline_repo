# ANEXO: HITO 06 - BLINDAJE Y REFACTORIZACIÓN DEL ARQUETIPO DE LENGUAS
# ESTADO: EN PROGRESO (HOJA DE RUTA DEFINITIVA)

## HOJA DE RUTA PARA LA PRÓXIMA SESIÓN (ACTUALIZADA)
1. **Auditoría de Código (Arquetipo ARCH_LANG):** Revisar las estrategias correspondientes a los 6 sub-arquetipos de lenguas (SUB-LIN-INSTR, SUB-LIN-MINOR, SUB-LIN-PHILO, SUB-LIN-NORM, SUB-LIN-TRA-TECH, SUB-LIN-TRA-LIT). Verificar su correcta integración con los nuevos esquemas Pydantic (`gemini_schemas.py`), la eliminación completa de los marcadores de texto en las plantillas y su compatibilidad con `gemini-3.1-flash` mediante Structured Outputs.
2. **Testing Exhaustivo de Lenguas:** Ejecutar pruebas de generación completas para cada uno de los 6 sub-arquetipos. Validar que la API retorna los JSON estructurados de forma estricta y que el orquestador los mapea en base de datos y renderiza en el frontend sin errores de truncamiento o sintaxis.
3. **Transición a Nuevo Arquetipo:** Una vez estabilizado y validado funcionalmente el arquetipo de Lenguas (`ARCH_LANG`), dar comienzo a la auditoría y refactorización del siguiente bloque en prioridad (ej. Ciencias de la Salud o Ciencias Sociales y Jurídicas).

**DIRECTRIZ DE FUENTE DE LA VERDAD:** El motor de IA opera ahora bajo "Structured Outputs". La plataforma Python define el modelo de datos (Pydantic) y la IA genera su respuesta constreñida a esa estructura. Queda prohibida la técnica de inyección mediante marcadores de texto.
