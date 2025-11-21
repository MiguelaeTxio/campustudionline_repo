# Hito 6: Sistema de Autoevaluaciones con IA (PAUSADO)

**Motivo de la Pausa:**
Se ha detectado una fragilidad crítica en el sistema de navegación de la "Sala de Estudio" que afecta directamente a la usabilidad de las evaluaciones. La arquitectura actual basada en deducción de jerarquías en tiempo real mediante consultas anidadas profundas es insostenible y propensa a errores por inconsistencias de datos (slugs). Se requiere una refactorización arquitectónica previa (Nuevo Hito 22) para implementar un sistema de navegación centrado en el usuario y persistente.

**Estado al Pausar:**
*   El sistema de evaluaciones (backend) funciona correctamente (generación y corrección con IA).
*   El problema reside exclusivamente en el acceso y navegación a las copias de estudio donde se alojan estas evaluaciones.

**Próximos Pasos (Al reanudar):**
1.  Integrar las vistas de evaluación con el nuevo sistema de navegación `UserStudyNavigation` (Hito 22).
2.  Verificar el flujo completo de usuario tras la refactorización.
