# /academic_structure/decorators.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'

from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def can_access_academic_structure_panel(user):
    """
    Comprueba si un usuario tiene permiso para acceder al Centro de Mando.
    La regla es: Verdadero si el usuario es superusuario, o si es un miembro del staff
    Y ADEMÁS pertenece al grupo 'Colaboradores'.
    """
    if not user.is_authenticated:
        return False

    # --- INICIO DE LA MODIFICACIÓN ---
    # La condición que implementa la regla de negocio CORRECTA.
    # Un usuario normal debe ser staff Y estar en el grupo.
    is_collaborator = (
        user.is_staff and user.groups.filter(name="Colaboradores").exists()
    )
    return user.is_superuser or is_collaborator
    # --- FIN DE LA MODIFICACIÓN ---


# Creamos el decorador usando la función de test de Django
# Redirige a la página de login del admin si el test falla
collaborator_required = user_passes_test(
    can_access_academic_structure_panel, login_url=reverse_lazy("admin:login")
)
