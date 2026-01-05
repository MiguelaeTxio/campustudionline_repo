# Anexo del Hito 35: Optimización de Infraestructura Redis

## 1. Visión y Objetivos
Eliminar los colapsos por "Max number of clients" en Redis Cloud (límite 30) mediante la optimización de la gestión de conexiones y tareas.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Última Actualización:** 05/01/2026

## 3. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Tarea 1: Refactorización de Eventos de Meta
- **Problema:** Se disparan ráfagas de tareas `send_meta_conversion_event` por cada clic, saturando Redis.
- **Acción:** Implementar un sistema de "Batching". Almacenar eventos en BD y procesarlos con una única tarea cada 15 minutos.

### Tarea 2: Parches de Configuración (Settings)
- **Acción:** Definir en `core/settings.py` los límites de pool:
    - `CELERY_BROKER_POOL_LIMIT = 4`
    - `CELERY_REDIS_MAX_CONNECTIONS = 20`

### Tarea 3: Mejora de Robustez en Arranque
- **Acción:** Modificar `start_unified_workers.sh` para incluir un retardo (`sleep 10`) y forzar concurrencia 1 (`-c 1`) por defecto.

### Tarea 4: Limpieza de Resultados
- **Acción:** Configurar `CELERY_RESULT_EXPIRES` a 3600 segundos para evitar acumulación de llaves en Redis.
