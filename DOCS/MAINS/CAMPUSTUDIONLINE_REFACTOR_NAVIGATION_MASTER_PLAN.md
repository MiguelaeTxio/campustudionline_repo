# PLAN MAESTRO: Refactorización de Navegación y Limpieza de Deuda Técnica
# ID de Proyecto: CAMPUSTUDIONLINE
# Fecha de Inicio: 22/11/2025
# Estado: EN PROGRESO

---

## 1. Objetivo Estratégico
Eliminar la deuda técnica acumulada por estructuras de clasificación obsoletas ("Jerarquía Intelectual" y "Contenido Libre Legacy") y reemplazar el sistema de navegación en tiempo real por un modelo persistente y optimizado (`UserStudyNavigation`).

## 2. Alcance de la Limpieza
El análisis de impacto ha identificado dependencias críticas en los siguientes módulos que deben ser eliminadas **antes** de tocar los modelos de base de datos:
*   **Orquestador:** `orchestrator/tasks.py` (Crea dinámicamente las jerarquías obsoletas).
*   **Comandos de Gestión:** Múltiples scripts en `contents/management/commands` y `content_automation` dedicados al mantenimiento de estas estructuras.
*   **Interfaz de Administración:** `contents/admin.py`.
*   **Formularios:** `contents/forms.py` y templates asociados.
*   **Búsqueda:** `search/views.py` y `search/urls.py`.
*   **Señales:** `contents/signals.py`.

---

## 3. Hoja de Ruta de Ejecución

### FASE 1: Desactivación Lógica (Orquestador) [COMPLETADO]
*Objetivo: Evitar que el sistema siga generando o buscando datos en las tablas a eliminar.*
- [x] **Modificar `orchestrator/tasks.py`**:
    - [x] Eliminar imports de `KnowledgeArea`, `Discipline`, `MainCategory`.
    - [x] Eliminar lógica de `get_or_create` para estas entidades en la generación de tareas.
    - [x] Eliminar asignación de `topic` en la creación de `ContentMaterial`.

### FASE 2: Eliminación de Herramientas Obsoletas [COMPLETADO]
*Objetivo: Eliminar código muerto que fallará cuando falten los modelos.*
- [x] **Eliminar Scripts en `contents/management/commands/`**:
    - [x] `update_free_content_flags.py`
    - [x] `clean_content_hierarchy.py`
    - [x] `resync_free_content_flags.py`
    - [x] `clean_autogen_content.py`
    - [x] `ensure_free_content_structure.py`
    - [x] `setup_default_categories.py`
- [x] **Eliminar Scripts en `content_automation/management/commands/`**:
    - [x] `correct_academic_classification.py`

### FASE 3: Limpieza de Interfaz y Formularios [COMPLETADO]
*Objetivo: Desacoplar el frontend y el admin de los modelos legacy.*
- [x] **Limpiar `contents/forms.py`**: Eliminar campos `topic`, `main_category`, `discipline`, `knowledge_area`.
- [x] **Limpiar `contents/admin.py`**: Eliminar registros de modelos legacy y referencias en `ContentMaterialAdmin`.
- [x] **Limpiar Templates**:
    - [x] `contents/templates/contents/create_edit_content.html` (Selectores AJAX).
    - [x] `contents/templates/contents/favorite_folder_detail.html` (Referencias a `material.topic`).

### FASE 4: Limpieza de Consumidores (Search y Signals) [CORRECCIÓN PENDIENTE]
*Objetivo: Eliminar referencias de lectura.*
- [x] **Refactorizar `search/views.py`**: Eliminar bloque "Intelectual" en búsqueda global y vistas passthrough.
- [x] **Refactorizar `search/urls.py`**: Eliminar rutas `academic/`.
- [x] **Limpiar `contents/signals.py`**: Eliminar lógica de sincronización de flags `has_free_content` en jerarquía intelectual.

### FASE 5: Cirugía de Modelos (Base de Datos) [COMPLETADO]
*Objetivo: Alteración destructiva del esquema.*
- [x] **Modificar `contents/models.py`**:
    - [x] Eliminar modelos: `KnowledgeArea`, `Discipline`, `MainCategory`, `Topic`, `FreeContentTopic`, `FreeContentCategory`.
    - [x] Eliminar campos en `ContentMaterial`: `topic`, `free_category`.
    - [x] Eliminar funciones helper obsoletas.
- [ ] **Crear Migración**: `makemigrations contents`.

### FASE 6: Nueva Arquitectura de Navegación [PENDIENTE]
*Objetivo: Implementar `UserStudyNavigation`.*
- [ ] **Definir Modelo**: Añadir `UserStudyNavigation` a `contents/models.py` (Ya incluido en Fase 5).
- [ ] **Implementar Servicio**: Crear `contents/services/navigation_builder.py`.
- [ ] **Conectar Señales**: Invocar el builder en `post_save`/`post_delete` de `ContentCopy`.
- [ ] **Actualizar Vistas**: Modificar `study_room_views.py` para consumir el JSON.
- [ ] **Comando de Inicialización**: Crear script para generar el árbol para usuarios existentes.

---

## 4. Registro de Sesiones
*   **Sesión 1:** Análisis de impacto, definición de estrategia y ejecución de fases 1 a 5.
