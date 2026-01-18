# Hito 6: Sistema de Autoevaluaciones con IA (Fase Multimodal)

**Estado:** 🛑 BLOQUEADO (Error de Sintaxis en Backend)
**Modelo:** `gemini-2.5-flash-lite`

## RESUMEN DE LA SESIÓN
- **Infraestructura Multimodal:** Se ha actualizado `gemini_service.py` para soportar entrada/salida de audio nativo.
- **Base de Datos:** Aplicada migración `0023` añadiendo el campo `generated_audio` al modelo `Assessment`.
- **Lógica UGR:** Se ha diseñado la inyección de títulos académicos oficiales y la activación de widgets (Play/Micro) mediante etiquetas separadas.
- **Incidencia:** Una operación de reemplazo global corrompió `orchestrator/tasks.py`, insertando saltos de línea físicos dentro de literales de cadena, lo que impide el arranque del servidor WSGI.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: RECUPERACIÓN DEL SERVIDOR (PRIORIDAD ALTA)
1. **Restaurar `tasks.py`:** Ejecutar `cp orchestrator/tasks.py.bak orchestrator/tasks.py` para devolver el servidor a un estado funcional.
2. **Verificación:** Reiniciar WSGI y confirmar carga del sitio.

### PASO 2: RE-APLICACIÓN DE MEJORAS HITO 6
Aplicar de forma quirúrgica (PMA) sobre el archivo restaurado las siguientes funciones ya validadas:
1. **Generación de Audio Nativo:** Integrar `generate_audio_content` en el flujo de creación para persistir el Listening real en `.mp3`.
2. **Terminología UGR:** Aplicar el mapa de títulos académicos dinámicos según el idioma detectado por la IA.
3. **Hardening de Widgets:** Asegurar dobles saltos de línea `\n\n` antes de `[---AUDIO-REQUIRED---]` y `[---RECORDING-REQUIRED---]`.
4. **Corrección Multimodal:** Activar `generate_multimodal_correction` para que la IA escuche las grabaciones del alumno en la sección de Speaking.
5. **Blindaje de Modelos:** Saneamiento de los campos del JSON de la IA para evitar errores por campos alucinados (como `follow_up_questions`).

### PASO 3: VALIDACIÓN FINAL
1. Generar evaluación de idiomas (ej. Italiano) y verificar:
   - Títulos académicos correctos.
   - Botón de Play funcional (con audio nativo).
   - Grabadora activa y evaluada por la IA tras la entrega.
