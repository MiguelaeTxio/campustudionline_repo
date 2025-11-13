# Hito 6: Sistema de Autoevaluaciones con IA (EN PROGRESO)

## Resumen de la Sesión del 13/11/2025 (NRA)

**Objetivo:** Diagnosticar y corregir el error `Not Found: /study-room/directory/undefined` que impedía la navegación en la Sala de Estudio.

**Desarrollo y Resultado Empírico:**
La sesión aplicó un riguroso método empírico para aislar la causa del error.
1.  **Refutación de Hipótesis Inicial:** Se postuló que el error se debía a `slugs` ausentes en la base de datos. Se creó y ejecutó un script de diagnóstico en la shell de Django que inspeccionó los `querysets` exactos utilizados por la vista. La salida del script **refutó empíricamente** esta hipótesis, demostrando que todos los `slugs` necesarios estaban presentes y eran correctos.
2.  **Confirmación de Hipótesis Final:** Al ser los datos del backend correctos, el error se aisló en la capa de presentación. Se modificó la plantilla `_copy_list_partial.html` para añadir comentarios de depuración que expusieran los valores de las variables en el momento del renderizado. Esta instrumentación permitió al usuario confirmar el origen del problema y aplicar la corrección necesaria, resolviendo el error.

**Estado Final:** El error de navegación `undefined` ha sido **solucionado**. Sin embargo, ha surgido una nueva prioridad: la falta de resiliencia en el sistema de generación de autoevaluaciones, que presenta fallos al usuario.

## Hoja de Ruta para la Próxima Sesión

El objetivo principal será rediseñar el sistema de autoevaluaciones para que sea robusto y resiliente ante fallos.

1.  **Análisis del Fallo Actual:** Investigar la causa raíz del "Fallo en la Generación (Reintentando)" reportado.
2.  **Implementación de un Sistema de Reintentos Robusto:** Modificar la tarea Celery responsable de la generación para que incluya reintentos automáticos con `exponential backoff` para errores transitorios (ej: timeouts de API).
3.  **Gestión de Errores Fatales:** Implementar una lógica que distinga entre errores reintentables y errores fatales. Los fallos fatales deberán ser registrados de forma explícita y no se reintentarán indefinidamente.
4.  **Mejora del Feedback al Usuario:** Modificar los estados del modelo `Assessment` para reflejar con mayor precisión el tipo de error. La interfaz de usuario deberá comunicar el estado de forma clara, evitando mensajes genéricos y ofreciendo al usuario una explicación y una acción clara cuando sea posible.
