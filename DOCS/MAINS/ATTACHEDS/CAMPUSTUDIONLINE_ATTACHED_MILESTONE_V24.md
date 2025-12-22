# Hito 24: Sistema de Ruegos y Preguntas (FAQ)

## 1. Visión Estratégica
Desarrollar una sección de "Preguntas Frecuentes" (FAQ) para reducir la carga de soporte y mejorar la experiencia de usuario, proporcionando respuestas claras y accesibles a las dudas más comunes.

## 2. Hoja de Ruta Táctica para la Siguiente Sesión
1.  **[ ] FASE 1: Modelo de Datos.**
    *   Crear una nueva aplicación Django llamada `faq`.
    *   Dentro de `faq/models.py`, definir el modelo `QuestionAnswer`:
        *   `category`: CharField con `choices` para agrupar preguntas (Ej: 'Cuenta', 'Pagos', 'Uso de la Plataforma').
        *   `question`: TextField para la pregunta.
        *   `answer`: TextField para la respuesta (se puede usar Markdown).
        *   `is_visible`: BooleanField para controlar la publicación.
        *   `order`: PositiveIntegerField para ordenar las preguntas dentro de una categoría.

2.  **[ ] FASE 2: Integración en el Admin.**
    *   Registrar el modelo `QuestionAnswer` en `faq/admin.py`.
    *   Utilizar `list_display`, `list_filter` y `list_editable` para una gestión eficiente.

3.  **[ ] FASE 3: Backend y Frontend.**
    *   Crear una vista en `faq/views.py` que obtenga todas las `QuestionAnswer` visibles, agrupadas por categoría.
    *   Crear una plantilla `faq/faq_list.html` que renderice las preguntas y respuestas en un formato de acordeón (Bootstrap Collapse).
    *   Crear la URL correspondiente en `faq/urls.py` e incluirla en el `core/urls.py` principal.

4.  **[ ] FASE 4: Enlace en la Interfaz.**
    *   Añadir un enlace a la nueva sección de "Ayuda" o "FAQ" en el footer (`templates/base.html`).
