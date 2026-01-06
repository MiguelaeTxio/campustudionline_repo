# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos (Integración UMA)

## 1. Visión y Objetivos
Ampliación de la capacidad de recolección de datos de la plataforma para integrar la Universidad de Málaga (UMA).

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Última Actualización:** 06/01/2026

## 3. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
### Tarea 1: Ingeniería Inversa y Análisis UMA
- **Objetivo:** Analizar la estructura web de la UMA para determinar los endpoints de Grados, Asignaturas y Guías Docentes.
- **Acción:** Crear script de exploración inicial `web_scrapping/uma_audit_tool.py`.

### Tarea 2: Desarrollo del Harvester Base
- **Objetivo:** Implementar la clase base para la extracción de la UMA.
- **Archivo:** `web_scrapping/uma_harvester.py`.
- **Referencia (`PAIR`):** Utilizar `uco_harvester_v19.py` como implementación de referencia.

### Tarea 3: Integración de Datos
- **Objetivo:** Definir el esquema JSON de salida y asegurar la compatibilidad con el módulo `academic_structure`.
