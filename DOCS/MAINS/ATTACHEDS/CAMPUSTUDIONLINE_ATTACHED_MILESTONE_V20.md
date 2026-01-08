# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos (UMA)

## 1. Visión y Objetivos
Sustitución de la estructura de datos fallida de la UMA por una importación limpia y clasificada bajo criterios RUCT, utilizando la extracción universal (parámetro -1).

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (Bloqueo Técnico)
*   **Última Actualización:** 08/01/2026
*   **Resumen Técnico:** 
    *   Se ejecutó la purga nuclear de la UMA (BBDD limpia).
    *   Se identificó que el JSON de origen carecía de los datos de 1º curso.
    *   **CRÍTICO:** El script de recolección universal `uma_grand_master.py` ha fallado sistemáticamente al intentar forzar el parámetro `-1`.
    *   **CAUSA RAÍZ HIPOTÉTICA:** Salvaguarda de **Estado de Sesión de Oracle APEX**. El servidor probablemente rechaza el parámetro `-1` en peticiones GET directas si no se ha originado desde la navegación interna (falta de coincidencia de estado o checksum).
    *   **FALLO DE IA:** Se asume responsabilidad por generar código que ignora la persistencia de estado de la plataforma origen, rompiendo una herramienta que era funcional bajo navegación iterativa.

## 3. Hoja de Ruta para la Próxima Sesión (LEY SUPREMA)
### Tarea 1: Debugging de Sesión APEX
- **Acción:** Testear si el parámetro `-1` funciona realizando un POST previo que emule la selección en el desplegable de "Curso".
- **Alternativa:** Si la salvaguarda persiste, volver a la navegación por cursos (1,2,3,4) pero capturando el "Curso 0" o "Otros" para asegurar que no se pierda ninguna asignatura.

### Tarea 2: Importación y Sincronización
- **Acción:** Ejecutar `import_uma_data` una vez obtenido el JSON íntegro.
- **Acción:** Ejecutar `update_content_flags` (V2) para restaurar visibilidad.
