# Anexo del Hito 20: Ingestión de Datos ESAD Córdoba

## 1. Visión y Objetivos
Ampliar la oferta académica de la plataforma integrando el "Grado en Enseñanzas Artísticas Superiores de Diseño de Escenografía" de la ESAD Córdoba.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Última Actualización:** 04/01/2026

## 3. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Tarea 1: Generación de Datos (IA Assisted)
*   **Acción:** Obtener la estructura académica de `https://esadcordoba.com/inicio/oferta-formativa/escenografia/` usando el prompt definido abajo.
*   **Output Esperado:** Archivo `web_scrapping/esad_data.json` con estructura jerárquica.

### Tarea 2: Desarrollo del Importador
*   **Archivo:** `academic_structure/management/commands/import_esad_data.py`.
*   **Lógica:**
    *   Basada en `import_uco_data.py` pero simplificada (una sola rama "Artes y Humanidades").
    *   Crear Universidad: "Escuela Superior de Arte Dramático de Córdoba".
    *   Consumir el JSON para crear Grado, Años y Asignaturas.

### Tarea 3: Ejecución y Verificación
*   Ejecutar: `python manage.py import_esad_data`.
*   Verificar en Admin la correcta creación de la jerarquía.

## 4. Prompt de Extracción para LLM
"Actúa como un scraper de datos académicos. Analiza el HTML de esta URL: https://esadcordoba.com/inicio/oferta-formativa/escenografia/
Extrae las asignaturas del Grado en Escenografía.
Genera un JSON válido con esta estructura estricta:
[
  {
    'degree': 'Grado en Enseñanzas Artísticas Superiores de Diseño de Escenografía',
    'branch': 'Artes y Humanidades',
    'year': 1,
    'subjects': [
      { 'name': 'Nombre Asignatura', 'credits': 6, 'guide_url': 'https://...' }
    ]
  },
  ... (repetir para cursos 2, 3 y 4)
]
Nota: Si la guía docente es un enlace de descarga, inclúyelo en 'guide_url'."
