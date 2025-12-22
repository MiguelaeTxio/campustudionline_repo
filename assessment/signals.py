from django.db import transaction
# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/assessment/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assessment
from contents.services.navigation_builder import refresh_user_navigation

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Assessment)
def assessment_post_save_handler(sender, instance, created, **kwargs):
    """
    Signal handler integral para el modelo Assessment.
    1. Atribuye conversión de 'Primera Evaluación' si aplica.
    2. Actualiza la navegación del usuario.
    """
    # --- ATRIBUCIÓN DE CONVERSIÓN (HITO 30) ---
    if created:
        user_profile = getattr(instance.user, 'userprofile', None)
        if user_profile and user_profile.referred_by and not user_profile.has_claimed_assessment_incentive:
            try:
                user_profile.has_claimed_assessment_incentive = True
                user_profile.save(update_fields=['has_claimed_assessment_incentive'])
                logger.info(f"Conversión de Primera Evaluación atribuida a {user_profile.referred_by.username} por el usuario {instance.user.username}")
            except Exception as e:
                logger.error(f"Error atribuyendo conversión de evaluación: {e}")
    # ------------------------------------------

    # --- Lógica de navegación ---
    try:
        update_fields = kwargs.get('update_fields')
        relevant_fields = {'status', 'was_viewed'}
        if update_fields and not relevant_fields.intersection(update_fields) and not created:
            return

        transaction.on_commit(lambda: refresh_user_navigation(instance.user))
        logger.debug(f"Navegación actualizada por cambio en Assessment {instance.id}")
    except Exception as e:
        logger.error(f"Error actualizando navegación desde señal de Assessment: {e}")
