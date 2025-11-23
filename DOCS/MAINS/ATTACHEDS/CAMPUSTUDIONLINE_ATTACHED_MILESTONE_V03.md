# Hito 3: Ecosistema de Salas de Chat Globales y Contextuales (PAUSADO)

## Visión Estratégica (Redefinición Nov 2025)
Transformación del sistema de chat de un modelo "red social abierta" a un modelo "institucional y contextual". El chat deja de ser una funcionalidad aislada para convertirse en una capa de comunicación vinculada estrictamente al **contexto de estudio**.

## Especificaciones Funcionales

### 1. Salas Globales (Sistema)
*   **Sala General ("CampuStudiOnline"):** Sala única donde residen todos los usuarios registrados.
*   **Sala de Ayuda:** Canal directo de soporte comunitario.
*   **Automatización:** Los usuarios son añadidos automáticamente al registrarse (señal `post_save` en `User`).

### 2. Salas Contextuales (Automáticas)
*   **Concepto:** "Una sala por contexto de aprendizaje".
*   **Tipos:**
    *   **Académico:** Una sala única por `Subject` (Asignatura).
    *   **Contenido Libre:** Una sala única por `FreeContentSubCategory` (o `MasterCategory` si no tiene subcategoría).
*   **Acceso (Trigger):**
    *   El usuario **NO** puede unirse ni salir manualmente mediante botones de UI estándar.
    *   **Trigger:** Creación de una `ContentCopy` (Copia de Estudio).
    *   **Lógica:** Al crear una copia de estudio, el sistema detecta el contexto (Asignatura o Categoría) y añade al usuario a la sala de chat correspondiente. Si la sala no existe, el sistema la crea automáticamente.

### 3. Restricciones y Limpieza
*   **Eliminación:** Se elimina la capacidad de los usuarios de crear salas personalizadas.
*   **Depuración:** Se eliminarán o archivarán las salas públicas/privadas del modelo anterior que no encajen en este esquema.
*   **Unificación:** Fusión lógica de `chat` (genérico) y `academic_chat` bajo este nuevo paradigma.

## Plan de Implementación (Borrador)

1.  **Refactorización de Modelos:**
    *   Adaptar modelos de Chat para soportar vinculación directa a `Subject` y `Category`.
    *   Eliminar lógica de "Owner" (las salas son del sistema).

2.  **Implementación de Señales (Triggers):**
    *   `users.signals`: Al crear usuario -> Unir a Globales.
    *   `contents.signals`: Al crear `ContentCopy` -> Unir a Sala Contextual.

3.  **Migración de Datos:**
    *   Generar salas globales y poblar con usuarios existentes.
    *   Generar salas contextuales retroactivas basadas en las copias de estudio existentes.

4.  **Limpieza de UI:**
    *   Eliminar botones de "Crear Sala".
    *   Reorganizar la vista de lista de chats (Secciones: Global / Mis Asignaturas / Intereses).

