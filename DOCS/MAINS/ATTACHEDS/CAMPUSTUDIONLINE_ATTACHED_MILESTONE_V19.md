# /home/MiguelAeTxio/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/HITO_V19_DIRECTORIOS_ANEXO.md
**Título:** Anexo de Seguimiento: Hito 19 - Re-arquitectura de los Directorios de Navegación

**Filosofía:** Este documento es la única fuente de verdad para la planificación, ejecución y seguimiento del hito de re-arquitectura de los directorios de navegación.

---

#### **1. Visión General del Hito**

El objetivo de este hito es mejorar drásticamente la experiencia de usuario y la descubribilidad del contenido. Se re-diseñarán los directorios académico, intelectual y personal para mostrar siempre la estructura jerárquica completa. Los elementos que no contengan material de estudio serán visualmente diferenciados (ej. con un fondo gris) pero permanecerán completamente navegables, permitiendo al usuario explorar la estructura completa de la plataforma y solicitar la creación de contenido en las áreas vacías a través del sistema de solicitudes existente.

---
#### **2. Estado General Actual**
El hito se encuentra **COMPLETADO**. La refactorización del Directorio Académico y la implementación de la funcionalidad de Favoritos están terminadas.

---

#### **3. Hoja de Ruta Detallada del Hito**

**FASE 1: Re-arquitectura del Directorio Académico**

*   **Tarea 1.1: Auditar la Implementación Actual**
    *   **Descripción:** Realizar una auditoría exhaustiva de las plantillas y vistas del Directorio Académico para identificar todos los puntos de modificación necesarios.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 1.2: Refactorizar la Lógica de Datos**
    *   **Descripción:** Se ha refactorizado la lógica del backend para el Directorio Académico. Se ha implementado un campo booleano `has_public_content` en los modelos de la jerarquía (`University` -> `Branch` -> `Degree` -> `Subject`), un sistema de `signals` para la sincronización automática y un comando de gestión para el `backfilling` de los datos existentes.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 1.3: Implementar la Lógica de Diferenciación Visual**
    *   **Descripción:** Se han refactorizado las vistas y la plantilla del Directorio Académico para utilizar el nuevo campo `has_public_content` y una regla de CSS canónica para la diferenciación visual, solucionando los problemas de paginación y renderizado.
    *   **Estado:** `[COMPLETADA]`

**FASE 2: Re-arquitectura del Directorio Intelectual y Personal (INVALIDADA)**

*   *Cambio de Estrategia (30/09/2025):* Se ha decidido pivotar la estrategia. El objetivo ya no es replicar el patrón del Directorio Académico, sino transformar este directorio en un "Directorio de Contenidos Libres" con una lógica y funcionalidad propias.

---

**FASE 3: Re-arquitectura del Directorio de Contenidos Libres (NUEVO)**

*   **Tarea 3.1: Renombramiento de Interfaz**
    *   **Descripción:** Cambiar el `verbose_name` de "Directorio Intelectual" a "Directorio de Contenidos Libres".
    *   **Estado:** `[COMPLETADA]`
*   **Tarea 3.2: Refactorización de la Lógica de Consulta y Arquitectura**
    *   **Descripción:** Corrección de la lógica de filtrado del directorio. Se implementó un nuevo campo booleano `has_free_content` en la jerarquía intelectual (`KnowledgeArea` a `Topic`), junto con señales de sincronización automática y un comando de gestión (`update_free_content_flags`) para poblar los datos existentes, asegurando que el directorio solo muestre contenido no académico de forma eficiente.
    *   **Estado:** `[COMPLETADA]`
*   **Tarea 3.3: Implementación de Funcionalidad de Solicitud y Notificación (Flujo Completo)**
    *   **Descripción:** Implementación completa del sistema de solicitud de contenido libre: creación de modelos, vistas, formularios, **y el flujo de notificación bidireccional**. Se añadió el Guardián Lógico en `tasks.py` para asegurar que el contenido generado tenga clasificación, y se implementaron notificaciones Push/Email para administradores, así como feedback por correo al usuario al aprobar/rechazar la solicitud.
    *   **Estado:** `[COMPLETADA]`
*   **Tareas Pendientes:** Finalización de la UX y Estabilización (Ver FASE 4).

---

**FASE 4: Estabilización y Mejoras de Usabilidad (NUEVA)**

*   **Tarea 4.1: Corrección de Flujo de Aprobación y Bug Visual**
    *   **Descripción:** Se corrigió el bug que impedía el feedback al usuario tras aprobar una solicitud (al encolar la tarea). Se resolvió el bug del título duplicado ("eco") en la vista de creación de tareas.
    *   **Estado:** `[COMPLETADA]`
