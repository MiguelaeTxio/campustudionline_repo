# Hito 24: Soporte y Mantenimiento: Ruegos y Preguntas

## 1. Visión y Objetivos
Auditar y validar los sistemas críticos de la plataforma en la fase final de pruebas previa al lanzamiento comercial. Priorizar la estabilidad y la experiencia del usuario final sobre la generación automática de contenido. Mantenimiento evolutivo y resolución de incidencias bajo demanda.

## 2. Estado del Hito
*   **Estado:** EN PROGRESO
*   **Fecha de Inicio:** 14/12/2025

## 3. Hoja de Ruta Táctica

### 3.1. Gestión de Costes y Orquestación (COMPLETADO)
*   [x] **Implementación de Lógica Híbrida en el Orquestador:** Se ha modificado el núcleo (`tasks.py`) para desacoplar la generación masiva de las solicitudes prioritarias.
*   [x] **Sistema de Doble Interruptor:** Implementación en el Panel de Administración de controles independientes para "Sistema General" (Emergencia) y "Generación Masiva" (Ahorro).
*   [x] **Estrategia de Viabilidad:** El sistema queda configurado por defecto para atender exclusivamente Evaluaciones y Solicitudes de usuarios, pausando el relleno de fondo para contener el gasto de API.

### 3.2. Operaciones de Marketing (COMPLETADO)
*   [x] **Incidencia Meta Ads:** Resolución de problemas de visualización y contexto en el Administrador de Anuncios para la campaña de tráfico frío.

### 3.3. Soporte y Mantenimiento Continuo (EN CURSO)
*   [x] **Automatización de Solicitudes Académicas:** Implementación de "tubería directa" (Señales) para aprobar y lanzar tareas de generación automáticamente al solicitar una asignatura. Mejora de UX para feedback inmediato ("Generando...").
*   [ ] **Resolución de Incidencias:** Atención a errores reportados o detectados en la operativa diaria.
*   [ ] **Monitorización:** Vigilancia del comportamiento del modelo de negocio (Evaluaciones) en el entorno de producción.

## 4. Notas de Ejecución
Este hito actúa como un contenedor abierto para cualquier tarea de mantenimiento o soporte que surja durante la fase de validación comercial.
