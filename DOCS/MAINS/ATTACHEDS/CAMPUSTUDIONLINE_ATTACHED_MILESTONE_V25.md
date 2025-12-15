# Hito 25: Estrategia de Campaña Meta Ads

## 1. Visión y Objetivos
Establecer la infraestructura técnica, de seguimiento y de contenidos necesaria para el lanzamiento y optimización de campañas publicitarias en Meta (Facebook e Instagram Ads).

## 2. Estado del Hito
*   **Estado:** COMPLETADO
*   **Fecha de Inicio:** 13/12/2025
*   **Fecha de Finalización:** 14/12/2025

## 3. Hoja de Ruta Táctica (COMPLETADA)
*   [X] Implementación de Meta Pixel y Conversions API (Híbrido).
*   [X] Implementación de eventos 'CompleteRegistration', 'Lead', 'ViewContent', y 'RequestAssessment'.
*   [X] Implementación y depuración de Feed de Productos para Meta Catalog.
*   [X] Configuración completa de la infraestructura en Meta Business Manager (Pixel/Dataset, Cuenta Publicitaria, permisos).
*   [X] Lanzamiento de la primera campaña de prospección con catálogo.

## 4. Notas de Sesión
*   **14/12/2025 (NRA):** Sesión de finalización del hito. Se detectó y corrigió una implementación no conforme a la AEPD del banner de cookies en `base.html`. Se ajustó `contents/views.py` para habilitar la deduplicación de eventos híbrida (Pixel+CAPI). Se guio en la depuración de la configuración de Meta Business, creando y asignando los activos necesarios (Dataset, Cuenta Publicitaria). Se configuró y lanzó la primera campaña de Ventas, solucionando errores de `product set` y de ubicaciones incompatibles. Se añadieron parámetros UTM para el seguimiento. La campaña quedó publicada y "En revisión".
