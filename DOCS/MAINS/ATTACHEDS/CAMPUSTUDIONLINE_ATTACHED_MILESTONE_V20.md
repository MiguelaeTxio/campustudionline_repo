# Hito 20: Refinamiento del Proceso de Scraping de Datos (EN PROGRESO)

## Estado de la Sesión: SANEAMIENTO INTEGRAL (FASE 1 Y CÓRDOBA)
Se ha completado la depuración de la base de datos, eliminando 203 registros "ruido" (TFGs, Prácticas, Eventos) que afectaban tanto a la **Fase 1 (Andalucía Oriental)** completada, como a la parte ya ejecutada de la **Fase 2 (Córdoba/ESAD)**.

## Logros Técnicos:
1.  **Calidad del Dato:** Eliminación de asignaturas no lectivas mediante patrones de nombres (`purge_generic_subjects`), dejando los datasets de Almería, Granada, Málaga, Jaén y Córdoba limpios de carga administrativa.
2.  **Validación de Estructura:** Confirmación de integridad tras el borrado selectivo.

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
**Objetivo:** Organización de Infraestructura y Ejecución de Fase 2 (Andalucía Occidental).

1.  **Gestión y Organización de Scripts (Prioridad 1):**
    *   Creación de estructura de directorios en `/web_scrapping/` para segregar fases:
        *   `/PHASE_1_EAST/` (Almería, Granada, Málaga, Jaén).
        *   `/PHASE_2_WEST/` (Córdoba, Sevilla, Huelva, Cádiz).
    *   Migración y limpieza de scripts existentes a sus carpetas correspondientes.
2.  **Expansión a Sevilla (US):**
    *   Análisis de arquitectura web.
    *   Desarrollo de estrategia de scraping y *harvester*.
3.  **Expansión a Huelva (UHU):**
    *   Análisis de arquitectura web.
    *   Desarrollo de estrategia de scraping y *harvester*.
4.  **Expansión a Cádiz (UCA):**
    *   Evaluación preliminar y desarrollo de *harvester*.
