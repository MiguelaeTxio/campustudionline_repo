# ANEXO: HITO 24 - SISTEMA DE RUEGOS Y PREGUNTAS (EN PROGRESO)

## Estado de la Situación
Tras una refactorización de evaluaciones que provocó una regresión crítica en la generación de contenido académico, se ha procedido a una restauración quirúrgica de la lógica funcional al 14/01/2026.

### Logros Técnicos de la Sesión:
1. **Restauración Motor V0:** Se recuperó el ensamblado de Markdown con bibliografía y el flujo de generación por chunks ultra-blindado.
2. **Corrección 503 (High Demand):** Se implementó un filtro en `tasks.py` para distinguir errores de cuota (429) de sobrecarga de Google (503). El sistema ahora espera 45s ante un 503 sin castigar la API Key.
3. **Parche de Conteo Dashboard:** Se corrigió la consulta en `orchestrator/admin_views.py` para incluir asignaturas con contenidos directos (M2M) además de las de `ContentHashFamily`.
4. **Priorización de Exámenes:** Se inyectó el bloque de "PRIORIDAD 0" en el orquestador global para buscar exámenes `PENDING` antes que solicitudes de contenido.

### Incidencia Pendiente (Bloqueante):
A pesar de la prioridad inyectada, el examen `7dcaa92c-c414-423a-885c-57d71ee3848a` permanece en `PENDING` sin entrar en la cola de procesamiento. Se sospecha de un desajuste en el enrutamiento de colas de Celery o suscripción de los workers.

---

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Fase 1: Diagnóstico de Infraestructura Celery
1. **Auditoría de Colas:** Ejecutar `python3 -m celery -A core inspect active_queues` para verificar a qué colas están suscritos los workers actuales.
2. **Verificación de Enrutamiento:** Comprobar en `core/settings.py` y `core/celery.py` si existe un `task_routes` que esté enviando `generate_exam_task` a una cola inexistente o no atendida.
3. **Trace Manual:** Ejecutar un script en `SWAP` que llame a `generate_exam_task.apply()` (síncrono) para el UUID del examen pendiente y capturar el traceback exacto si falla la instanciación.

### Fase 2: Normalización de la Generación
1. **Consolidación de Prioridades:** Una vez resuelto el problema de la cola, verificar que el orquestador procesa secuencialmente: 1º Examen, 2º Solicitud de Usuario, 3º Generación Masiva.
2. **Test de Stress:** Solicitar un examen y un contenido simultáneamente para validar que el examen interrumpe el flujo masivo según lo diseñado.

### Fase 3: Continuidad del Hito 24
1. Retomar las tareas de mantenimiento y ruegos según el histórico.
