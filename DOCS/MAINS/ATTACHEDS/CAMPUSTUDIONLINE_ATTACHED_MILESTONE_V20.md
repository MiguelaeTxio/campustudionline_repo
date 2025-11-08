# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos

---

## 1. Visión General y Justificación

Este hito se crea para abordar las incidencias de integridad de datos detectadas durante la depuración de otras funcionalidades. Un proceso de scraping de datos robusto y limpio es fundamental para la estabilidad de la plataforma y la calidad del contenido generado automáticamente. El objetivo es refinar los scripts de scraping existentes para prevenir la ingesta de datos duplicados o ambiguos.

---

## 2. Objetivos Específicos

### 2.1. Eliminación de Duplicados por Especificadores Geográficos

*   **Problema:** El scraper actual crea entidades duplicadas para titulaciones que se imparten en diferentes campus o ciudades (ej. "Grado en X" y "Grado en X (Ciudad)").
*   **Solución:** Modificar la lógica de parsing para identificar y eliminar sistemáticamente los sufijos geográficos de los nombres de las titulaciones, unificando las entradas.

### 2.2. Eliminación de Duplicados por Idioma de Impartición

*   **Problema:** Se ha postulado que el scraper podría estar creando duplicados de asignaturas cuando estas se ofrecen en múltiples idiomas (ej. "Introduction to Physics" y "Introducción a la Física").
*   **Solución:** Implementar una lógica de detección y fusión que identifique estas asignaturas como una única entidad, posiblemente priorizando la versión en castellano o estableciendo una relación explícita entre ellas.

---

## 3. Estado Actual

*   **Estado:** `PAUSADO`
*   **Hoja de Ruta:** La implementación de estas mejoras se abordará en una sesión de trabajo dedicada a la integridad de los datos de origen.
