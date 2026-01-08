# Anexo del Hito 20: Refinamiento del Proceso de Scraping de Datos (UMA)

## 1. Visión y Objetivos
Sustitución de la estructura de datos fallida de la UMA por una importación limpia y clasificada bajo criterios RUCT.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO (Re-planificado por integridad de datos)
*   **Última Actualización:** 08/01/2026

## 3. Hoja de Ruta para la Próxima Sesión (LEY SUPREMA)
### Tarea 1: Purga Estructural de la UMA
- **Acción:** Ejecutar `purge_uma_data.py` con lógica Bottom-Up.
- **Objetivo:** Eliminar todos los registros de la "Institución Académica de Málaga" para evitar duplicados y años fantasma.

### Tarea 2: Re-Importación y Clasificación RUCT
- **Acción:** Ejecutar el importador `import_uma_data.py` aplicando los siguientes filtros:
    - **Validación de ID:** El curso real se define por la terminación del código P3_ID (`-1xx`, `-2xx`, etc.).
    - **Clasificación RUCT:** Asignación de Ramas de Conocimiento basada en el nombre del Grado (ej: Psicología -> Salud).
    - **Limpieza de Naming:** Eliminación de "Plan 20XX" y normalización de títulos.
    - **Filtro de Ruido:** Exclusión de TFG, Prácticas y registros sin temario.

### Tarea 3: Verificación de Integridad
- **Acción:** Validar que los grados nuevos (como Ciberseguridad) muestran únicamente sus años reales (1º a 3º).
