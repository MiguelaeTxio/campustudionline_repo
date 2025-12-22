# /users/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def commercial_required(function):
    """
    Decorador que comprueba si el usuario pertenece al grupo 'Comerciales'.
    Si no, lanza PermissionDenied (error 403).
    """
    def check_commercial(user):
        if user.is_authenticated and user.groups.filter(name='Comerciales').exists():
            return True
        raise PermissionDenied
    
    return user_passes_test(check_commercial)(function)
