# Hito de UX: Estandarización Sistémica de Botones

## 1. Filosofía y Problema Raíz

Esta sesión se origina por una inconsistencia visual detectada en la vista de detalle de contenido (`content_detail.html`), donde los botones de acción principal presentaban estilos y tamaños dispares. Sin embargo, una investigación más profunda revela que este no es un error aislado, sino un síntoma de un problema arquitectónico mayor: **la ausencia de una guía de estilo unificada y un sistema de componentes de UI centralizado para los botones en toda la plataforma CampuStudiOnline.**

La estilización actual, aplicada de forma individual en cada plantilla, ha generado una deuda técnica en la experiencia de usuario (UX) que se manifiesta en:
-   Uso inconsistente de clases de Bootstrap (ej. `btn-primary` vs. `btn-outline-primary`).
-   Falta de un lenguaje visual coherente para las acciones (ej. acciones primarias, secundarias, destructivas).
-   Disparidad en tamaños y alineaciones que degradan la percepción de profesionalidad de la aplicación.

Este sumario define una solución **sistémica y global**, prohibiendo parches locales y estableciendo un estándar a seguir para toda la plataforma.

## 2. Objetivo Estratégico

Establecer y aplicar un estándar de diseño de botones riguroso y coherente en toda la plataforma para unificar la experiencia de usuario, eliminar la deuda técnica visual y facilitar el mantenimiento futuro.

## 3. Plan de Acción Atómico y Fases

### Fase 1: Auditoría y Definición de Estándares

**3.1. Auditoría Empírica Exhaustiva:**
El primer paso es cuantificar el alcance del problema. Se debe ejecutar un comando en la raíz del proyecto para localizar todas las plantillas que implementan botones y analizar su variedad.
`grep -r 'class="btn' ./**/*.html`
La salida de este comando será la lista de trabajo para la Fase 2.

**3.2. Definición de la Guía de Estilo de Botones (Fuente Única de Verdad):**
Se establece la siguiente taxonomía de botones. **Todos los botones deben ser sólidos (sin usar `btn-outline-*`) para garantizar uniformidad.**

-   **Acción Primaria (Crear, Guardar, Enviar, Confirmar):**
    -   **Clase:** `btn btn-success` (Verde)
    -   **Ejemplo:** "Crear copia para estudio", "Guardar Cambios".

-   **Acción Secundaria (Editar, Ver Detalles, Navegar):**
    -   **Clase:** `btn btn-primary` (Azul)
    -   **Ejemplo:** "Editar", "Ver Resultados".

-   **Acción Destructiva (Eliminar, Borrar, Cancelar):**
    -   **Clase:** `btn btn-danger` (Rojo)
    -   **Ejemplo:** "Borrar", "Eliminar Cuenta".

-   **Acción de Advertencia o Especial (Favoritos, Destacar):**
    -   **Clase:** `btn btn-warning` (Amarillo)
    -   **Ejemplo:** "Añadir a Favoritos".

-   **Acción Informativa (Visita Guiada, Más Información):**
    -   **Clase:** `btn btn-info` (Celeste)
    -   **Ejemplo:** "Visita Guiada".

-   **Acción Neutra o de Retorno (Volver, Cerrar):**
    -   **Clase:** `btn btn-secondary` (Gris)
    -   **Ejemplo:** "Volver".

**3.3. Actualización del Documento Maestro:**
La guía de estilo definida en el punto 3.2 deberá ser incorporada como una nueva sección en el `{PROJECT_MASTER_DOC_PATH}` para asegurar su persistencia y consulta futura.

### Fase 2: Implementación y Refactorización Global

**4.1. Refactorización Sistemática:**
Utilizando la lista de archivos generada en la auditoría (3.1), se procederá a modificar **cada una de las plantillas** para que sus botones se adhieran estrictamente a la nueva guía de estilo.

**4.2. Caso de Estudio Piloto: `content_detail.html`:**
La refactorización comenzará con el archivo que originó esta sesión, `contents/templates/contents/content_detail.html`. La barra de acciones debe ser modificada para que todos los botones ("Volver", "Crear copia para estudio", "Añadir a Favoritos", "Visita Guiada") cumplan con el nuevo estándar, sirviendo como modelo para el resto de la refactorización.

## 5. Criterios de Aceptación (Definition of Done)

-   El 100% de los archivos de plantilla que contienen botones han sido refactorizados según la guía de estilo.
-   La guía de estilo de botones ha sido añadida y versionada en el `{PROJECT_MASTER_DOC_PATH}`.
-   La inspección visual de la plataforma en sus vistas clave no revela ninguna inconsistencia en el estilo de los botones.
