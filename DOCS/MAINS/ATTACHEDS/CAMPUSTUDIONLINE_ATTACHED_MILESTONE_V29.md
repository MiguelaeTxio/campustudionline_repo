# Anexo del Hito 29: Extensión de UniversIA a la Plataforma

## 1. Estado de la Situación
UniversIA está operativa pero requiere ajustes de seguridad en el frontend para evitar inyecciones masivas de texto y un refinamiento de su personalidad para operar estrictamente como asistente de navegación fuera de la Sala de Estudio.

## 2. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Tarea 1: Hardening del Frontend (Seguridad de Input)
- **Objetivo:** Prevenir la carga masiva de texto que pueda desestabilizar el servidor o consumir tokens excesivos.
- **Implementación Técnica:**
    - Modificar el JavaScript del chat (`universia.js` o equivalente).
    - Implementar listeners para bloquear eventos `paste`, `copy`, `cut` y `contextmenu` (clic derecho) en el área de entrada de texto.
    - Validar longitud máxima de caracteres en el frontend antes del envío.

### Tarea 2: Ingeniería de Prompt (Comportamiento)
- **Objetivo:** Definir límites claros de operación para UniversIA fuera de contextos educativos específicos.
- **Lógica de Prompt:**
    - **Rol Base:** Secretaria Virtual y Asistente de Navegación/Agenda.
    - **Restricción Estricta:** Si el usuario pregunta dudas teóricas o sobre contenido específico *sin* estar en una sesión de estudio vinculada, UniversIA debe rechazar amablemente la respuesta.
    - **Protocolo de Derivación:** Instruir explícitamente al usuario para que busque el material en la Biblioteca, cree una copia en su Sala de Estudio y realice la consulta desde allí.
    - **Excepción:** Permitir dudas operativas sobre el uso de la plataforma.

### Tarea 3: Verificación
- Comprobar bloqueo de pegado en chat.
- Verificar respuesta de UniversIA ante una pregunta académica compleja fuera de contexto (debe derivar).
