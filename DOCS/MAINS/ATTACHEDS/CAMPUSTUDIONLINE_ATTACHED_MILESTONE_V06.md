# Hito 6: Sistema de Autoevaluaciones con IA (EMULADOR UGR - RECONSTRUCCIÓN V4)

**Estado:** 🚧 EN DESARROLLO (Clasificación Semántica y Blindaje LaTeX Implementados)
**Modelo Vinculante:** `gemini-2.5-flash-lite`

## RESUMEN DE LA SESIÓN ACTUAL
- **Infraestructura:** Estabilización de las `Always-on Tasks` (`Primary` y `Heavy`) eliminando bloqueos de identidad (`--hostname`) y simplificando el arranque con carga nativa de `.env`.
- **Lógica de Clasificación:** Implementado el **PASO 0** en `orchestrator/tasks.py`. Ahora el sistema consulta a la IA la naturaleza de la asignatura (Ciencias, Idiomas o Humanidades) antes de generar el examen.
- **Blindaje de Datos:** Implementado el **Escudo LaTeX** en `core/services/gemini_service.py` (función `clean_json_response`). Este filtro duplica barras invertidas en secuencias no estándar, evitando fallos de decodificación JSON en fórmulas matemáticas.
- **Sintaxis:** Corregidos errores de cadenas multilínea en `prompt_generators.py` que bloqueaban el arranque del servidor.

## HOJA DE RUTA PARA LA SIGUIENTE SESIÓN (LEY SUPREMA)

### PASO 1: VERIFICACIÓN DE ARQUETIPOS (TEST UNITARIOS)
1.  **Validar Ingeniería:** Confirmar que la evaluación de "Derivadas e Integrales V2" (ID #203 o sucesiva) ha finalizado correctamente gracias al Escudo LaTeX.
2.  **Validar Idiomas:** Ejecutar test unitario para "Inglés Académico C1" y verificar la estructura de 4 secciones (Reading/Listening/Writing/Speaking).
3.  **Validar Humanidades:** Ejecutar test unitario para "Historia del Arte" y verificar la estructura mixta de Test y Ensayo.

### PASO 2: AUDITORÍA DE RENDIMIENTO
1.  Verificar que el tiempo de respuesta del "Paso 0" (Clasificación) no penaliza excesivamente la experiencia de usuario.
2.  Confirmar que las fórmulas LaTeX se renderizan correctamente en el frontend tras el blindaje.

### PASO 3: LIMPIEZA DE TEST
1.  Una vez validados los 3 arquetipos, purgar las asignaturas y contenidos de prueba del sistema para mantener la higiene de la BBDD.
