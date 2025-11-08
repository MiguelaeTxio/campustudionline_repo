# /users/templatetags/auth_extras.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'
from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    """
    Filtro de plantilla para verificar si un usuario pertenece a un grupo específico.
    Uso en la plantilla: {% if user|has_group:"NombreDelGrupo" %}
    """
    if not user.is_authenticated:
        return False

    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        # Si el grupo no existe, devuelve False para evitar errores en producción
        return False
