# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 09/11/2025 (NRA)

**Objetivo Inicial:** Resolver cuatro incidencias relacionadas con la visualización de los indicadores de estado de las autoevaluaciones (`badges`).

**Progreso y Descubrimientos Clave:**

1.  **Resolución de Incidencias Menores:** Se corrigieron con éxito tres de las cuatro incidencias originales mediante modificaciones atómicas y auditadas (protocolo `PMA`):
    *   **Incidencia 2:** Eliminada la leyenda de indicadores de "Mi Explorador Personal".
    *   **Incidencia 4:** Implementado un *tooltip* informativo en el botón deshabilitado de "Solicitar Evaluación".
    *   **Inconsistencia Visual:** Corregido el color del indicador de navegación en la "Sala de Estudio" para alinearlo con el branding de la plataforma.

2.  **Diagnóstico de Causa Raíz (Incidencias 1 y 3):** La investigación sobre la ausencia de *badges* en los directorios reveló un fallo de diseño fundamental en la utilidad `get_latest_active_assessment_subqueries`. Se demostró empíricamente que esta función:
    *   Excluye deliberadamente los estados de fallo (`FAILED`), impidiendo su visualización.
    *   Carece de la capacidad de agregar múltiples estados de nodos hijos para reflejarlos en un nodo padre.
    *   Es incapaz de implementar la lógica para el indicador de "Múltiples estados diferentes".

**Estado Final:** Se ha identificado que la solución a la visibilidad de los *badges* no es un parche, sino una refactorización de la lógica de propagación de estados. Las correcciones superficiales aplicadas inicialmente a las vistas fueron insuficientes al no abordar el fallo en la utilidad subyacente.

## Hoja de Ruta para la Próxima Sesión

La próxima sesión se centrará **exclusivamente** en la refactorización completa del sistema de indicadores de evaluación para cumplir con el requisito de que todos los estados de la leyenda se propaguen jerárquicamente en los tres directorios.

1.  **Objetivo Principal: Refactorizar la Lógica de Anotación de Estados:**
    *   Diseñar y desarrollar una nueva utilidad (o modificar la existente) que sea capaz de consultar **todos** los descendientes de un nodo de directorio (Área, Disciplina, Categoría, etc.).
    *   La nueva lógica deberá contar los **estados distintos** de las evaluaciones encontradas.
    *   Implementar la regla de negocio: si el recuento de estados distintos es > 1, el nodo padre debe ser anotado con un estado "Múltiple". Si es 1, se anota con ese único estado. Si es 0, no se anota nada.
    *   La consulta debe incluir **todos** los estados relevantes de la leyenda, incluyendo los de fallo (`FAILED`, `TIMEOUT_FAILURE`, etc.).

2.  **Objetivo Secundario: Integración y Verificación:**
    *   Integrar la nueva utilidad en las vistas de los tres directorios: `academic_directory`, `search` (Contenidos Libres) y `contents` (Sala de Estudio).
    *   Verificar empíricamente que los *badges* se muestran correctamente en todos los niveles y para todos los estados posibles.
