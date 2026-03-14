# ANEXO: HITO 06 - BLINDAJE Y REFACTORIZACIÓN DEL ARQUETIPO DE LENGUAS
# ESTADO: EN PROGRESO (HOJA DE RUTA DEFINITIVA)

## RESUMEN DE INCIDENCIAS DE LA SESIÓN ANTERIOR
1.  **Fallo de Rendimiento (Latencia Crítica):** Se ha confirmado una demora inaceptable entre la solicitud de una evaluación y la carga de la vista de configuración. La causa raíz es la llamada de clasificación a la IA (`AcademicDeductor`), que se ejecuta en un "punto ciego" antes de que se inicie el log de la tarea Celery, impidiendo su monitorización.
2.  **Fallo de Calidad (Contaminación Lingüística):** Se ha validado un error catastrófico en la generación del examen de chino, donde el modelo de IA ha mezclado caracteres del silabario japonés (Katakana) con los caracteres chinos (Hanzi) solicitados. La causa es un prompt de sistema insuficientemente restrictivo en la estrategia de generación de idiomas.

## HOJA DE RUTA PARA LA PRÓXIMA SESIÓN
1.  **Instrumentación de Logs (Resolución F1-Latencia):**
    *   **Acción:** Solicitar el archivo `orchestrator/tasks.py` para modificarlo mediante `PMA`.
    *   **Lógica a Implementar:** Justo antes de la línea `metadata = AcademicDeductor.get_context_metadata(...)` en la tarea `generate_exam_task`, añadir un evento de log: `exam.event_log.append({"ts": timezone.now().isoformat(), "msg": "Iniciando clasificación de asignatura (IA)..."})`. Justo después, añadir otro evento que registre la finalización y el resultado: `exam.event_log.append({"ts": timezone.now().isoformat(), "msg": f"Clasificación completada. Archetype: {metadata['archetype_id']}"})`.

2.  **Blindaje del Prompt de la Estrategia (Resolución F2-Contaminación):**
    *   **Acción:** Solicitar el archivo `assessment_v2/services/engine/strategies/humanities.py` para modificarlo mediante `PMA`.
    *   **Lógica a Implementar:** Localizar el método `get_system_prompt` dentro de la clase `HumanitiesStrategy`. Se reforzará el prompt con instrucciones dictatoriales y restricciones negativas explícitas para el `target_language_code` 'zh' (Chino). El nuevo prompt debe incluir una directriz como: "Eres un experto en la generación de pruebas de nivel para el idioma chino (Mandarín). **PROHIBIDO** terminantemente usar caracteres de los silabarios japoneses (Hiragana, Katakana) o coreanos (Hangul). Céntrate exclusivamente en los caracteres chinos Hanzi simplificados. Los errores de este tipo son inaceptables."

3.  **Re-validación de Campo:**
    *   Una vez aplicados los parches, el usuario (Miguel Ángel) junto a la colaboradora especialista, ejecutarán un nuevo test de generación de examen de Chino (LVL_B, ITIN_MIN) directamente desde la plataforma.
    *   Se deberá verificar la ausencia total de caracteres no chinos y que la latencia inicial ahora queda reflejada de forma clara en el log del examen.
