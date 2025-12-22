# Hito 30: Sistema de Atribución Comercial por Código de Recomendación (COMPLETADO)

## 1. Resumen de la Implementación
Se ha implementado con éxito el sistema de atribución de referidos. La lógica ha sido refactorizada para que el consumo del código se realice en el momento de la activación de la cuenta, no durante el registro inicial, evitando la pérdida de códigos. Se ha construido un dashboard de autoservicio para el rol 'Comercial', permitiéndoles generar nuevos lotes de códigos de forma autónoma cuando agotan los existentes, con una notificación de auditoría a los administradores.

## 2. Componentes Afectados
- **`users/models.py`**: Refactorizado `RecommendationCode` y `UserProfile`.
- **`users/forms.py`**: Modificado `UserRegistrationForm` para la nueva lógica.
- **`users/views.py`**: Refactorizadas `validate_registration_view` y `activate_account_view`. Creadas `commercial_dashboard` y `request_new_code_batch`.
- **`users/urls.py`**: Añadidas las rutas para el dashboard y la solicitud de códigos.
- **`users/decorators.py`**: Creado decorador `@commercial_required`.
- **`templates/base.html`**: Añadido enlace condicional al dashboard.
- **`templates/users/commercial_dashboard.html`**: Creada la plantilla del dashboard.