*   **Tarea 4.2: Implementación del Flujo de Triage Completo en el Centro de Control**
    *   **Descripción:** Se ha refactorizado por completo el `Centro de Control de Contenidos` para incluir un flujo de triage robusto. Ahora se muestran botones individuales por solicitud para "Revisar", "Aprobar", "Rechazar" y "Eliminar". Se ha refactorizado la vista de revisión para ser coherente con el flujo y se ha corregido un error de arquitectura en las señales que impedía el envío de correos de feedback.
    *   **Estado:** `[COMPLETADA]`

---

**FASE 5: Implementación del Flujo de Trabajo Iterativo (NUEVA)**

*   **Tarea 5.1: Implementar el Ciclo "Detener y Revisar"**
    *   **Descripción:** El `Centro de Control` debe permitir a un administrador corregir el rumbo de una tarea de generación que ha empezado a producir resultados incorrectos. Se implementará un ciclo de "Generar -> Revisar Logs -> Detener -> Corregir -> Regenerar" sin necesidad de eliminar la solicitud original.
    *   **Estado:** `[COMPLETADA]`

---

**FASE 6: Backend - Modelos y Lógica de Cuotas y Favoritos (NUEVA)** `[INVALIDADO]`

*   **Tarea 6.1: Implementación del Sistema de Creación y Cuotas de `ContentMaterial` para Usuarios:** `[INVALIDADO]`
    *   **Descripción:**
        1. Se implementó la vista y el formulario para que los usuarios estándar creen un `ContentMaterial` original.
        2. Se implementó la lógica de cuotas en la vista para verificar la pertenencia a grupos (`administradores` o `colaboradores`).
        3. La lógica cuenta los materiales creados por el usuario y bloquea la creación si se excede la cuota de 1 público y 1 privado.
        4. Se implementó un validador para limitar el tamaño del contenido Markdown.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 6.2: Implementación del Sistema de Favoritos:** `[INVALIDADO]`
    *   **Descripción:** Se estableció una relación `ManyToManyField` entre el `users.UserProfile` y `contents.ContentMaterial` para gestionar los favoritos.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 6.3: Creación del Modelo de Organización de Favoritos en la App `contents`:** `[INVALIDADO]`
    *   **Descripción:** Se creó el modelo `FavoriteFolder` en la aplicación `contents` con las relaciones necesarias para una estructura de directorios anidada.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 6.4: Lógica de la Carpeta Fija "Mis Publicaciones":** `[INVALIDADO]`
    *   **Descripción:** Se implementará la lógica para asegurar la existencia de la carpeta fija "Mis Favoritos". Los `ContentMaterial` creados por el usuario (`creator=request.user`) se listarán bajo una sección "Mis Publicaciones" y no serán parte del sistema de carpetas de favoritos.
    *   **Estado:** `[COMPLETADA]`

**FASE 7: Backend - Vistas y Endpoints para la Nueva Funcionalidad (NUEVA)** `[INVALIDADO]`

*   **Tarea 7.1: Refactorización de la Vista del Directorio Personal:** `[INVALIDADO]`
    *   **Descripción:** Se refactorizó la vista `contents.views.personal_workspace_view` para aceptar un `username` opcional, lo que le permite funcionar como el Espacio de Trabajo Privado (sin `username`) y como la vista de Materiales Públicos de otro usuario (con `username`), resolviendo el `NoReverseMatch`. Se corrigió el `FieldError` en la consulta ORM con la cláusula `order_by('-updated_at')`.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 7.2: Creación de Endpoints para la Gestión de Favoritos:** `[INVALIDADO]`
    *   **Descripción:** Se crearán vistas/endpoints (probablemente para ser consumidos con HTMX/JS) que manejen la lógica de: Añadir/quitar favoritos, Crear/Renombrar/Eliminar carpetas, Mover favoritos.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 7.3: Modificación de la Vista de Creación de Contenido:** `[INVALIDADO]`
    *   **Descripción:** La vista `contents/views.py` asociada a `create_edit_content.html` fue modificada para verificar la cuota del usuario antes de permitir la creación de un nuevo `ContentMaterial`.
    *   **Estado:** `[COMPLETADA]`

**FASE 8: Frontend - Implementación de la Interfaz de Explorador de Archivos (NUEVA)** `[INVALIDADO]`

*   **Tarea 8.1: Rediseño de la Plantilla del Directorio Personal:** `[INVALIDADO]`
    *   **Descripción:** La plantilla `contents/templates/contents/personal_workspace.html` fue refactorizada para integrar el nuevo componente de paginación (`pagination_controls.html`), corrigiendo la paginación manual y la regresión de `NoReverseMatch`. El resto del diseño (estructura de árbol de directorios) está pendiente.
