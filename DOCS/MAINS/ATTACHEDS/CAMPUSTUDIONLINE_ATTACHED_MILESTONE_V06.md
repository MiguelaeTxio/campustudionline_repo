# Hito 6: Sistema de Autoevaluaciones con IA (EMULADOR UGR - RECONSTRUCCIÓN V4)

**Estado:** 🚧 EN DESARROLLO (Arquitectura de Pipeline Implementada)
**Modelo Vinculante:** `gemini-3-flash-preview`

## RESUMEN DE LA SESIÓN ACTUAL
- **Modelos:** Campos `selection_range`, `reading_stimulus` y `listening_transcript` plenamente operativos.
- **Lógica de Filtrado:** Implementada en `utils.py` la extracción por TOC Markdown y filtrado por selección de usuario.
- **Frontend:** Creada vista `configure_assessment` y template de selección de capítulos.
- **Interfaz de Realización:** Sidebar actualizada para mostrar el estímulo generado con blindaje MathJax.
- **Incidencia Crítica:** La sesión termina con un `ImportError` en `tasks.py` debido a una persistencia fallida en `core/services/prompt_generators.py`. El sistema está actualmente inoperativo (WSGI bloqueado).

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 0: REPARACIÓN DE EMERGENCIA (DESBLOQUEO WSGI)
1. **Restauración de `prompt_generators.py`:** Es MANDATORIO inyectar las funciones `generate_stimulus_creation_prompt` y `generate_ugr_questions_prompt` que no se persistieron correctamente. Sin esto, el servidor no arrancará.

### PASO 1: VALIDACIÓN DEL PIPELINE
1. **Test de Generación:** Realizar una solicitud de evaluación seleccionando temas específicos.
2. **Auditoría de Persistencia:** Verificar que el `reading_stimulus` se guarda en la BBDD tras el Paso 1 del orquestador.

### PASO 2: REFINAMIENTO DE RENDIMIENTO
1. **Optimización de Carga:** Analizar por qué el texto del reading tarda en aparecer en la sidebar tras la generación.
2. **Hardening de Tareas:** Asegurar que el cambio de claves API (rotación) en el Paso 1 y Paso 2 sea atómico.
