
## Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)
1. **OPTIMIZACIÓN DEL ADMIN (ÚNICA TAREA):** Ejecutar una auditoría de rendimiento integral y optimización exclusiva del administrador de Django (`django.contrib.admin`).
2. **OBJETIVO:** Eliminar cualquier latencia en la carga de vistas del Admin.
3. **MÉTODO:** Aplicación estricta de `select_related`, `prefetch_related` y `defer` sobre los modelos `ChatRoom`, `ChatMessage` y `ContentMaterial`. Sin inventar ni suponer nada más.
