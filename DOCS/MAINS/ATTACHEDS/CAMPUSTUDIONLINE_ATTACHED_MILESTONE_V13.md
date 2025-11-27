# Hito Final 2: Documentación de Proyecto ("La Enciclopedia Galáctica")

**Propósito:** Crear un compendio de documentación externa como manual técnico del proyecto.
**Estado:** **PAUSADO** (Interrupción por Hotfix UX/Legal/Estabilidad).

## Bitácora de Sesión

### 27/11/2025 - Sesión de Hotfix Crítico (UX/Legal + Bugs 500)

#### 1. Ajuste de Terminología (UX/Legal)
*   **Intervención:** Cambio de nomenclatura pública.
*   **Cambio:** "Universidad" -> "**Institución**" (Modelos y Datos).
*   **Motivo:** Neutralidad y prevención legal.

#### 2. Corrección de Error 500 en Chats Académicos
*   **Problema:** `FieldError` al acceder a listas de chats.
*   **Solución:** Corrección de la ruta de búsqueda en `views.py` (`subject__academic_year__year`).

#### 3. Corrección de Error de Integridad (Borrado de Usuarios)
*   **Problema:** Imposibilidad de borrar usuarios por FKs hacia tablas inexistentes en el modelo actual.
*   **Causa:** Tablas zombis de versiones antiguas (`messaging_webpushsubscription`, `portafolio_shortmessage`) que retenían referencias.
*   **Solución:** Limpieza quirúrgica de la base de datos (DROP TABLE) para restaurar la integridad referencial.

## Tareas Pendientes (Documentación)
- [ ] Manual de Arquitectura.
- [ ] Referencia de Componentes.
- [ ] Guía de Dependencias.
