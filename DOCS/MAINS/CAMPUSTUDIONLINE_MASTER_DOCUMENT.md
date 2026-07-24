# Documento Maestro: Proyecto CampuStudiOnline
---
## 1. Visión General del Proyecto
CampuStudiOnline es una plataforma web de e-learning diseñada para centralizar materiales de estudio, facilitar la colaboración entre estudiantes a través de salas de chat y anotaciones, y ofrecer herramientas de autoevaluación personalizadas mediante Inteligencia Artificial.
---
## 2. Arquitectura Técnica y Estructural del Proyecto
### 2.1. Entorno de Ejecución
*   **Entorno virtual:** campus_pa_env_py3.10
*   **Ruta local:** /c/Users/numme/Downloads/DirectorioDescargasPVR/
*   **Ruta Pythonanywhere:** /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/ (corregido 2026-07-24: la prosa decía `/home/MiguelAeTxio/CampuStudiOnline/`, sin `PROJECTS/`, en contradicción con `SESSION_VARIABLES.md` y con la ruta absoluta real usada en `academic_structure/management/commands/import_uma_data.py`; se confirma como correcta la ruta con `PROJECTS/`)
*   **Usuario y ruta Pythonanywhere:** MiguelAeTxio@ssh.pythonanywhere.com:CampuStudiOnline/
*   **Framework:** Django
*   **Servidor de Aplicación:** WSGI
*   **Gestión de Secretos:** Las variables de entorno y secretos se gestionan a través de un archivo `.env` y se cargan con `python-dotenv`.
### 2.1.1. Logs del Servidor (PythonAnywhere)
Los archivos de log de la aplicación en producción se encuentran en las siguientes rutas:
*   **Access log:** `/var/log/www.campustudionline.com.access.log`
*   **Error log:** `/var/log/www.campustudionline.com.error.log`
*   **Server log:** `/var/log/www.campustudionline.com.server.log`
*   **Logs históricos rotados:** `/var/log/` (con sufijos de fecha)
*   **Nota:** Los logs de Django (`manage.py` commands) emiten directamente a `stdout` — para capturarlos redirigir con `> /home/MiguelAeTxio/SWAP/output.txt 2>&1`.
### 2.2. Arquitectura de Aplicaciones Django (Fusionada y Verificada)
*   `academic_chat`: [FUNCIÓN PENDIENTE DE DOCUMENTAR - Aplicación funcional e independiente].
*   `academic_directory`: Expone una navegación pública de la estructura académica.
*   `academic_structure`: Es el pilar de la jerarquía académica (`University` -> `Branch` -> `Degree` -> `Subject`).
*   `announcements`: Un Tablón de Anuncios simple para comunicaciones generales.
*   `assessment`: Gestiona modelos y vistas de autoevaluación. Lógica de tareas centralizada en `orchestrator`.
*   `assessment_v2`: Nuevo motor de acreditación (v2) con arquitectura segregada, gestión de planes y tracking de costes.
*   `chat`: Sistema de Comunicación Grupal con salas públicas/privadas, roles y membresías.
*   `contents`: Es la Biblioteca Central y la Sala de Estudio.
*   `core`: El núcleo de Django (settings, urls, etc.).
*   `global_settings`: Panel de control singleton para Configuraciones Globales.
*   `messaging`: Sistema de Comunicación Privada (P2P).
*   `portfolio`: El Perfil Social del Usuario.
*   `push_tester`: Aplicación de diagnóstico para notificaciones push.
*   `search`: Actúa como el Explorador del Campus.
*   `users`: Gestiona la identidad y seguridad.
### 2.3. Control de Versiones
*   **Repositorio Remoto:** De acuerdo con la convención de la plataforma, el nombre canónico del repositorio para este proyecto es `campustudionline_repo`.
---
## 3. Hoja de Ruta Estratégica Consolidada
### Hito 37: Migración a Gemini 3 Flash y Estandarización de SDK
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V37.md`)

### Hito 1: Migración del Sistema de Mensajería y Chat a WSGI
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V01.md`)
### Hito 2: Optimización para Motores de Búsqueda (SEO)
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V02.md`)
### Hito 3: Ecosistema de Salas de Chat Globales y Contextuales
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V03.md`)
### Hito 4: Gestión Avanzada de Cuentas de Usuario
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V04.md`)
### Hito 5: Mantenimiento y Mejoras Generales
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V05.md`)
### Hito 18: Re-arquitectura del Generador de Contenido
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V18.md`)
### Hito 19: Re-arquitectura de los Directorios de Navegación
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V19.md`)
### Hito 6: Sistema de Autoevaluaciones con IA
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V06.md`)
### Hito 7: Mejoras de Usabilidad y Feedback de Usuario
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V07.md`)
### Hito 8: Estandarización de Imagen Corporativa en Emails
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V08.md`)
### Hito de Depuración: Sistema de Notificaciones Push
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V10.md`)
### Hito de Estabilización: Generador de Contenido v5
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V11.md`)
### Hito 12: Migración a Python 3.9+ y SDK de Google Gen AI
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V12.md`)
### Hito Final 1: Refinamiento y Coherencia del Código
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V14.md`)
### Hito Final 2: Documentación de Proyecto
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V13.md`. Manual de Arquitectura, Referencia de Componentes y Guía de Dependencias finalizados.)
### Hito 20: Refinamiento del Proceso de Scraping de Datos
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V20.md`)
### Hito 21: Refactorización del Orquestador de Tareas Asíncronas
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V21.md`)
### Hito 22: Refactorización de Navegación de Sala de Estudio
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V22.md`)
### Hito 23: Cumplimiento Normativo y Legal
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V23.md`)
### Hito 25: Estrategia de Campaña Meta Ads
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V25.md`)
### Hito 26: Cumplimiento Regla de Oro del Idioma
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V26.md`. Corrección de textos de interfaz en mensajería.)
### Hito 35: Optimización de Infraestructura Redis y Gestión de Tareas
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V35.md`)

### Hito 36: Implementación de la Sala de Traducción
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V36.md`)



### Hito 24: Sistema de Ruegos y Preguntas
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V24.md`)
---
### Hito 27: Optimización de UX y Onboarding para Evaluaciones
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V27.md`)
### Hito 28: Implementación de Asistente Contextual 'UniversIA'
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V28.md`)
---
### Hito 30: Estrategia Comercial de Recomendación y Gestión de Afiliados
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V30.md`)

### Hito 31: Sistema de Agenda Académica Personal (Schedule)
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md`. Funcionalidad técnica completada. Pendiente integración futura con IA.)
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V31.md`)

### Hito 32: Sistema de Visitas Guiadas e Integración de Onboarding
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V32.md`)

### Hito 33: Optimización de Comunicaciones Administrativas
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V33.md`)

---

### Hito 34: Optimización de Redes Sociales y Metadatos de Compartición
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V34.md`)

## 4. Reglas de Negocio Clave
### 4.1. Módulo `contents` (Sala de Estudio)
*   **Límite de 6 copias de estudio por usuario:** Para evitar el abuso de recursos y mantener la relevancia del espacio de trabajo del usuario, cada cuenta está limitada a un máximo de 6 `ContentCopy` activas simultáneamente.
*   **Adición automática a favoritos:** Al crear una `ContentCopy` de un material de estudio, el `ContentMaterial` original se añade automáticamente a la carpeta "Mis Favoritos" del usuario.

### Hito 29: Extensión de UniversIA a la Plataforma
(Ver anexo `CAMPUSTUDIONLINE_ATTACHED_MILESTONE_V29.md`)

---
