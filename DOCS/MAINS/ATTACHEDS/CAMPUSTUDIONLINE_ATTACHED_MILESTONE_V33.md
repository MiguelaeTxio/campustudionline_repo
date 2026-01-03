# Anexo del Hito 33: Optimización de Comunicaciones Administrativas

## 1. Estado de la Situación
- **Problema:** El formulario de envío de "Circulares" desde el panel de administración (`global_settings`) inyecta automáticamente saludos y despedidas (boilerplate) que no son visibles para el administrador durante la redacción.
- **Consecuencia:** El administrador tiende a escribir manualmente saludos/despedidas, resultando en correos con textos duplicados (ej: "Hola, Hola...").

## 2. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Tarea 1: Análisis del boilerplate actual
- Localizar la lógica de inyección de texto en `global_settings/views.py` o `services`.
- Revisar el template `admin/global_settings/send_custom_email.html`.

### Tarea 2: Refactorización de UX
- **Opción A (Backend):** Eliminar la inyección automática y pre-poblar el campo `body` del formulario con el texto boilerplate para que sea editable/visible.
- **Opción B (Frontend):** Mostrar una previsualización en tiempo real o un aviso claro de "Texto que se añadirá automáticamente".
- **Decisión:** Se priorizará la **Opción A** (Pre-poblado) por ser más transparente y flexible ("Lo que ves es lo que envías").

