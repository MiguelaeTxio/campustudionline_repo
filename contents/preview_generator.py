# /home/MiguelAeTxio/CampuStudiOnline/contents/preview_generator.py
import os
import logging
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from pdf2image import convert_from_path

# Importamos la función centralizada y renombrada
from academic_structure.utils import markdown_to_html_with_pygments

logger = logging.getLogger(__name__)

# --- CONSTANTES ---
# Definimos rutas base para evitar repeticiones y facilitar cambios futuros
PREVIEWS_DIR = os.path.join(settings.BASE_DIR, "public_seo_previews")
TEMPLATES_DIR = os.path.join(settings.BASE_DIR, "contents", "templates", "content_public_preview_templates")
INDEX_TEMPLATE = os.path.join(TEMPLATES_DIR, "index_template.html")
CONTENT_DETAIL_TEMPLATE = os.path.join(TEMPLATES_DIR, "content_detail_template.html")


def clean_existing_previews(content_material):
    """
    Elimina los archivos de vista previa antiguos de un material de contenido.
    """
    try:
        # Usamos un patrón para encontrar todos los archivos relacionados
        pattern = f"material_{content_material.pk}"
        for filename in os.listdir(PREVIEWS_DIR):
            if filename.startswith(pattern) and filename.endswith(".html"):
                os.remove(os.path.join(PREVIEWS_DIR, filename))
                logger.info(f"Vista previa HTML antigua eliminada: {filename}")
    except Exception as e:
        logger.error(
            f"Error al limpiar vistas previas antiguas para el material {content_material.pk}: {e}",
            exc_info=True,
        )


def generate_public_preview(content_material):
    """
    Genera una vista previa pública en HTML para un ContentMaterial.
    Esta función ahora también invoca la generación del índice.
    """
    try:
        # 1. Limpiar vistas previas antiguas para evitar duplicados con slugs diferentes
        clean_existing_previews(content_material)

        # 2. Renderizar el contenido del material a HTML
        rendered_content_html = markdown_to_html_with_pygments(
            content_material.body
        )

        # 3. Preparar el contexto para la plantilla de detalle
        context = {
            "content": content_material,
            "rendered_content_html": rendered_content_html,
        }

        # 4. Renderizar la plantilla de detalle completa
        final_html = render_to_string(CONTENT_DETAIL_TEMPLATE, context)

        # 5. Guardar el archivo de vista previa de detalle
        preview_filename = f"material_{content_material.pk}_{content_material.slug}.html"
        preview_filepath = os.path.join(PREVIEWS_DIR, preview_filename)
        with open(preview_filepath, "w", encoding="utf-8") as f:
            f.write(final_html)
        logger.info(f"Vista previa pública generada con éxito: {preview_filename}")

        # 6. Actualizar el índice general después de crear una nueva vista previa
        generate_index_preview()

        return True

    except Exception as e:
        logger.error(
            f"Error crítico al generar la vista previa para el material {content_material.pk}: {e}",
            exc_info=True,
        )
        return False


def generate_index_preview():
    """
    Genera la página de índice (index.html) para todas las vistas previas públicas.
    """
    from .models import ContentMaterial

    try:
        # 1. Obtener todos los materiales de contenido públicos
        public_materials = ContentMaterial.objects.filter(is_public=True).order_by(
            "-created_at"
        )

        # 2. Preparar el contexto para la plantilla del índice
        context = {"public_materials": public_materials}

        # 3. Renderizar la plantilla del índice
        index_html = render_to_string(INDEX_TEMPLATE, context)

        # 4. Guardar el archivo index.html
        index_filepath = os.path.join(PREVIEWS_DIR, "index.html")
        with open(index_filepath, "w", encoding="utf-8") as f:
            f.write(index_html)

        logger.info("Índice de vistas previas públicas actualizado con éxito.")
        return True

    except Exception as e:
        logger.error(
            "Error crítico al generar el índice de vistas previas públicas: %s",
            e,
            exc_info=True,
        )
        return False


def delete_public_preview(content_material):
    """
    Elimina la vista previa pública de un ContentMaterial y regenera el índice.
    """
    try:
        # Limpiar las vistas previas asociadas al material
        clean_existing_previews(content_material)
        logger.info(
            f"Vista previa pública para el material {content_material.pk} eliminada."
        )

        # Regenerar el índice para reflejar la eliminación
        generate_index_preview()
        return True

    except Exception as e:
        logger.error(
            f"Error al eliminar la vista previa para el material {content_material.pk}: {e}",
            exc_info=True,
        )
        return False


def generate_share_card_image(content_material):
    """
    Genera una imagen de tarjeta para compartir en redes sociales a partir de un ContentMaterial.
    La imagen se guarda en la ruta definida en el modelo.
    """
    try:
        # 1. Definir la ruta del archivo temporal y el archivo final
        temp_html_path = os.path.join(
            settings.MEDIA_ROOT, f"temp_share_card_{content_material.pk}.html"
        )
        temp_pdf_path = os.path.join(
            settings.MEDIA_ROOT, f"temp_share_card_{content_material.pk}.pdf"
        )
        final_image_path = os.path.join(
            settings.MEDIA_ROOT, content_material.share_card_image.name
        )
        final_image_dir = os.path.dirname(final_image_path)

        # Asegurarse de que el directorio de destino existe
        os.makedirs(final_image_dir, exist_ok=True)

        # 2. Preparar contexto y renderizar la plantilla HTML
        context = {"material": content_material}
        html_content = render_to_string(
            "contents/share_card_template.html", context
        )
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # 3. Convertir HTML a PDF con WeasyPrint
        HTML(string=html_content).write_pdf(temp_pdf_path)

        # 4. Convertir PDF a imagen con pdf2image
        images = convert_from_path(
            temp_pdf_path,
            dpi=200,  # Aumentamos la resolución para mayor calidad
            fmt="jpeg",
            first_page=1,
            last_page=1,
            size=(1200, 630),  # Tamaño estándar para OG cards
        )

        # 5. Guardar la imagen final
        if images:
            images[0].save(final_image_path, "JPEG", quality=90)  # Ajustamos la calidad
            logger.info(
                f"Imagen para compartir generada con éxito en: {final_image_path}"
            )
            return True
        else:
            logger.error(
                f"No se pudo generar la imagen desde el PDF para el material {content_material.pk}"
            )
            return False

    except Exception as e:
        logger.error(
            f"Error crítico al generar la imagen para compartir para el material {content_material.pk}: {e}",
            exc_info=True,
        )
        return False

    finally:
        # 6. Limpieza de archivos temporales
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
