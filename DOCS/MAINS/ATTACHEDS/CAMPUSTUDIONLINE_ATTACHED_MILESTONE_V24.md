# Hito de Soporte y Mantenimiento: Ruegos y Preguntas

**Propósito:** Hito contenedor persistente para tareas de depuración, resolución de dudas imprevistas y mantenimiento correctivo del sistema.
**Estado:** **EN PROGRESO** (Fase de Monitorización Pasiva)

## Bitácora de Sesión

### 28/11/2025 - 29/11/2025 (Sesiones Previas)
*   Resolución de incidencia crítica de BD (34GB liberados).
*   Reparación integral de Admin Users y Registro.

### 30/11/2025 - Mejoras UX y Seguridad
*   **Spinner Global:** Implementación exitosa de indicador de carga que intercepta navegación interna y formularios.
*   **Anti-Screenshot:** Evaluado y descartado por UX en móvil.

### 01/12/2025 - 05/12/2025 (Semana de Regresión)
*   **Introducción de "Cortafuegos Empírico":** Se introdujo una nueva lógica de cuarentena de API Keys como respuesta a una crisis de disco. Esta lógica, aunque bien intencionada, contenía un defecto de diseño crítico: no validaba si los errores de cuota persistían en la *misma clave*, provocando que tareas con reintentos acumulados pusieran en cuarentena claves sanas al primer fallo, generando una parálisis del sistema.
*   **Crisis de Almacenamiento (Error 122):** Diagnóstico y resolución de llenado de disco provocado por bucles de tareas de evaluación fallidas. La respuesta a esta crisis fue la causa indirecta de la regresión en la gestión de cuotas.

### 07/12/2025 - Restauración de Alto Rendimiento y Estabilización
*   **Diagnóstico Forense:** Mediante análisis cruzado de `git log`, `git show` y el historial de sesiones Gemini, se identificó el commit exacto (`03f80a6`) que introdujo la lógica de cuarentena defectuosa.
*   **Restauración Quirúrgica:** Se ha restaurado la lógica de gestión de cuotas de la versión estable del Lunes 1 (`cee0d26`), que demostró un alto rendimiento (40 cursos/día). Esta lógica no pone claves en cuarentena, simplemente reintenta.
*   **Fusión de Seguridad:** Se ha fusionado el código restaurado con el manejo de excepciones mejorado para las tareas de **evaluación**, previniendo así los bucles infinitos que causaron la crisis de disco original. El resultado es un sistema híbrido que combina la alta productividad del código antiguo con la seguridad del nuevo.
*   **Liberación del Sistema:** Todas las API Keys han sido liberadas de la cuarentena y el sistema de cuarentena automática ha sido desmantelado.

## Hoja de Ruta (Tareas Pendientes)

### Monitorización
*   **Estado:** A la espera de nuevas incidencias. Mantenimiento del hito abierto a petición del usuario.
