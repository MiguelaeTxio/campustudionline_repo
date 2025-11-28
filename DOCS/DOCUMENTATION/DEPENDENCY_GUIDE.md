---
title: Guía de Dependencias y Stack Tecnológico
project: CampuStudiOnline
last_updated: 2025-11-28
status: Stable
---

# Guía de Dependencias y Stack Tecnológico

## 1. Introducción y Filosofía de Gestión

La gestión de dependencias en **CampuStudiOnline** se rige por el principio de reproducibilidad determinista. Utilizamos `pip-tools` para separar las dependencias lógicas (definidas por el desarrollador) de las dependencias exactas de instalación.

*   **`requirements.in`**: Archivo fuente. Define *qué* librerías necesitamos y, opcionalmente, restricciones de versión mayores.
*   **`requirements.txt`**: Archivo compilado. Generado automáticamente mediante `pip-compile`. Define el árbol completo de dependencias con versiones fijadas (`==`) para garantizar que todos los entornos (Dev, Prod) sean idénticos.

## 2. Catálogo de Dependencias

A continuación se detalla el propósito de cada paquete listado en `requirements.in`, agrupado por su función en la arquitectura del sistema.

### 2.1. Core de Django y Servidor

El núcleo sobre el que se ejecuta la aplicación.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **Django** | `5.0.7` | Framework web de alto nivel. Base de toda la arquitectura. |
| **uvicorn[standard]** | `0.29.0` | Servidor ASGI. Necesario para manejar conexiones asíncronas, WebSockets y las características de tiempo real de la aplicación. |
| **gunicorn** | `22.0.0` | Servidor WSGI. Estándar de industria para despliegue de aplicaciones Python en producción. |

### 2.2. Base de Datos y Entorno

Herramientas para la persistencia de datos y configuración del entorno.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **mysqlclient** | `2.2.4` | Conector DB API optimizado para MySQL, el motor de base de datos de producción. |
| **python-dotenv** | `1.0.1` | Carga variables de entorno desde el archivo `.env` para la gestión segura de secretos y configuración. |
| **django-dotenv** | `1.4.2` | Adaptador específico para integrar `python-dotenv` con el flujo de carga de `manage.py` y `wsgi.py`. |

### 2.3. Utilidades de Django

Extensiones que potencian la funcionalidad nativa del framework.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **crispy-bootstrap5** | `2024.2` | Paquete de plantillas para renderizar formularios Django usando las clases de Bootstrap 5. |
| **django-crispy-forms** | `2.1` | Gestión programática del renderizado de formularios ("DRY forms"). |
| **django-anymail[sendgrid]** | `10.2` | Backend de correo electrónico unificado. Configurado para usar la API de **SendGrid** en producción. |
| **django-cleanup** | `7.0.0` | Mantenimiento automático del almacenamiento: borra los archivos físicos cuando se eliminan sus referencias en la BD. |
| **django-htmx** | `1.18.0` | Extensiones de servidor para integrar **HTMX**, permitiendo interacciones dinámicas SPA-like sin complejidad de React/Vue. |
| **django-markdownify** | `0.9.5` | Filtros de plantilla para renderizar contenido Markdown como HTML seguro. |
| **django-recaptcha** | `4.0.0` | Integración de Google reCAPTCHA para proteger formularios públicos (Login, Registro). |
| **django-user-agents** | `0.4.0` | Identificación del dispositivo cliente (Móvil vs Escritorio) para lógica de renderizado adaptativa. |

### 2.4. Procesamiento de Contenido y Formatos

Herramientas para manejar el contenido educativo, Markdown y estructuras de datos.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **python-frontmatter** | `1.0.0` | Extracción de metadatos YAML incrustados al inicio de los archivos Markdown de contenido. |
| **pymdown-extensions** | `10.8.1` | Extensiones avanzadas para la sintaxis Markdown estándar. |
| **Markdown** | `3.8.2` | Motor base de conversión de texto a HTML. |
| **Pygments** | `2.19.2` | Resaltado de sintaxis de código (syntax highlighting) en los bloques de código del material educativo. |
| **beautifulsoup4** | `4.12.3` | Parsing y limpieza de HTML. Fundamental para tareas de scraping o sanitización. |
| **lxml** | `5.2.2` | Parser XML/HTML de alto rendimiento, backend para BeautifulSoup. |
| **django-treebeard** | `4.7.1` | Implementación eficiente de estructuras de árbol (Materialized Path) para jerarquías académicas y de carpetas. |

### 2.5. Canales y Tiempo Real

Infraestructura para comunicación asíncrona y mensajería.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **redis** | `4.6.0` | Almacén de estructura de datos en memoria. Actúa como *Message Broker* para Celery y capa de canal para WebSockets. |
| **django-webpush** | `0.3.6` | Gestión del protocolo Web Push para notificaciones nativas en el navegador. |

### 2.6. Manipulación de Imágenes y Documentos

Procesamiento de medios estáticos.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **Pillow** | `10.4.0` | Librería estándar de manipulación de imágenes en Python. |
| **weasyprint** | `65.1` | Motor de renderizado visual para convertir HTML/CSS a **PDF** (certificados, informes). |
| **pdf2image** | `1.17.0` | Conversión de páginas de PDF a imágenes rasterizadas (utilizado para previsualizaciones). |

### 2.7. Soporte de Fechas y Zonas Horarias

Garantía de consistencia temporal.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **pytz** | `2024.1` | Definiciones de zonas horarias mundiales (Base de datos Olson). |
| **tzdata** | `2024.1` | Datos de zona horaria oficiales de IANA. |

### 2.8. APIs y Servicios Externos (IA y Cloud)

Integraciones con servicios de terceros.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **google-generativeai** | `0.8.5` | SDK oficial para acceder a los modelos **Gemini** (Inteligencia Artificial Generativa). |
| **google-cloud-vision** | `3.10.2` | API de visión computacional. Utilizada para OCR de alta precisión en procesamiento de documentos (ej. albaranes). |
| **google-api-core** | `2.25.1` | Librerías base comunes para las APIs de Google Cloud. |

### 2.9. Asincronía y Tareas en Segundo Plano

Gestión de procesos fuera del ciclo de petición-respuesta HTTP.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **celery** | `5.4.0` | Cola de tareas distribuida. Maneja procesos pesados (emails, generación de IA) en segundo plano. |
| **django-celery-beat** | `2.8.1` | Programador de tareas periódicas (Cron) integrado con el ORM de Django. |
| **asgiref** | `3.9.1` | Utilitarios para la compatibilidad entre código síncrono y asíncrono. |

### 2.10. Herramientas de Desarrollo

Herramientas para mantener la calidad del código.

| Paquete | Versión | Propósito |
| :--- | :--- | :--- |
| **black** | `25.1.0` | Formateador de código "uncompromising". Garantiza un estilo de código consistente automáticamente. |

---
*Documento generado automáticamente a partir del análisis de `requirements.in` y `requirements.txt`.*
