# /home/MiguelAeTxio/CampuStudiOnline/contents/utils.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

import logging
import os
import tempfile
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from pdf2image import convert_from_path
from django.db.models import Exists, OuterRef
from .models import FavoriteFolder


# Configuración del logger para este módulo
logger = logging.getLogger(__name__)


def generate_share_image_bytes(context=None):
    """
    Genera una imagen de compartición PNG y la devuelve como un objeto de bytes.
    Utiliza un flujo de dos pasos:
    1. WeasyPrint convierte el HTML a un PDF en un archivo temporal.
    2. pdf2image convierte ese PDF a una imagen PNG en memoria.
    Este enfoque es robusto y evita librerías inestables.
    """
    if context is None:
        context = {}

    # Rutas a los recursos estáticos
    logo_path_svg = os.path.join(settings.STATIC_ROOT, "images/favicon.svg")
    logo_path_png = os.path.join(settings.STATIC_ROOT, "images/favicon-96x96.png")

    final_context = {
        "title": context.get("title", "Únete a la comunidad de CampuStudiOnline"),
        "author": context.get("author", "Tu Plataforma de Estudio Colaborativo"),
        "logo_path_svg": logo_path_svg,
        "logo_path_png": logo_path_png,
    }

    temp_pdf_path = None
    try:
        # --- Renderizado de la plantilla HTML ---
        html_string = render_to_string(
            "contents/share_card_template.html", final_context
        )

        # --- Carga de fuentes personalizadas ---
        font_regular_path = os.path.join(
            settings.STATIC_ROOT, "fonts/Roboto-Regular.ttf"
        )
        font_bold_path = os.path.join(settings.STATIC_ROOT, "fonts/Roboto-Bold.ttf")

        font_face_rules = f"""
            @font-face {{
                font-family: 'Roboto';
                src: url('file://{font_regular_path}');
                font-weight: normal;
                font-style: normal;
            }}
            @font-face {{
                font-family: 'Roboto';
                src: url('file://{font_bold_path}');
                font-weight: bold;
                font-style: normal;
            }}
        """
        css_stylesheet = CSS(string=font_face_rules)
        html = HTML(string=html_string, base_url=f"{settings.SITE_URL}/")

        # PASO 1: Renderizar HTML a PDF en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
            html.write_pdf(target=temp_pdf, stylesheets=[css_stylesheet])
            temp_pdf_path = temp_pdf.name

        # PASO 2: Convertir el PDF temporal a una imagen PNG
        # Usamos `single_file=True` para obtener solo la primera página.
        images = convert_from_path(temp_pdf_path, single_file=True, dpi=192)

        if not images:
            raise RuntimeError("pdf2image no pudo convertir el PDF a imagen.")

        image = images[0]

        # Convertir la imagen de Pillow a bytes en memoria
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        png_bytes = buffer.getvalue()

        logger.info(
            f"Bytes de imagen de compartición generados exitosamente para el título: \"{final_context['title']}\""
        )

        return png_bytes

    except Exception as e:
        logger.exception(f"Error crítico durante la generación de bytes de imagen: {e}")
        return None

    finally:
        # Nos aseguramos de que el archivo temporal se elimine siempre.
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except OSError as e:
                logger.error(
                    f"Error al eliminar el archivo temporal {temp_pdf_path}: {e}"
                )


def annotate_is_favorite(queryset, user):
    """
    Anota un QuerySet de ContentMaterial con un booleano 'is_favorite'
    indicando si el material está en alguna carpeta de favoritos del usuario.
    """
    if user.is_authenticated:
        return queryset.annotate(
            is_favorite=Exists(
                FavoriteFolder.objects.filter(
                    user=user, 
                    materials__pk=OuterRef('pk')
                )
            )
        )
    return queryset
