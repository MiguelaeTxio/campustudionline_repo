# Hito 22: Refactorización de Navegación de Sala de Estudio (User-Centric)

**Objetivo Estratégico:**
Implementar un modelo de navegación persistente y desnormalizado (`UserStudyNavigation`) que desacople la visualización de la jerarquía académica de las consultas en tiempo real, eliminando la fragilidad ante cambios de slugs y mejorando drásticamente el rendimiento.

**Problema Identificado:**
La navegación actual deduce la jerarquía (Universidad -> Rama -> Grado...) en tiempo real consultando las relaciones de cada `ContentCopy`. Esto genera:
1.  Consultas complejas y costosas.
2.  Errores 404 si algún slug intermedio cambia o es inconsistente.
3.  Imposibilidad de manejar estados "vacíos" o "parciales" de forma elegante.

**Solución Propuesta (Arquitectura):**
1.  **Nuevo Modelo `UserStudyNavigation`:** Relación 1:1 con `User`. Almacena un `JSONField` con el árbol de navegación pre-calculado del usuario.
2.  **Actualización por Señales:** `post_save` y `post_delete` en `ContentCopy` disparan una regeneración del JSON de ese usuario.
3.  **Vistas O(1):** La vista de "Sala de Estudio" simplemente lee el JSON y lo renderiza. Cero consultas jerárquicas.

**Hoja de Ruta:**
1.  Definición del modelo `UserStudyNavigation` y estructura del JSON schema.
2.  Implementación del servicio `NavigationTreeBuilder` para generar el JSON a partir de las copias.
3.  Implementación de Señales en `contents/signals.py`.
4.  Migración de `study_room_views.py` para consumir el nuevo modelo.
5.  Creación de comando de gestión `rebuild_user_navigation` para inicializar el sistema.
