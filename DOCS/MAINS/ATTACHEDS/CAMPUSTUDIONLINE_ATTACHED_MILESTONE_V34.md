# Anexo del Hito 34: Optimización de Redes Sociales y Metadatos de Compartición

## 1. Estado de la Situación
Se ha detectado un fallo en la generación y visualización de imágenes de previsualización (Open Graph) al compartir enlaces en plataformas externas (WhatsApp, X, LinkedIn). Adicionalmente, la iconografía de Twitter está obsoleta.

## 2. Hoja de Ruta para la Siguiente Sesión (LEY SUPREMA)

### Tarea 1: Diagnóstico de Generación de Imágenes (Empírico)
- Auditar la función `generate_share_image_bytes` en `contents/utils.py`.
- Verificar la existencia de las fuentes y recursos necesarios en el servidor para el renderizado de imágenes.
- Comprobar que las peticiones a las URLs de imágenes dinámicas no devuelven errores 404 o 500.

### Tarea 2: Verificación de Metatags en Templates
- Auditar `base.html` y las vistas de detalle de contenido para asegurar que `og:image` y `twitter:image` entregan URLs absolutas.
- Validar la configuración de `settings.SITE_URL`.

### Tarea 3: Actualización de Identidad Visual (Iconografía)
- Localizar todas las instancias del icono de Twitter en el proyecto.
- Sustituir el icono antiguo por el nuevo logotipo de "X".

### Tarea 4: Test de Integración con Validadores Externos
- Realizar pruebas de scraping mediante herramientas de depuración de Facebook (Open Graph) y X (Card Validator).
