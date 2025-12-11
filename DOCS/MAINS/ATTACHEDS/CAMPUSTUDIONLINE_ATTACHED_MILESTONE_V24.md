# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Estado:** **EN PROGRESO - SOPORTE DE PLATAFORMA ACTIVO**

## Bitácora de Sesión (09/12/2025 - 10/12/2025)
*   **Actividad:** Depuración Profunda del Orquestador (Celery).
*   **Logros:** Corrección de silenciamiento de excepciones, Fusible Global, Hot-Swap y Bucle de Resistencia Local.

## Bitácora de Sesión (11/12/2025) - Mañana
*   **Incidencia Resuelta (Content Gating):** Se detectó y corrigió una regresión crítica en la aplicación `contents` donde los usuarios anónimos podían acceder al contenido completo de materiales privados/públicos sin restricción visual.
*   **Solución Técnica:**
    *   **Backend (`contents/views.py`):** Inyección explicita del flag `is_gated` en el contexto de `content_detail`.
    *   **Frontend (`content_detail.html`):** Restauración de estilos CSS para efecto *fade-out* (desvanecimiento) y reimplementación del bloque CTA (*Call To Action*) para registro/login.

## Bitácora de Sesión (11/12/2025) - Tarde
*   **Incidencia Crítica Resuelta (Orquestador - Bucle Infinito):**
    *   **Diagnóstico:** Fallo en la lógica de comprobación del "Fusible Global" que permitía reintentos infinitos (contadores > 120/10) tras un fallo de ACK en la cola de mensajes.
    *   **Solución:** Implementación de un parche de "Drenaje Rápido" en `tasks.py` que aborta inmediatamente la ejecución si la tarea ya está marcada como `FAILED_FATAL`, permitiendo vaciar la cola de RabbitMQ sin saturar la DB.
    *   **Rescate:** Se rescató y reinició exitosamente la tarea `716774f2` afectada por el fallo, asegurando la entrega del contenido al usuario.
*   **Optimización de Rendimiento (Búsqueda Global):**
    *   **Diagnóstico:** Latencia extrema en `global_search_view` debido a la carga ansiosa (Eager Loading) de campos de texto masivos (`markdown_content`, `html_content`) para todos los resultados de la búsqueda.
    *   **Solución:** Refactorización de la vista utilizando `QuerySet.defer()` y `QuerySet.only()` para diferir la carga de campos pesados y traer únicamente metadatos ligeros (título, ID, fecha). Se corrigió un conflicto de `FieldError` ajustando la estrategia de carga para modelos académicos ligeros.

## Hoja de Ruta (Siguientes Pasos)

### 1. MANTENIMIENTO CORRECTIVO INTEGRAL
*   **Objetivo:** Atención a cualquier incidencia, error lógico o regresión que surja en cualquier módulo de la plataforma.
*   **Alcance:** Frontend, Backend, Base de Datos y Orquestación.

### 2. MONITORIZACIÓN CONTINUA
*   Vigilancia de estabilidad del Orquestador de Tareas (post-refactorización).
*   Verificación de la experiencia de usuario (UX) en flujos de navegación.
