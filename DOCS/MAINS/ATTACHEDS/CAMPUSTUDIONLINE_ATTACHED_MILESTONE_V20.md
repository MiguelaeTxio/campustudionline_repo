# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/DOCS/MAINS/ATTACHEDS/CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md
# Hito 20: Refinamiento del Proceso de Scraping de Datos (PAUSADO)

## Estado de la Sesión: SEVILLA COMPLETADA
Se ha culminado con éxito la integración de la Institución Académica de Sevilla. El proceso se realizó íntegramente en el borde (dispositivo local), filtrando TFGs y prácticas antes de la ingesta.

## Logros Técnicos:
1.  **Higiene Estructural:** Reorganización del directorio `/web_scrapping/` y `/data/` segregando por fases geográficas (EAST/WEST) y utilidades.
2.  **Cosecha Masiva:** Extracción de 5015 asignaturas enriquecidas mediante el procesamiento dinámico de SEVIUS4 (envíos POST para descarga de PDFs).
3.  **Integridad RUCT:** Implementación de un mapeador inteligente en el comando de importación para asignar los grados de Sevilla a sus 5 ramas oficiales de conocimiento.
4.  **Calidad del Dato:** 96.8% de cobertura en objetivos y temarios.

## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
**Objetivo:** Expansión de la Fase 2 a la Universidad de Cádiz (UCA).

1.  **Análisis de Arquitectura (UCA):** Identificación del portal de transparencia y catálogo de grados/asignaturas.
2.  **Desarrollo de Sonda:** Creación de `uca_link_extractor.py` para obtener el listado maestro de títulos.
3.  **Estrategia de Enriquecimiento:** Evaluar si la UCA dispone de PDFs directos o requiere navegación dinámica (tipo SEVIUS).
4.  **Procesamiento en el Borde:** Ejecución local de la cosecha y refinamiento.
