# Hito 25: Estrategia de Campaña Meta Ads

## 1. Visión y Objetivos
Establecer la infraestructura técnica, de seguimiento y de contenidos necesaria para el lanzamiento y optimización de campañas publicitarias en Meta (Facebook e Instagram Ads).

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Fecha de Inicio:** 13/12/2025

## 3. Hoja de Ruta Táctica

### 3.1. Infraestructura de Tracking (COMPLETADO)
*   [X] Implementación de Meta Pixel (Client-side) en base.html con lógica GDPR.
*   [X] Implementación de Conversions API (Server-side) vía Celery/facebook-business.
*   [X] Configuración de variables de entorno META_PIXEL_ID y META_CONVERSIONS_API_TOKEN.
*   [X] Implementación del evento 'CompleteRegistration' de forma híbrida con deduplicación.
*   [X] Depuración y corrección del error de sintaxis en `users/tasks.py`.

### 3.2. Implementación de Conversiones Clave (COMPLETADO)
*   [X] Implementar evento 'Lead' al completar el formulario de Contacto o Reporte de Error.
*   [X] Implementar evento 'ViewContent' en la vista de detalle de cursos (ContentMaterial).
*   [X] Implementar evento personalizado 'RequestAssessment' al solicitar evaluación en la Sala de Estudio. (Sustituye a InitiateCheckout por estrategia MVP).

### 3.3. Landing Pages y Catálogo (COMPLETADO)
*   [X] Implementación de Feed de Productos RSS 2.0 extendido para Meta Catalog.
*   [X] Habilitación de ruta pública `/contents/feed/meta-catalog/`.
*   [X] Definición implícita de Landing Pages (Vistas de Detalle de Contenido).
*   [X] Depuración y corrección de error 500 en la generación del Feed.
*   [X] Subida y validación exitosa del catálogo en Meta Commerce Manager.

### 3.4. Configuración y Lanzamiento de Campaña (EN PROGRESO)
*   [X] Configuración del Origen de Datos (Feed) en Meta Commerce Manager.
*   [ ] Verificación de eventos (ViewContent, RequestAssessment) en Events Manager.
*   [ ] Creación de Creatividades y Copy.
*   [ ] Configuración de la Campaña de Conversiones en Ads Manager.
*   [ ] Lanzamiento y Fase de Aprendizaje.

## 4. Notas de Sesión
*   **14/12/2025 (EDC):** Sesión de depuración y validación final de la infraestructura. Se detectó y corrigió un error 500 en la generación del feed XML debido a múltiples fallos en cascada (`AttributeError` en `feeds.py`, `TypeError` por argumentos duplicados). Se corrigió un `AttributeError` en el SDK de Facebook en `users/tasks.py` y se limpiaron bloques de código CAPI erróneos en `contents/views.py`. Tras las correcciones, se guió en la subida y procesamiento exitoso del catálogo (1615 productos) en Meta Commerce Manager.
*   **14/12/2025 (MAMC):** Se completó la implementación técnica de la API de Conversiones (CAPI) para los eventos `ViewContent`, `Lead` y `RequestAssessment`. Se solucionó un error crítico de sintaxis en `users/tasks.py` y se corrigió la configuración de logs en `settings.py` para reactivar el script de monitoreo. Se implementó el Feed de Productos XML en `/contents/feed/meta-catalog/`.
*   **13/12/2025:** Sesión enfocada en la creación e integración de la infraestructura de tracking de Meta Ads (Pixel + CAPI). Se creó el porfolio empresarial en Meta, se obtuvieron las claves de ID y Token.
