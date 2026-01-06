# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos (Integración UMA)

## 1. Visión y Objetivos
Ampliación de la capacidad de recolección de datos de la plataforma para integrar la Universidad de Málaga (UMA) bajo el nombre "Institución Académica de Málaga".

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (RE-INTENTO REQUERIDO)
*   **Última Actualización:** 06/01/2026

## 3. Resumen de la Sesión
- Análisis de la estructura Oracle APEX de la UMA y descubrimiento de la técnica "Deep Linking" para acceso directo a titulaciones.
- Implementación de la filosofía "Edge Processing": procesamiento, limpieza y estructuración de datos en el entorno local (Termux).
- Desarrollo del Harvester UMA (v1.2) y del comando de gestión `import_uma_data.py`.
- Detección de error de recolección: la web de la UMA requiere iteración explícita por cada curso para devolver los listados completos (el proceso inicial solo capturó el Año 1).
- Purga completa de los registros parciales de la UMA en la base de datos mediante script quirúrgico en la shell.
- Rediseño del script a la versión `uma_final_harvester.py` (v2.1) con iteración forzada de años (1 al 5).

## 4. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
### Tarea 1: Recolección Masiva (Termux)
- **Acción:** Ejecutar `python /sdcard/Download/uma_final_harvester.py` en Termux.
- **Validación:** Asegurar que el JSON generado (`uma_ready_to_deploy.json`) contiene las asignaturas de todos los cursos académicos.

### Tarea 2: Importación y Despliegue
- **Acción:** Subir el JSON a `/home/MiguelAeTxio/SWAP/`.
- **Acción:** Ejecutar `python manage.py import_uma_data /home/MiguelAeTxio/SWAP/uma_ready_to_deploy.json`.
- **Validación:** Verificar en el Directorio Académico que la "Institución Académica de Málaga" muestra la jerarquía completa.
