# Hito 25: Estrategia de Campaña Meta Ads

## 1. Visión y Objetivos
Establecer la infraestructura técnica, de seguimiento y de contenidos necesaria para el lanzamiento y optimización de campañas publicitarias en Meta (Facebook e Instagram Ads).

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Fecha de Inicio:** 13/12/2025

## 3. Hoja de Ruta Táctica (Continuación)

### 3.1. Infraestructura de Tracking (COMPLETADO)
*   [X] Implementación de Meta Pixel (Client-side) en base.html con lógica GDPR.
*   [X] Implementación de Conversions API (Server-side) vía Celery/facebook-business.
*   [X] Configuración de variables de entorno META_PIXEL_ID y META_CONVERSIONS_API_TOKEN.
*   [X] Implementación del evento 'CompleteRegistration' de forma híbrida con deduplicación.
*   [X] Depuración y corrección del error de sintaxis en `users/tasks.py`.

### 3.2. Implementación de Conversiones Clave (Próxima Tarea)
*   [ ] Implementar evento 'Lead' al completar el formulario de Contacto.
*   [ ] Implementar evento 'ViewContent' en la vista de detalle de cursos (ContentMaterial).
*   [ ] Implementar evento 'InitiateCheckout' en el inicio del proceso de pago.

### 3.3. Landing Pages y Catálogo
*   [ ] Definición de estructura de URLs para Landing Pages (en planificación).
*   [ ] Generación de feed de productos (cursos) XML/CSV para Meta Catalog.

## 4. Notas de Sesión
*   Sesión enfocada en la creación e integración de la infraestructura de tracking de Meta Ads (Pixel + CAPI).
*   Se creó el porfolio empresarial en Meta, se obtuvieron las claves de ID y Token.
*   Se introdujo la librería `facebook-business` y se implementó el evento `CompleteRegistration`.
*   Se solucionó el error crítico de `ModuleNotFoundError` causado por un error de sintaxis en la importación de la API de Facebook.
