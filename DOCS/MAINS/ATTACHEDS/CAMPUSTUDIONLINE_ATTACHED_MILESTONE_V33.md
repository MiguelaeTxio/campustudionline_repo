# Anexo del Hito 33: Optimización de Comunicaciones Administrativas

## 1. Resumen de Implementación
- **Dashboard de Envío:** Implementado en el panel administrativo (`global_settings`) con arquitectura de previsualización en tiempo real (WYSIWYG) mediante JavaScript robusto.
- **Estandarización de Emails:** Las plantillas `admin_general_announcement` (.html y .txt) han sido refactorizadas para incluir bloques inmutables (saludo, introducción y despedida fija).
- **Gestión de Preferencias RGPD:**
    - Modelo `UserProfile` actualizado con campo `accepts_marketing`.
    - Implementación de `email_extras` (templatetag) para generación de URLs de baja firmadas.
    - Vista `unsubscribe_view` operativa para desuscripción con un solo clic.
- **Resiliencia de Infraestructura:** Refactorización de `orchestrator/signals.py` mediante un dispatcher seguro para evitar bloqueos por saturación de conexiones en Redis.
- **Depuración Académica:** Reparación del error de resolución de URL en los breadcrumbs académicos (`academic_year_list`).

**Estado:** COMPLETADO
