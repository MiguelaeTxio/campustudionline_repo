# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos (Integración UMA)

## 1. Visión y Objetivos
Integración completa de la oferta académica de la Universidad de Málaga (UMA) mediante la extracción masiva de guías docentes (PDF) y su estructuración para la plataforma.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (FALLO TÉCNICO EN ORQUESTACIÓN)
*   **Última Actualización:** 06/01/2026

## 3. Resumen de la Sesión
- Se ha identificado la estructura de navegación de 3 niveles de Oracle APEX en la UMA:
    1. **Nivel Orquestación:** Obtención de Centros y Titulaciones vía AJAX/Widgets de APEX.
    2. **Nivel Listado:** Filtrado parametrizado por Grado y Año Académico. Descubrimiento de paginación técnica (1-10, 1-11, etc.) oculta bajo el parámetro `min_row`.
    3. **Nivel Detalle:** Página intermedia de "Programación Docente" que contiene el enlace final al PDF en `/ht/2025/`.
- Se han realizado múltiples intentos de scripts unificados que han fallado en el conteo de asignaturas por el ruido del HTML (capturando enlaces de menús y pies de página).
- Se ha verificado que el motor de extracción basado en `pdfplumber` es capaz de parsear correctamente el contenido una vez que se le entrega la URL del PDF real.

## 4. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
### Tarea 1: Implementación del Scraper "Tulipán"
- **Acción:** Crear un script que use la arquitectura de orquestación (Centros -> Grados -> Años) pero que utilice selectores CSS estrictos (`table.t-Report-report`) para evitar el conteo de basura.
- **Acción:** Integrar el motor de extracción de PDF que generó el JSON de éxito (Objetivos, Temario, Bibliografía).
- **Validación:** El script debe imprimir el número de asignaturas que coincida exactamente con lo visualizado en la web (ej. 11, 12, 13).

### Tarea 2: Importación Multirrama
- **Acción:** Ejecutar `import_uma_data.py` con el mapeo de `Branch` basado en el nombre del centro para que los datos se clasifiquen correctamente en las 5 ramas de conocimiento.
