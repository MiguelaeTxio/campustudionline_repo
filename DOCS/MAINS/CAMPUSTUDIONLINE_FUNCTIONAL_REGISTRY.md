# REGISTRO FUNCIONAL DE CAMPUSTUDIONLINE
> **LEY SUPREMA DE FUNCIONALIDAD Y TERMINOLOGÍA**
> Este documento define qué hace la plataforma, cómo se llama cada zona y cuáles son las reglas inmutables.

## 1. Mapa de Navegación (Estructura Total)
| Zona | Ruta Base | Descripción y Uso |
| :--- | :--- | :--- |
| **Inicio** | `/` | Dashboard principal. Acceso rápido y resumen. |
| **Agenda** | `/schedule/` | Calendario personal de eventos y tareas. |
| **Chat Grupal** | `/chat/` | **Sistema Híbrido:**<br>1. **Salas Globales:** "General" y "Ayuda".<br>2. **Salas de Asignatura:** Acceso automático al crear una **Copia de Estudio** de esa materia. |
| **Mensajería Privada** | `/messaging/` | Chat directo 1 a 1 (Estilo WhatsApp). |
| **Tablón de Anuncios** | `/announcements/` | **Público.** Avisos, compra-venta, compartir piso, comunidad. |
| **Dir. Académico** | `/academic-directory/` | Estructura Reglada Oficial (Uni > Grado > Asignatura). |
| **Dir. Contenidos Libres** | `/search/` | **Explorador de Categorías:** Cursos y tutoriales de Formación Libre. |
| **Sala de Traducción** | `/traducciones/` | Herramienta IA para traducción de textos y documentos (PDF/DOCX). |
| **Directorio Personal** | `/contents/` | **Tu explorador de archivos:** "Mis Favoritos", "Mis Publicaciones" y carpetas personales. |
| **Sala de Estudio** | `/contents/study-room/` | **[CORE]** Donde se estudia. Listado de Copias activas. Único lugar para evaluar. |
| **Mi Portafolio** | `/portfolio/<username>/` | Perfil público, CV social, enlaces y biografía. |
| **Panel de Control** | `/accounts/` | Configuración de cuenta, seguridad, privacidad y perfil. |
| **Buscador Global** | `Navbar` | Herramienta de búsqueda general disponible en la cabecera. |

## 2. Flujos de Trabajo Críticos

### 2.1. El Ciclo de Estudio (El Corazón del Sistema)
1.  **Buscar:** Encuentras material en los *Directorios* o el *Buscador Global*.
2.  **Copiar:** Pulsas **"Crear Copia para Estudio"**. (Nunca se edita el original).
3.  **Estudiar:** Se abre la **Sala de Estudio**.
4.  **Socializar:** Al crear la copia, entras al **Chat de la Asignatura**.

### 2.2. Autoevaluación con IA
*   **Requisito:** Tener una **Copia de Estudio** abierta.
*   **Acción:** Botón "Solicitar Evaluación" en la Sala de Estudio.

### 2.3. Creación de Contenido
*   **Herramienta:** Editor Markdown nativo.
*   **Restricción:** **NO EXISTE SUBIDA DE ARCHIVOS.** Todo se crea en la plataforma.

## 3. Ayuda de Interfaz (Micro-funcionalidad)
Para dudas sobre **"Cómo funciona esta pantalla"** (ej: cómo subrayar, cómo compartir, botones específicos):
*   **PROTOCOLO:** No explicar el "clic a clic".
*   **RESPUESTA:** "Para ver los detalles de los botones y funciones de esta pantalla, por favor pulsa el botón **'Visita Guiada'**."

## 4. Terminología (Anti-Alucinaciones)
*   ❌ Biblioteca -> ✅ Directorios
*   ❌ Subir PDF -> ✅ Crear Material
*   ❌ Muro -> ✅ Tablón de Anuncios
*   ❌ DM -> ✅ Mensajería Privada
