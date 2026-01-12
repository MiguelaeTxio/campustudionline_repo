# Anexo del Hito 20: Refinamiento y Expansión del Proceso de Scraping de Datos

## 1. Visión y Objetivos
Consolidación de la recolección de datos académicos. Tras la integración exitosa de la UMA y la UJA, y la reconstrucción arquitectónica de la UGR (Maior/Minor), el foco se desplaza a la Universidad de Almería (UAL) para completar la Fase 1: Andalucía Oriental.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Última Actualización:** 12/01/2026
*   **Logros Recientes:**
    *   **UJA Completada:** Desarrollo de `uja_refiner_v7` con detección de estructura basada en DIVs y validación de rangos de curso (Sanity Check 1-6). Importación inteligente con reubicación de 1.611 asignaturas a sus cursos correctos.
    *   **UGR Reconstruida:** Solución a la contaminación cruzada en grados de lenguas. Implementación de identidad por nombre completo (Maior/Minor), eliminación de 5.400 duplicados técnicos y purga de contenidos huérfanos preservando datos de usuario.

## 3. Hoja de Ruta para la Próxima Sesión (LEY SUPREMA)
### Tarea 1: Reconocimiento y Scraping UAL (Almería)
- **Objetivo:** Desarrollar `ual_harvester.py`.
- **Fuente:** Portal de Grados de la Universidad de Almería.
- **Estrategia Técnica:**
    - Análisis de estructura web (detección de patrones de curso/semestre).
    - Extracción de catálogo completo.
    - **Salida Esperada:** `ual_raw_data.json` en local.

### Tarea 2: Normalización e Importación UAL
- **Acción:** Crear `clean_ual_local.py` para estandarización de nombres.
- **Acción:** Implementar `import_ual_data.py` bajo la entidad "Institución Académica de Almería".
