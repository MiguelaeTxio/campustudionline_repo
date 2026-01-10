# Anexo del Hito 20: Refinamiento y Expansión del Proceso de Scraping de Datos

## 1. Visión y Objetivos
Consolidación de la recolección de datos académicos. Tras la finalización exitosa de la UMA, el foco se desplaza a la integración de la Universidad de Jaén (UJA).

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Última Actualización:** 10/01/2026
*   **Logros Recientes:**
    *   **UMA Completada:**
        *   Scraper `v4` con tolerancia a huecos y reanudación inteligente.
        *   Limpieza de datos (eliminación de TFG, Practicum, etc.).
        *   Importador reescrito para estructura plana.
        *   Importación exitosa de 4321 registros y estandarización de nombre ("Institución Académica de Málaga").

## 3. Hoja de Ruta para la Próxima Sesión (LEY SUPREMA)
### Tarea 1: Reconocimiento y Scraping UJA
- **Objetivo:** Desarrollar `uja_harvester.py`.
- **Fuente:** [Catálogo UJA 2025-26](https://uvirtual.ujaen.es/pub/es/informacionacademica/catalogofichasdocentesasignaturas/p/2025-26/4/135A)
- **Estrategia Técnica:**
    - Analizar el DOM de la plataforma `uvirtual.ujaen.es`.
    - Determinar patrones de URL para Grados y Asignaturas.
    - Implementar extracción de Guías Docentes.
    - **Salida Esperada:** `uja_raw_data.json` en local.

### Tarea 2: Normalización e Importación
- **Acción:** Adaptar `clean_uma_local.py` para la UJA (`clean_uja_local.py`).
- **Acción:** Crear `import_uja_data.py` basándose en el modelo de importación plana consolidado con la UMA.
