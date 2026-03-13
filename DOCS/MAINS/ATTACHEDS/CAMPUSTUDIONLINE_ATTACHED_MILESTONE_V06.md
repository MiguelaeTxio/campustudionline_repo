# ANEXO: HITO 06 - BLINDAJE Y REFACTORIZACIÓN DEL ARQUETIPO DE LENGUAS
# ESTADO: EN PROGRESO (HOJA DE RUTA DEFINITIVA)

## HOJA DE RUTA PARA LA PRÓXIMA SESIÓN
1. **Testing de Generación (Testing Funcional):** Ejecutar un script de prueba temporal en `/home/MiguelAeTxio/SWAP/test_lang_generation.py` que invoque `ExamFactory.get_strategy` para `ARCH_LANG` y solicite una generación atómica de una sección (ej: `SD_READ`).
2. **Validación de Estructura:** Verificar que la respuesta de Gemini sea un JSON estricto que cumpla con `ExamSectionSchema` (sin marcadores de posición, sin texto libre).
3. **Mapeo a BBDD:** Validar que `generate_exam_task` persiste correctamente los datos en `ExamSection` y `ExamItem` utilizando los `item_id` inyectados en el esqueleto.
4. **Verificación de UniversIA:** Si el testing de evaluación es exitoso, auditar las llamadas de UniversIA para asegurar que los nuevos esquemas de respuesta no interfieran con la lógica conversacional.

**DIRECTRIZ DE FUENTE DE LA VERDAD:** El motor de IA opera bajo "Structured Outputs". La plataforma Python define el modelo de datos (Pydantic) y la IA genera su respuesta constreñida a esa estructura. Queda prohibida la técnica de inyección mediante marcadores de texto.
