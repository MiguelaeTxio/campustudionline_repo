import os

# --- ACTUALIZACIÓN HITO 2 (Arquitectura) ---
v02_path = '/home/MiguelAeTxio/PROJECTS/Mecalygest/DOCS/ATTACHMENTS/MECALYGEST_ATTACHED_MILESTONE_V02.md'

# Leemos el archivo original
with open(v02_path, 'r', encoding='utf-8') as f:
    v02_content = f.read()

# Definimos el bloque de texto a añadir antes de "## 2. Requerimientos de Administración"
branding_model = """### 1.6. Módulo de Configuración (White-labeling)
Para permitir la personalización de la interfaz según la imagen corporativa del cliente.

*   **`SystemSettings` (Singleton):**
    *   `client_logo` (ImageField): Logotipo para cabecera y login.
    *   `primary_color` (ColorField): Color corporativo principal.
    *   `secondary_color` (ColorField): Color de acento.
    *   `app_title` (Char): Nombre personalizado de la instancia (ej: "Gestión [NombreCliente]").

"""

# Insertamos el bloque
if "### 1.6." not in v02_content:
    insertion_point = "## 2. Requerimientos de Administración"
    v02_new_content = v02_content.replace(insertion_point, branding_model + insertion_point)
else:
    v02_new_content = v02_content # Ya existe

# Guardamos propuesta V02
with open(v02_path + '.prop', 'w', encoding='utf-8') as f:
    f.write(v02_new_content)


# --- ACTUALIZACIÓN HITO 3 (Interfaz) ---
v03_path = '/home/MiguelAeTxio/PROJECTS/Mecalygest/DOCS/ATTACHMENTS/MECALYGEST_ATTACHED_MILESTONE_V03.md'

with open(v03_path, 'r', encoding='utf-8') as f:
    v03_content = f.read()

branding_ui = """
---

## 5. Requerimientos de Personalización (White-labeling)

La interfaz debe adaptarse dinámicamente a la identidad visual definida en el Hito 2.

*   **Context Processors:** Implementar un context processor global en Django que inyecte el objeto `SystemSettings` en todas las plantillas.
*   **Login Screen:** El formulario de acceso debe mostrar el `client_logo` y usar el `primary_color` en el botón de "Entrar".
*   **Layout Base (`base.html`):**
    *   Navbar/Sidebar: Mostrar `client_logo` y `app_title`.
    *   Estilos CSS: Inyección de variables CSS (`:root`) con los colores configurados para afectar a botones, bordes y acentos de toda la app.
"""

# Añadimos al final del archivo
if "## 5. Requerimientos de Personalización" not in v03_content:
    v03_new_content = v03_content.strip() + "\n" + branding_ui
else:
    v03_new_content = v03_content

# Guardamos propuesta V03
with open(v03_path + '.prop', 'w', encoding='utf-8') as f:
    f.write(v03_new_content)

print("Propuestas generadas correctamente.")
