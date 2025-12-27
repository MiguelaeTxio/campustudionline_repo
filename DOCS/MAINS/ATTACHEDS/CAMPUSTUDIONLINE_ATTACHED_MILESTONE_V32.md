# Hito 32: Sistema de Visitas Guiadas e Integración de Onboarding

## 1. Visión
Actualización integral del sistema de onboarding (Shepherd.js) para reflejar las últimas funcionalidades críticas de la plataforma: la Agenda Personal y el Asistente UniversIA.

## 2. Estado del Hito
*   **Estado:** COMPLETADO
*   **Fecha de Finalización:** 27/12/2025

## 3. Resumen de Ejecución
Se han implementado satisfactoriamente las guías interactivas para mejorar la adoptabilidad de las nuevas herramientas:

1.  **Tour de Agenda (`schedule_tour.js`):**
    *   Creado nuevo tour específico para la vista de calendario.
    *   Incluye 5 pasos: Bienvenida, Navegación, Detalle, Creación Manual y **Atajo UniversIA** (explicando el rol de "Secretaria" y la capacidad de mover el icono).

2.  **Tour de Inicio (`home_tour.js`):**
    *   Actualizado para señalar el nuevo acceso a la Agenda.
    *   Añadida explicación detallada sobre los roles de UniversIA (Global vs Contextual) y la usabilidad del widget (Drag & Drop).
    *   **Versionado:** Se actualizó el ID del tour a `home_v32` para forzar su visualización a todos los usuarios.

3.  **Optimización:**
    *   Integración en `base.html` mediante carga condicional de recursos (el JS del tour de agenda solo se carga en esa sección).

