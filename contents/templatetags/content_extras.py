# /home/MiguelAeTxio/CampuStudiOnline/contents/templatetags/content_extras.py
from django import template
from ..models import FavoriteFolder

register = template.Library()


@register.filter(name="get_item")
def get_item(dictionary, key):
    """
    Permite acceder a un valor de un diccionario usando una variable como clave en las plantillas de Django.
    Uso: {{ mi_diccionario|get_item:mi_clave }}
    """
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def get_root_folders(context):
    """
    Devuelve las carpetas de la raíz del usuario actual para el modal de mover.
    """
    user = context['request'].user
    if not user.is_authenticated:
        return FavoriteFolder.objects.none()
    
    return FavoriteFolder.objects.filter(user=user, parent__isnull=True).order_by('name')
