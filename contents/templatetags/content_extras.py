# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/contents/templatetags/content_extras.py
import markdown
import bleach
from bleach.css_sanitizer import CSSSanitizer
from django import template
from django.utils.safestring import mark_safe
from ..models import FavoriteFolder, MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS, ALLOWED_TAGS, ALLOWED_ATTRIBUTES

register = template.Library()


@register.filter(name="get_item")
def get_item(dictionary, key):
    """
    Allows accessing a dictionary value using a variable as a key in Django templates.
    Usage: {{ my_dictionary|get_item:my_key }}
    ---
    Permite acceder a un valor de un diccionario usando una variable como clave en las plantillas de Django.
    Uso: {{ mi_diccionario|get_item:mi_clave }}
    """
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def get_root_folders(context):
    """
    Returns the current user's root folders for the move modal.
    ---
    Devuelve las carpetas de la raíz del usuario actual para el modal de mover.
    """
    user = context['request'].user
    if not user.is_authenticated:
        return FavoriteFolder.objects.none()
    
    return FavoriteFolder.objects.filter(user=user, parent__isnull=True).order_by('name')


@register.filter(name="render_markdown")
def render_markdown(text):
    """
    Converts Markdown text to safe HTML.
    ---
    Convierte texto Markdown a HTML seguro.
    """
    if not text:
        return ""
    
    try:
        # Convert Markdown to HTML / Convertir Markdown a HTML
        html = markdown.markdown(
            text,
            extensions=MARKDOWN_EXTENSIONS,
            extension_configs=MARKDOWN_EXTENSION_CONFIGS
        )
        
        # Initialize CSS Sanitizer to avoid NoCssSanitizerWarning
        # Inicializar el Sanitizador de CSS para evitar el NoCssSanitizerWarning
        css_sanitizer = CSSSanitizer()
        
        # Clean HTML using bleach / Limpiar el HTML usando bleach
        cleaned_html = bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
            css_sanitizer=css_sanitizer
        )
        
        return mark_safe(cleaned_html)
    except Exception:
        # Fallback to raw text on error / Volver al texto original en caso de error
        return text
