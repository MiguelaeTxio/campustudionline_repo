# Hito 6: Sistema de Autoevaluaciones con IA (RECONSTRUCCIÓN NUCLEAR - EN PROGRESO)

**Estado:** 🚧 EN DESARROLLO (Arquitectura Pedagógica Validada)
**Modelo Vinculante:** `gemini-2.5-flash-lite`

## DIRECTRIZ SUPREMA PARA LA PRÓXIMA SESIÓN
El modelo entrante **DEBE** comenzar realizando una investigación profunda (PVD) sobre los siguientes estándares para igualar el contexto del modelo saliente. No debe generar código hasta haber verbalizado la comprensión de:
1.  **CertACLES (UGR):** Modelo de 4 destrezas para Idiomas (Reading, Listening, Writing, Speaking).
2.  **EUR-ACE® (Ingeniería):** Estándar de calidad para STEM centrado en resolución de problemas complejos y juicio técnico.
3.  **MECES Nivel 2 / Taxonomía SOLO (Humanidades):** Foco en aprendizaje relacional y crítico (Comentario de Fuentes).

## HOJA DE RUTA TÉCNICA (ORDEN ESTRICTO)
1.  **Orchestrator Fix (Blindaje DB):** En `tasks.py`, dentro de `generate_assessment_from_content_task`, sanear el diccionario `q_data` antes de llamar a `Question.objects.create()`. Forzar `q_data['question_type'] = 'open_ended'` para evitar el Error 1406 (Data too long) de MySQL.
2.  **Refactor de Prompts (Super-Arquetipos):** Implementar en `prompt_generators.py` los 3 Super-Arquetipos con lógica de sub-disciplina (Arte, Historia, Derecho, Ingeniería, etc.) asegurando una densidad de 12-15 ítems por examen.
3.  **Validación de Flujo Server-Side:** Verificar que la vista `take_assessment` en `views.py` procesa correctamente los nuevos fragmentos (transcripts y tags de grabación) usando la lógica server-side ya implementada.
4.  **Prueba de Carga:** Generar una evaluación completa para una asignatura de Ingeniería y otra de Idiomas para validar la estabilidad del parser `dirtyjson`.

