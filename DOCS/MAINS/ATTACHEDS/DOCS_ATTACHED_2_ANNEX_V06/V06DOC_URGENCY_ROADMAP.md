# V06DOC_URGENCY_ROADMAP - PLAN DE ESTABILIZACIÓN DE EMERGENCIA (V1.0)

Este documento define las acciones críticas para resolver la incoherencia estructural detectada en la auditoría del Hito 6 (Fase II).

## 1. DIAGNÓSTICO CRÍTICO
Se han identificado 4 bloqueos fatales que impedirán la ejecución del motor `assessment_v2`:

1.  **Rotura de Contrato de Firma (`TypeError`):** `BaseExamStrategy` y sus clases hijas tienen definiciones divergentes de `get_user_prompt`. El orquestador fallará al intentar pasar argumentos.
2.  **Violación de "Skeleton-First" (Alucinación Estructural):** Las estrategias (salvo Languages) siguen usando prompts generativos ("GENERA 3 ÍTEMS") en lugar de prompts de rellenado ("RELLENA ESTE ESQUELETO"). Esto provoca que la IA ignore la configuración técnica de Python.
3.  **Fallo en Soporte de Archivos (Motores Discursivos):** Los motores `DRA-HOLO` y `BMT-SHIFT` (Humanidades, Social, Lenguas) fallan si reciben un diccionario con `file_url` en lugar de una cadena de texto, rompiendo la evaluación de tareas con adjuntos.
4.  **Configuración Obsoleta de Audio (SDK v1):** El parámetro `response_mime_type` para audio es incorrecto en la versión actual del SDK unificado de Google.

## 2. PROTOCOLO DE REPARACIÓN (SECUENCIAL)

### ACCIÓN 1: ESTANDARIZACIÓN DE LA CLASE BASE (BaseExamStrategy)
*   **Objetivo:** Unificar la firma del método `get_user_prompt` para soportar la inyección del esqueleto JSON.
*   **Cambio:** 
    ```python
    def get_user_prompt(self, context_text, topic, subdivision_id, generated_item_titles=None, skeleton_json=None):
    ```

### ACCIÓN 2: IMPLEMENTACIÓN DE "PROMPT BINDING" (Todas las Estrategias)
*   **Objetivo:** Modificar `humanities.py`, `social.py`, `tech.py`, `science.py` y `health.py`.
*   **Cambio:** Reescribir `get_user_prompt` para que:
    1.  Acepte `skeleton_json`.
    2.  Instruya a la IA explícitamente a **rellenar** la estructura proporcionada y **no generar** ítems nuevos.
    3.  Devuelva el JSON con los IDs intactos.

### ACCIÓN 3: SOPORTE DE ADJUNTOS EN MOTORES (Logic Refactor)
*   **Objetivo:** Evitar `Crash` cuando el alumno sube un archivo.
*   **Cambio:** En `grade_item` (para `DRA-HOLO` y similares), añadir detección de `file_url`:
    ```python
    if isinstance(student_input, dict) and 'file_url' in student_input:
        return Decimal('0.0'), {"status": "PENDING_AI_ANALYSIS", "file_received": True}
    ```

### ACCIÓN 4: CORRECCIÓN DE AUDIO (Gemini Service)
*   **Objetivo:** Generar audio nativo correctamente.
*   **Cambio:** Actualizar `generate_audio_content` para usar `response_modalities=["AUDIO"]` en `GenerateContentConfig`.

## 3. CRITERIOS DE VALIDACIÓN (DOD - Definition of Done)
1.  **Firma Unificada:** El orquestador puede instanciar cualquier estrategia y llamar a `get_user_prompt` con los mismos 5 argumentos sin error.
2.  **Persistencia de IDs:** La IA devuelve un JSON donde los `item_id` coinciden exactamente con los generados por Python en el paso `get_exam_skeleton`.
3.  **Gestión de Archivos:** El sistema acepta una entrega con archivo adjunto y la marca como `PENDING_AI_ANALYSIS` en lugar de lanzar una excepción.
