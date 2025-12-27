# Hito 32: Sistema de Visitas Guiadas e Integración de Onboarding

## 1. Visión
Actualización integral del sistema de onboarding (Shepherd.js) para reflejar las últimas funcionalidades críticas de la plataforma: la Agenda Personal y el Asistente UniversIA.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Prioridad:** MÁXIMA

## 3. Hoja de Ruta Táctica para la Siguiente Sesión (LEY SUPREMA)

### A. Actualización del Tour de Inicio (Home Tour)
*   **Archivo:** `static/js/tours/home_tour.js`
*   **Objetivo:** Incluir pasos para la Agenda y, crucialmente, para UniversIA.
*   **Especificaciones del Paso UniversIA:**
    *   **Target:** Botón de chat de UniversIA.
    *   **Contenido Explicativo Obligatorio:**
        1.  **Ubicación:** Indicar claramente dónde se inicia el chat.
        2.  **Rol Global ("Perro Guía" 🦮 y "Secretaria"):** Explicar que en toda la plataforma sirve para ayuda de navegación y para **gestionar eventos y tareas** (Secretaria).
        3.  **Rol Contextual ("Profesora" 🎓):** Aclarar explícitamente que **SÓLO** en la **Sala de Estudio** actúa como tutora/profesora para resolver dudas académicas.

### B. Creación del Tour de Agenda (Schedule Tour)
*   **Archivo:** `static/js/tours/schedule_tour.js` (Neonato)
*   **Objetivo:** Explicar el funcionamiento de la nueva vista de calendario.
*   **Pasos Clave:**
    *   Navegación del calendario (Mes/Semana/Día).
    *   Creación de eventos (Click en día / Botón flotante).
    *   Distinción de tipos de eventos.

### C. Registro
*   Registrar el nuevo tour en `base.html` o en el gestor de tours correspondiente.