*   **Estado:** `[COMPLETADA]`

*   **Tarea 8.2: Implementación de la Lógica de Interfaz:** `[INVALIDADO]`
    *   **Descripción:** Se implementará el código JavaScript/HTMX necesario para interactuar con los endpoints del backend, permitiendo acciones como crear carpetas, arrastrar y soltar favoritos entre carpetas, y mostrar menús contextuales.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 8.3: Integración del Botón "Añadir a Favoritos":** `[INVALIDADO]`
    *   **Descripción:** Se añadirá un botón y la lógica correspondiente en la plantilla `contents/templates/contents/content_detail.html` para permitir a los usuarios marcar/desmarcar un contenido como favorito.
    *   **Estado:** `[COMPLETADA]`

---
*   **Motivo de Invalidación (06/10/2025):** Las Fases 6, 7 y 8 fueron ejecutadas pero se abandona por malfuncionamiento y se decide crear un prototipo aislado (`favorites_prototype`). Estas fases quedan como registro histórico de un plan de acción erróneo.
---

**FASE 9 (ACTUAL): Prototipado de la Interfaz del Directorio Personal en App Aislada**

*   **Descripción:** Para evitar la desestabilización de la aplicación principal `contents`, la funcionalidad del explorador de favoritos se está desarrollando y validando en una aplicación de prototipo aislada (`favorites_prototype`). Se atravesó una fase de depuración crítica donde se identificó la ausencia de la librería `hyperscript.org` como causa raíz de los fallos iniciales. Se pivotó a una arquitectura "Multi-Page" que ha sido implementada y validada con éxito.
*   **Estado:** `[COMPLETADA]` - El prototipo es ahora completamente funcional, incluyendo navegación jerárquica y operaciones CRUD (Crear, Renombrar, Eliminar). Sirve como una implementación de referencia (`PAIR`) validada para su futura integración en la aplicación `contents`.

---

**FASE 10: Integración y Estabilización de Favoritos (NUEVA)**

*   **Tarea 10.1: Migración Atómica de Funcionalidad (`PAIR`)**
    *   **Descripción:** Se ha transferido la lógica completa y validada de `favorites_prototype` a la aplicación `contents`, incluyendo vistas, URLs y plantillas. La arquitectura funcional ya está integrada en la aplicación principal.
    *   **Estado:** `[COMPLETADA]`

*   **Tarea 10.2: Depuración de Bug de Visualización**
    *   **Descripción:** Tras la integración, se ha detectado que la plantilla `favorite_folder_detail.html` no renderiza la lista de `ContentMaterial` asociados a una `FavoriteFolder`.
    *   **Estado:** `[COMPLETADA]`

---

**FASE 11: Implementación y Depuración de la Funcionalidad "Mover"**

*   **Descripción:** Se implementó el backend y la interfaz de usuario para permitir mover materiales entre carpetas de favoritos. Se atravesó una fase de depuración intensiva para corregir un `AttributeError` en la vista que provocaba un error 500, y un `VariableDoesNotExist` combinado con un error de lógica en la plantilla recursiva que impedía la correcta visualización del árbol de directorios en el modal de destino.
*   **Estado:** `[COMPLETADA]`

---

**FASE 12: Estabilización y Refinamiento del Explorador de Favoritos**

*   **Descripción:** Se ha completado la fase inicial de estabilización del explorador. Se resolvió un `AttributeError` crítico en `django-treebeard` mediante la purga de datos corruptos de la BBDD. Se restauró la funcionalidad del botón "Añadir a Favoritos" en la vista de detalle de contenido, y se corrigieron bugs visuales en la botonera de acciones para una experiencia de usuario coherente.
*   **Estado:** `[COMPLETADA]`
*   **Tareas Pendientes:**
    *   **Expandir Funcionalidad "Toggle Favorite":** Integrar el botón "Añadir/Quitar de Favoritos" en todas las vistas de listado de materiales para una UX consistente, incluyendo:
        *   Directorio Personal ("Mis Publicaciones").
        *   Directorio Académico.
        *   Directorio de Contenidos Libres.
*   **Resumen de Finalización:** Se ha integrado con éxito el botón "Añadir/Quitar de Favoritos" en todas las vistas de listado de materiales, completando la tarea pendiente. Durante el proceso, se solucionaron los bugs críticos (Error 500) y de UX (refresco del modal) que surgieron, dejando la funcionalidad estable y completa.
