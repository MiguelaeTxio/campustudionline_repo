# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assessment
from contents.services.navigation_builder import refresh_user_navigation

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Assessment)
def update_navigation_on_assessment_change(sender, instance, created, **kwargs):
    """
    Actualiza el árbol de navegación del usuario cuando cambia el estado
    de una evaluación (ej: de PENDING a COMPLETED).
    """
    try:
        # Solo actualizamos si hay cambios relevantes para la navegación
        # (aunque por simplicidad y seguridad, actualizamos siempre que se guarde)
        refresh_user_navigation(instance.user)
        logger.debug(f"Navegación actualizada por cambio en Assessment {instance.id}")
    except Exception as e:
        logger.error(f"Error actualizando navegación desde señal de Assessment: {e}")
