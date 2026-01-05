# Anexo del Hito 36: Implementación de la Sala de Traducción (Translation Room)

## 1. Visión y Objetivos
Implementar un módulo de traducción basado en IA que procese texto plano y archivos (PDF, Word, TXT) sin persistencia en base de datos.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Última Actualización:** 05/01/2026

## 3. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Tarea 1: Creación de la App y Routing
- Ejecutar `python manage.py startapp translation_room`.
- Registrar la app en `core/settings.py`.
- Configurar el namespace en `core/urls.py` y crear `translation_room/urls.py`.

### Tarea 2: Lógica de Negocio y Servicios
- Desarrollar `translation_room/services.py`:
    - Integración con `core.services.gemini_service.GeminiService`.
    - Lógica de extracción para `pypdf` y `python-docx`.
    - Implementación de `TranslationManager` para manejar el chunking de documentos largos.

### Tarea 3: Vistas y UI (HTMX)
- Implementar `TranslationHomeView` en `views.py`.
- Crear el template `translation_home.html` utilizando `HTMX` para actualizaciones parciales sin recarga de página.
- Configurar la zona de carga de archivos (File Input) con soporte multiformato.

### Tarea 4: Integración de Conocimiento IA
- Modificar `universia/services.py` para inyectar en el contexto de sistema la existencia de la Sala de Traducción.
- Actualizar el prompt base para que UniversIA redirija consultas de traducción a `/traducciones/`.

### Tarea 5: Tours y UX
- Actualizar `static/js/tours/home_tour.js` para incluir el nodo de la nueva sala.
- Crear `static/js/tours/translation_room_tour.js`.
