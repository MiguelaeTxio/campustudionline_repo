# /users/tasks.py
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.
# ATENCIÓN!!! La aplicación de usuarios se llama 'users' pero el Namespace a usar es 'usuarios'.

from celery import shared_task
from django.contrib.auth import get_user_model
import logging

# Opcional: Configurar un logger específico para las tareas si quieres seguir su ejecución
task_logger = logging.getLogger("celery_tasks")


@shared_task
def cleanup_inactive_user(user_id):
    """
    Busca un usuario por su ID y lo elimina si todavía está inactivo.
    Se programa para ejecutarse X minutos después del registro.
    """
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        if not user.is_active:
            task_logger.info(
                f"Limpiando usuario inactivo: {user.username} (ID: {user_id}). La cuenta será eliminada."
            )
            user.delete()
        else:
            task_logger.info(
                f"El usuario {user.username} (ID: {user_id}) ya está activo. No se requiere limpieza."
            )
    except User.DoesNotExist:
        task_logger.warning(
            f"Se intentó limpiar el usuario con ID {user_id}, pero ya no existía. Posiblemente activado y luego eliminado, o nunca existió."
        )
